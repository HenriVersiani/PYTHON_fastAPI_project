from fastapi import FastAPI
from app.database import engine, Base
from app.routes import router
from app.middleware import SimpleMiddleware
from app.init_db import init_db
import app.models

app = FastAPI()

# Inicializar banco de dados e roles
init_db()

app.add_middleware(SimpleMiddleware)

app.include_router(router)
