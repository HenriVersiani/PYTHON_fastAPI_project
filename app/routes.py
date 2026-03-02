from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import SessionLocal
from app.schemas import UserCreate, UserResponse, UserUpdate
from app.services import UserService

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return await UserService.create(db, user)

@router.get("/users/search", response_model=List[UserResponse])
async def list_users(db: Session = Depends(get_db)):
    return await UserService.list(db)

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    return await UserService.get_by_id(db, user_id)

@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    return await UserService.update(db, user_id, user_data)

@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    await UserService.delete(db, user_id)
    return {"message": "Deletado com sucesso"}
