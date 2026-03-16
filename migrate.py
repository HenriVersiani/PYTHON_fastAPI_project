"""
Migration script to update the users table schema
Run this once to add the password column to existing tables
"""
from app.database import engine, Base
from app.models import User

# Drop existing tables and recreate with new schema
print("Dropping existing tables...")
Base.metadata.drop_all(bind=engine)

print("Creating tables with new schema...")
Base.metadata.create_all(bind=engine)

print("✓ Database migration complete! Users table now has password column.")
