from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from app.services.ai_service import ai_service
from app.services.database import get_database
from app.api.deps import get_current_user, get_current_user_optional
import os
import shutil
from uuid import uuid4
from datetime import datetime
from typing import Optional

router = APIRouter()

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@router.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...),
    db = Depends(get_database),
    current_user: Optional[dict] = Depends(get_current_user_optional)
):
    # Save file temporarily
    file_ext = os.path.splitext(file.filename)[1]
    temp_filename = f"{uuid4()}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, temp_filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        # Extract text
        if file_ext.lower() == ".pdf":
            resume_text = ai_service.extract_text_from_pdf(file_path)
        elif file_ext.lower() == ".docx":
            resume_text = ai_service.extract_text_from_docx(file_path)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format. Please upload PDF or DOCX.")
        
        # Clean text
        resume_text_clean = ai_service.clean_text(resume_text)
        job_desc_clean = ai_service.clean_text(job_description)
        
        # Analyze
        analysis_result = await ai_service.analyze_resume_llm(resume_text_clean, job_desc_clean)
        
        # Save to database if user is logged in
        if current_user:
            analysis_record = {
                "user_id": str(current_user["_id"]),
                "filename": file.filename,
                "job_description": job_description[:200] + "...",
                "result": analysis_result,
                "created_at": datetime.utcnow()
            }
            await db.analysis_history.insert_one(analysis_record)
        
        return analysis_result
    
    finally:
        # Cleanup
        if os.path.exists(file_path):
            os.remove(file_path)

@router.get("/history")
async def get_history(
    db = Depends(get_database), 
    current_user: dict = Depends(get_current_user)
):
    cursor = db.analysis_history.find({"user_id": str(current_user["_id"])}).sort("created_at", -1)
    history = await cursor.to_list(length=100)
    for item in history:
        item["_id"] = str(item["_id"])
    return history

@router.get("/analysis/{analysis_id}")
async def get_analysis_by_id(
    analysis_id: str,
    db = Depends(get_database),
    current_user: dict = Depends(get_current_user)
):
    from bson import ObjectId
    try:
        record = await db.analysis_history.find_one({
            "_id": ObjectId(analysis_id),
            "user_id": str(current_user["_id"])
        })
    except:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    if not record:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    record["_id"] = str(record["_id"])
    return record
