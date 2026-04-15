from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import SessionLocal
from app.schemas import UserCreate, UserResponse, UserUpdate, LoginRequest, TokenResponse
from app.services import UserService
from app.context import require_admin, require_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login", response_model=TokenResponse)
async def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    try:
        result = await UserService.login(db, credentials.email, credentials.password)
        return result
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return await UserService.create(db, user)
    except ValueError as e:
        error_msg = str(e)
        if "Password" in error_msg or "password" in error_msg:
            raise HTTPException(status_code=400, detail=error_msg)
        raise HTTPException(status_code=400, detail=error_msg)

@router.get("/users/search", response_model=List[UserResponse])
async def list_users(db: Session = Depends(get_db), user: dict = Depends(require_admin)):
    print(f"Usuários listados por: {user['email']} (ID: {user['user_id']})")
    return await UserService.list(db)

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db), user: dict = Depends(require_admin)):
    print(f"Usuário {user_id} acessado por: {user['email']} (ID: {user['user_id']})")
    try:
        return await UserService.get_by_id(db, user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db), user: dict = Depends(require_admin)):
    print(f"Usuário {user_id} atualizado por: {user['email']} (ID: {user['user_id']})")
    try:
        return await UserService.update(db, user_id, user_data)
    except ValueError as e:
        error_msg = str(e)
        if "Email already exists" in error_msg:
            raise HTTPException(status_code=400, detail=error_msg)
        raise HTTPException(status_code=404, detail=error_msg)

@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db), user: dict = Depends(require_admin)):
    print(f"Usuário {user_id} deletado por: {user['email']} (ID: {user['user_id']})")
    try:
        await UserService.delete(db, user_id)
        return {"message": "Deletado com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

