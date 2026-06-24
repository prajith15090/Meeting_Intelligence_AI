import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import NEON_DATABASE_URL

# Fix URL for sqlalchemy if needed
if NEON_DATABASE_URL and NEON_DATABASE_URL.startswith("postgres://"):
    NEON_DATABASE_URL = NEON_DATABASE_URL.replace("postgres://", "postgresql://", 1)

try:
    engine = create_engine(NEON_DATABASE_URL, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    print(f"Database connection error: {e}")
    engine = None
    SessionLocal = None

def get_db():
    if not SessionLocal:
        yield None
        return
        
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
