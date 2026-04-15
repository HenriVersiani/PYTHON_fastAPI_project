from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routes import router
from app.middleware import SimpleMiddleware
from app.init_db import init_db
import app.models

app = FastAPI()

# Inicializar banco de dados e roles
init_db()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite and npm dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SimpleMiddleware)

app.include_router(router)
