from sqlalchemy import String, Text, Float, ForeignKey, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector
from database import Base

class JobBlog(Base):
    __tablename__ = "job_blogs"
    id: Mapped[int] = mapped_column(primary_key=True)
    company_name: Mapped[str] = mapped_column(String(100))
    requirements: Mapped[str] = mapped_column(Text)
    hr_questions: Mapped[str] = mapped_column(Text) # The "Brain Teasers" from HR

class Candidate(Base):
    __tablename__ = "candidates"
    match_reason = Column(String, nullable=True)
    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255))
    experience_summary: Mapped[str] = mapped_column(Text)
    quiz_score: Mapped[float] = mapped_column(Float, default=0.0)
    resume_vector: Mapped[Vector] = mapped_column(Vector(768)) # 768 for Gemini
    applied_job_id: Mapped[int] = mapped_column(ForeignKey("job_blogs.id"))