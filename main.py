from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, database
from database import get_db, engine
from services.ai_engine import get_embedding, generate_match_reason
from services.quiz_tool import create_custom_quiz
from fastapi.middleware.cors import CORSMiddleware
from scipy.spatial.distance import cosine
import numpy as np
from fastapi.staticfiles import StaticFiles

# Create tables on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/jobs")
def list_jobs(db: Session = Depends(get_db)):
    return db.query(models.JobBlog).all()

@app.post("/api/jobs")
async def create_job(job_data: dict, db: Session = Depends(get_db)):
    new_job = models.JobBlog(
        company_name=job_data.get('company_name'),
        requirements=job_data.get('requirements'),
        hr_questions=job_data.get('hr_questions')
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return {"status": "Job Posted Successfully", "job_id": new_job.id}

@app.post("/api/apply/{job_id}")
async def apply_to_job(job_id: int, name: str, experience: str, score: float, db: Session = Depends(get_db)):
    job = db.query(models.JobBlog).filter(models.JobBlog.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    # Process AI context
    vector = get_embedding(experience)
    reason = generate_match_reason(experience, job.requirements)
    
    new_candidate = models.Candidate(
        full_name=name,
        experience_summary=experience,
        quiz_score=score,
        resume_vector=vector,
        applied_job_id=job_id,
        match_reason=reason
    )
    db.add(new_candidate)
    db.commit()
    return {"status": "Application Submitted", "reason": reason}

import numpy as np

@app.get("/api/results/{job_id}")
def get_sorted_candidates(job_id: int, db: Session = Depends(get_db)):
    job = db.query(models.JobBlog).filter(models.JobBlog.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    job_vector = get_embedding(job.requirements)
    candidates = db.query(models.Candidate).filter_by(applied_job_id=job_id).all()
    
    ranked_list = []
    for c in candidates:
        similarity = 0
        # FIX: Check if vector exists using len() to avoid ambiguity error
        if c.resume_vector is not None and len(c.resume_vector) > 0:
            dist = cosine(job_vector, c.resume_vector)
            # FIX: Prevent NaN values from crashing JSON
            similarity = 1 - dist if not np.isnan(dist) else 0
        
        final_score = (similarity * 0.5) + ((c.quiz_score / 100) * 0.5)
        
        ranked_list.append({
            "id": c.id,
            "full_name": c.full_name,
            "final_score": round(float(final_score) * 100, 2), # Force standard float
            "quiz_score": c.quiz_score,
            "match_reason": c.match_reason or "Reviewing technical profile..."
        })

    ranked_list.sort(key=lambda x: x["final_score"], reverse=True)
    return {
        "toppers": ranked_list[:3],
        "near_miss": ranked_list[3:6]
    }
@app.post("/api/generate-quiz/{job_id}")
async def generate_user_quiz(job_id: int, db: Session = Depends(get_db)):
    # FIXED: .get() replaced with .filter().first() for stability
    job = db.query(models.JobBlog).filter(models.JobBlog.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return create_custom_quiz(job.requirements, job.hr_questions)