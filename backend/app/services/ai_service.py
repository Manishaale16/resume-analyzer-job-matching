import spacy
import re
import json
import os
from PyPDF2 import PdfReader
import docx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from app.core.config import settings
from openai import AsyncOpenAI

class AIService:
    def __init__(self):
        try:
            self.nlp = spacy.load(settings.SPACY_MODEL)
        except:
            self.nlp = None
        
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    def extract_text_from_pdf(self, file_path):
        text = ""
        with open(file_path, "rb") as f:
            reader = PdfReader(f)
            for page in reader.pages:
                text += page.extract_text()
        return text

    def extract_text_from_docx(self, file_path):
        doc = docx.Document(file_path)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text

    def clean_text(self, text):
        text = re.sub(r'[^a-zA-Z0-9\s#+]', '', text) 
        text = re.sub(r'\s+', ' ', text).strip().lower()
        return text

    async def analyze_resume_llm(self, resume_text, job_desc_text):
        if not os.getenv("OPENAI_API_KEY"):
            # Fallback to local analysis if no API key
            return self.analyze_resume(resume_text, job_desc_text)

        prompt = f"""
        Act as an expert technical recruiter and ATS systems analyst. 
        Analyze the following resume against the job description.
        
        RESUME:
        {resume_text[:4000]}
        
        JOB DESCRIPTION:
        {job_desc_text[:2000]}
        
        Provide a detailed analysis in JSON format with these exact keys:
        - overall_match: (0-100 score)
        - skill_match_score: (0-100 score)
        - experience_score: (0-100 score)
        - resume_exp: (detected years of experience)
        - required_exp: (required years if detectable, else 0)
        - matched_skills: [list of key technical skills found in both]
        - missing_skills: [list of critical skills in job desc but missing in resume]
        - suggestions: [list of 3 actionable improvement tips]
        """
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                response_format={ "type": "json_object" }
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"LLM Error: {e}")
            return self.analyze_resume(resume_text, job_desc_text)

    def extract_experience_years(self, text):
        # Improved regex to capture more formats like "5+ years", "5 years", "five years", "10+ yrs"
        text_lower = text.lower()
        # Convert word numbers to digits for common small numbers
        word_map = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10}
        for word, digit in word_map.items():
            text_lower = text_lower.replace(f"{word} year", f"{digit} year")

        patterns = [
            r'(\d+)\s*\+?\s*years?',
            r'(\d+)\s*\+?\s*yrs?',
            r'(\d+)\s*\+?\s*yoe'
        ]
        years = []
        for pattern in patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                try:
                    val = int(match)
                    if 0 < val < 40: # Sanity check for realistic experience
                        years.append(val)
                except:
                    pass
        
        return max(years) if years else 0

    def extract_skills(self, text):
        # Professional-grade skill database
        skill_db = {
            # Languages
            "python": 3, "javascript": 3, "typescript": 3, "java": 3, "c#": 3, "c++": 3, "go": 3, "rust": 3, "php": 2, "ruby": 2, "swift": 2, "kotlin": 2,
            "html": 1, "css": 1, "sql": 2, "nosql": 2, "bash": 1, "shell": 1,
            
            # Frontend
            "react": 3, "nextjs": 3, "vue": 2, "angular": 2, "svelte": 2, "ember": 1, "jquery": 1,
            "tailwind": 2, "bootstrap": 1, "material ui": 1, "chakra ui": 1, "framer motion": 1,
            "redux": 2, "mobx": 1, "graph ql": 2, "apollo": 1,
            
            # Backend
            "node": 3, "express": 2, "nestjs": 2, "django": 3, "flask": 2, "fastapi": 3,
            "spring boot": 3, "asp.net": 3, "laravel": 2, "ruby on rails": 2,
            
            # Database
            "postgresql": 3, "mysql": 2, "mongodb": 2, "redis": 2, "cassandra": 2, "elasticsearch": 2, "dynamodb": 2, "firebase": 2, "supabase": 2,
            
            # DevOps & Cloud
            "docker": 3, "kubernetes": 3, "jenkins": 2, "github actions": 2, "gitlab ci": 2, "circleci": 2,
            "aws": 3, "azure": 3, "gcp": 3, "terraform": 3, "ansible": 2, "prometheus": 2, "grafana": 2,
            
            # AI/ML
            "tensorflow": 3, "pytorch": 3, "keras": 2, "scikit-learn": 2, "pandas": 2, "numpy": 2,
            "openai": 3, "llm": 3, "nlp": 3, "computer vision": 3, "langchain": 3, "hugging face": 2,
            
            # Methodologies & Tools
            "agile": 1, "scrum": 1, "kanban": 1, "jira": 1, "git": 2, "github": 1, "gitlab": 1,
            "tdd": 2, "bdd": 1, "ci/cd": 2, "microservices": 3, "serverless": 2, "rest api": 2, "soap": 1
        }
        
        extracted = {}
        text_lower = text.lower()
        
        # Helper to check word boundaries
        def has_skill(skill_name, text):
            # Special handling for C++ and C#
            if skill_name in ["c++", "c#"]:
                return skill_name in text
            return re.search(rf'\b{re.escape(skill_name)}\b', text) is not None

        for skill, weight in skill_db.items():
            if has_skill(skill, text_lower):
                extracted[skill] = weight
        
        return extracted

    def calculate_similarity(self, resume_text, job_desc_text):
        try:
            vectorizer = TfidfVectorizer(stop_words='english')
            tfidf_matrix = vectorizer.fit_transform([resume_text, job_desc_text])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
            return float(similarity[0][0])
        except Exception:
            # Fallback simple Jaccard similarity
            set1 = set(resume_text.split())
            set2 = set(job_desc_text.split())
            intersection = len(set1.intersection(set2))
            union = len(set1.union(set2))
            return intersection / union if union > 0 else 0.0

    def analyze_resume(self, resume_text, job_desc_text):
        # 1. Skill Analysis
        resume_skills_dict = self.extract_skills(resume_text)
        job_skills_dict = self.extract_skills(job_desc_text)
        
        # 2. Experience Analysis
        resume_exp = self.extract_experience_years(resume_text)
        job_exp = self.extract_experience_years(job_desc_text)
        if job_exp == 0: job_exp = 3 # Default to 3 years if not found in JD
        
        # 3. Calculate Scores
        # Skill Score
        total_job_weight = sum(job_skills_dict.values())
        matched_weight = sum(weight for skill, weight in job_skills_dict.items() if skill in resume_skills_dict)
        skill_match_score = (matched_weight / total_job_weight * 100) if total_job_weight > 0 else 85
        
        # Experience Score
        exp_score = min(100, (resume_exp / job_exp) * 100)
        
        # Structural/Content Similarity
        structure_score = self.calculate_similarity(resume_text, job_desc_text) * 100 * 1.5 # Boost similarity weight slightly
        structure_score = min(100, structure_score)

        # Weighted Overall Score
        overall_match = (skill_match_score * 0.45) + (exp_score * 0.30) + (structure_score * 0.25)
        
        # Lists
        matched_skills = [s for s in job_skills_dict if s in resume_skills_dict]
        missing_skills = [s for s in job_skills_dict if s not in resume_skills_dict]
        
        # Suggestions Generation (Rule-based)
        suggestions = []
        
        if len(missing_skills) > 0:
            top_missing = sorted(missing_skills, key=lambda x: job_skills_dict[x], reverse=True)[:3]
            suggestions.append(f"Your resume is missing critical keywords found in the job description: {', '.join(top_missing)}. Try to weave these into your experience section.")
            
        if exp_score < 100:
            diff = job_exp - resume_exp
            if diff > 0:
                suggestions.append(f"This role requires ~{job_exp} years of experience, but we detected {resume_exp}. Highlight high-impact projects to compensate for the seniority gap.")
        
        if structure_score < 40:
            suggestions.append("The vocabulary and phrasing in your resume differs significantly from the job description. Try mirroring the terminology used in the job post.")
            
        if len(suggestions) < 3:
            suggestions.append("Quantify your achievements! Use numbers (e.g., 'Improved performance by 20%') to make your bullet points more impactful.")

        return {
            "overall_match": round(overall_match),
            "skill_match_score": round(skill_match_score),
            "experience_score": round(exp_score),
            "resume_exp": resume_exp,
            "required_exp": job_exp,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "suggestions": suggestions
        }

ai_service = AIService()
