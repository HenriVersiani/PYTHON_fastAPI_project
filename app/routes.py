from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import SessionLocal
from app.schemas import UserCreate, UserResponse, UserUpdate
from app.services import UserService
from app.models import User

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Route-specific dependency middlewares

def validate_user_id(user_id: int):
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid user ID. Must be a positive integer")
    return user_id

def check_user_exists(user_id: int = Depends(validate_user_id), db: Session = Depends(get_db)):
    user = User.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def validate_user_data(user: UserCreate):
    if not user.name or len(user.name.strip()) == 0:
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    if not user.email or len(user.email.strip()) == 0:
        raise HTTPException(status_code=400, detail="Email cannot be empty")
    return user

@router.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate = Depends(validate_user_data), db: Session = Depends(get_db)):
    return await UserService.create(db, user)

@router.get("/users/search", response_model=List[UserResponse])
async def list_users(db: Session = Depends(get_db)):
    return await UserService.list(db)

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user: User = Depends(check_user_exists)):
    return user

@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_data: UserUpdate, user: User = Depends(check_user_exists), db: Session = Depends(get_db)):
    return await UserService.update(db, user.id, user_data)

@router.delete("/users/{user_id}")
async def delete_user(user: User = Depends(check_user_exists), db: Session = Depends(get_db)):
    await UserService.delete(db, user.id)
    return {"message": "Deletado com sucesso"}
