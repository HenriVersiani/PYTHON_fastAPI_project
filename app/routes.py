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
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return UserService.create(db, user)

@router.get("/users/search", response_model=List[UserResponse])
def list_users(db: Session = Depends(get_db)):
    return UserService.list(db)

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return UserService.get_by_id(db, user_id)

@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    return UserService.update(db, user_id, user_data)

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    UserService.delete(db, user_id)
    return {"message": "Deletado com sucesso"}
