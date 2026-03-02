from fastapi import FastAPI
from app.database import engine, Base
from app.routes import router
from app.middleware import SimpleLoggerMiddleware
import app.models

app = FastAPI()
Base.metadata.create_all(bind=engine)

# Add simple middleware
app.add_middleware(SimpleLoggerMiddleware)

app.include_router(router)
