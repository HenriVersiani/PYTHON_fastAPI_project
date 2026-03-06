from app.repository import UserRepository

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
