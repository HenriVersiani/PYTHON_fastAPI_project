from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import SessionLocal
from app.schemas import UserCreate, UserResponse
from app.services import create_user_service, list_users_service

router = APIRouter()


# Dependência para abrir e fechar sessão automaticamente
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user_service(db, user)


@router.get("/users", response_model=List[UserResponse])
def list_users(db: Session = Depends(get_db)):
    return list_users_service(db)
