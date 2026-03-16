from app.repository import UserRepository
from app.auth import verify_password, create_access_token
from datetime import timedelta

class UserService:
    @staticmethod
    async def create(db, user):
        return await UserRepository.create(db, user)

    @staticmethod
    async def list(db):
        return await UserRepository.list(db)

    @staticmethod
    async def get_by_id(db, user_id):
        user = await UserRepository.get_by_id(db, user_id)
        if not user:
            raise ValueError("User not found")
        return user

    @staticmethod
    async def delete(db, user_id):
        user = await UserRepository.get_by_id(db, user_id)
        if not user:
            raise ValueError("User not found")
        return await UserRepository.delete(db, user_id)

    @staticmethod
    async def update(db, user_id, user_data):
        user = await UserRepository.get_by_id(db, user_id)
        if not user:
            raise ValueError("User not found")
        return await UserRepository.update(db, user_id, user_data)

    @staticmethod
    async def login(db, email: str, password: str):
        user = await UserRepository.get_by_email(db, email)
        if not user:
            raise ValueError("Invalid email or password")
        if not verify_password(password, user.password):
            raise ValueError("Invalid email or password")
        
        # Create JWT token
        access_token_expires = timedelta(minutes=30)
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role
        }
        access_token = create_access_token(data=token_data, expires_delta=access_token_expires)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user
        }
