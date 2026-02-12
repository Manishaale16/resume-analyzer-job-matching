from fastapi import APIRouter, Depends, Body
from app.services.ai_service import ai_service
from app.services.database import get_database

router = APIRouter()

# Mock job database with experience requirements
MOCK_JOBS = [
    {
        "id": 1, 
        "title": "Senior Software Engineer", 
        "company": "TechCorp", 
        "description": "We are looking for a Senior Developer with 5+ years of experience in Python and FastAPI. Expertise in React and PostgreSQL is required."
    },
    {
        "id": 2, 
        "title": "Frontend Developer", 
        "company": "DesignSoft", 
        "description": "Junior Frontend role. Requires 1 year of experience with React, Tailwind CSS, and Typescript."
    },
    {
        "id": 3, 
        "title": "AI Research Scientist", 
        "company": "DataViz", 
        "description": "Experienced researcher with 8 years of experience. Specialization in NLP, Machine Learning, and Python required."
    },
]

@router.post("/match")
async def match_jobs(resume_text: str = Body(..., embed=True)):
    results = []
    resume_clean = ai_service.clean_text(resume_text)
    
    for job in MOCK_JOBS:
        job_desc_clean = ai_service.clean_text(job["description"])
        analysis = ai_service.analyze_resume(resume_clean, job_desc_clean)
        
        results.append({
            "id": job["id"],
            "title": job["title"],
            "company": job["company"],
            "match_score": analysis["overall_match"],
            "experience_score": analysis["experience_score"],
            "skill_score": analysis["skill_match_score"],
            "matched_skills": analysis["matched_skills"],
            "missing_skills": analysis["missing_skills"],
            "experience_detected": analysis["resume_exp"],
            "experience_required": analysis["required_exp"],
            "why_this_job": f"Matches {len(analysis['matched_skills'])} critical skills and fits the {analysis['required_exp']}-year experience profile."
        })
    
    # Sort by match score
    results.sort(key=lambda x: x["match_score"], reverse=True)
    return results

@router.get("/")
async def get_jobs():
    return MOCK_JOBS
