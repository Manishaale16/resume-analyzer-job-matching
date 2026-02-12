from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.services.database import get_database
from app.core.security import verify_password, create_access_token, get_password_hash
from app.models.user import UserCreate, UserOut, Token
from datetime import datetime, timedelta
from app.core.config import settings
import logging

router = APIRouter()

@router.post("/register", response_model=UserOut)
async def register(user_in: UserCreate, db = Depends(get_database)):
    logging.info(f"Registration attempt for: {user_in.email}")
    # Check if user exists
    try:
        existing_user = await db.users.find_one({"email": user_in.email})
    except Exception as e:
        logging.error(f"Database error during registration check: {e}")
        raise HTTPException(status_code=500, detail="Database connection error")
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists"
        )
    
    user_dict = user_in.model_dump()
    password = user_dict.pop("password")
    user_dict["hashed_password"] = get_password_hash(password)
    user_dict["created_at"] = datetime.utcnow()
    user_dict["updated_at"] = datetime.utcnow()
    
    logging.info(f"Inserting new user into database: {user_in.email}")
    try:
        result = await db.users.insert_one(user_dict)
        logging.info(f"User created successfully: {result.inserted_id}")
    except Exception as e:
        logging.error(f"Error inserting user: {e}")
        raise HTTPException(status_code=500, detail="Error creating user")
        
    user_dict["_id"] = str(result.inserted_id)
    return user_dict

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db = Depends(get_database)):
    user = await db.users.find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user["email"], expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
