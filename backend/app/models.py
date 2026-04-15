from sqlalchemy import Column, Integer, String, select, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)


    @classmethod
    def get_all(cls, db):
        stmt = select(cls)
        return db.scalars(stmt).all()

    @classmethod
    def get_by_id(cls, db, id):
        stmt = select(cls).where(cls.id == id)
        return db.scalars(stmt).first()

    @classmethod
    def delete_by_id(cls, db, id):
        obj = cls.get_by_id(db, id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

    @classmethod
    def update_by_id(cls, db, id, data):
        obj = cls.get_by_id(db, id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.commit()
            db.refresh(obj)
        return obj

class Role(BaseModel):
    __tablename__ = "roles"

    name = Column(String, unique=True, index=True)
    users = relationship("User", back_populates="role")

class User(BaseModel):
    __tablename__ = "users"

    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role_id = Column(Integer, ForeignKey("roles.id"), index=True, default=1)
    role = relationship("Role", back_populates="users")
