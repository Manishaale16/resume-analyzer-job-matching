from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, resumes, jobs, users
from app.core.config import settings
import time

from contextlib import asynccontextmanager
from app.services.database import connect_to_mongo, close_mongo_connection, get_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()

app = FastAPI(
    title="SmartResume AI API",
    description="Backend for AI-Powered Resume Analysis & Job Matching",
    version="1.0.0",
    lifespan=lifespan
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    print(f"Incoming request: {request.method} {request.url}")
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Request finished: {request.method} {request.url} - Status: {response.status_code} - Time: {process_time:.4f}s")
    return response

# Set up CORS
origins = settings.ALLOWED_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(resumes.router, prefix="/api/resumes", tags=["Resumes"])
app.include_router(jobs.router, prefix="/api/jobs", tags=["Jobs"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])

@app.get("/api/health")
async def health_check(db = Depends(get_database)):
    try:
        if db is None:
            return {"status": "unhealthy", "database": "disconnected", "error": "Database object is None"}
        # Ping with short timeout
        import asyncio
        await asyncio.wait_for(db.command('ping'), timeout=2.0)
        return {
            "status": "healthy",
            "database": "connected",
            "message": "Connected to MongoDB Atlas"
        }
    except asyncio.TimeoutError:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": "MongoDB connection timed out (2s)"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }

@app.get("/")
async def root():
    return {"message": "Welcome to SmartResume AI API"}
