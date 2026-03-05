from sqlalchemy.orm import Session
from database import SessionLocal
import models

def seed_data():
    db = SessionLocal()
    try:
        # Check if we already have data to prevent duplicates
        if db.query(models.JobBlog).count() == 0:
            jobs = [
                models.JobBlog(
                    company_name="Google",
                    requirements="Experience with Python, FastAPI, and Vector Databases for AI applications.",
                    hr_questions="How do you handle high-dimensional vector similarity in PostgreSQL?"
                ),
                models.JobBlog(
                    company_name="Amazon",
                    requirements="AWS Cloud Architect to manage scalable infrastructure and RDS instances.",
                    hr_questions="Describe a time you had to resolve a database port conflict in a production environment."
                ),
                models.JobBlog(
                    company_name="OpenAI",
                    requirements="ML Engineer focused on RAG pipelines and LLM fine-tuning.",
                    hr_questions="Explain the difference between Cosine Similarity and Euclidean Distance."
                )
            ]
            db.add_all(jobs)
            db.commit()
            print("Successfully seeded 3 Job Blogs into the database!")
        else:
            print("Database already has job blogs. No new data added.")
    except Exception as e:
        print(f"Oops! Something went wrong while seeding: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()