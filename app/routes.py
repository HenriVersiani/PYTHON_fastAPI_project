from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List

from app.database import SessionLocal
from app.schemas import UserCreate, UserResponse, UserUpdate
from app.services import UserService
from app.context import get_user_context

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db), request: Request = None):
    context = get_user_context(request)
    
    print(f"✅ Usuário criado por: {context['username']}")
    return await UserService.create(db, user)

@router.get("/users/search", response_model=List[UserResponse])
async def list_users(db: Session = Depends(get_db), request: Request = None):
    context = get_user_context(request)
    
    print(f"✅ Usuários listados por: {context['username']}")
    return await UserService.list(db)

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db), request: Request = None):
    context = get_user_context(request)
    
    print(f"✅ Usuário {user_id} acessado por: {context['username']} (ID: {context['user_id']})")
    try:
        return await UserService.get_by_id(db, user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db), request: Request = None):
    context = get_user_context(request)
    
    print(f"✅ Usuário {user_id} atualizado por: {context['username']}")
    try:
        return await UserService.update(db, user_id, user_data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db), request: Request = None):
    context = get_user_context(request)
    
    print(f"✅ Usuário {user_id} deletado por: {context['username']}")
    try:
        await UserService.delete(db, user_id)
        return {"message": "Deletado com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
