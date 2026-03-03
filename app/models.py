from sqlalchemy import Column, Integer, String, select
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

class User(BaseModel):
    __tablename__ = "users"

    name = Column(String)
    email = Column(String, unique=True, index=True)
