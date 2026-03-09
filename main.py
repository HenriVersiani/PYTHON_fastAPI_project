from fastapi import FastAPI
from app.database import engine, Base
from app.routes import router
from app.middleware import SimpleMiddleware
import app.models

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.add_middleware(SimpleMiddleware)

app.include_router(router)
