from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models import User


class UserRepository:
	@staticmethod
	async def create(db, user):
		try:
			user_obj = User(name=user.name, email=user.email, role=user.role)
			db.add(user_obj)
			db.commit()
			db.refresh(user_obj)
			return user_obj
		except IntegrityError as e:
			db.rollback()
			if "email" in str(e):
				raise ValueError("Email already exists")
			raise ValueError("Database error: duplicate entry")

	@staticmethod
	async def list(db):
		return User.get_all(db)

	@staticmethod
	async def get_by_id(db, user_id):
		return User.get_by_id(db, user_id)

	@staticmethod
	async def delete(db, user_id):
		return User.delete_by_id(db, user_id)

	@staticmethod
	async def update(db, user_id, user_data):
		try:
			data = user_data.dict(exclude_unset=True)
			return User.update_by_id(db, user_id, data)
		except IntegrityError as e:
			db.rollback()
			if "email" in str(e):
				raise ValueError("Email already exists")
			raise ValueError("Database error: duplicate entry")
