from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Create base class for declarative models
Base = declarative_base()

def get_database_url():
    """Get database URL from environment variables or use default"""
    host = os.getenv('DB_HOST', 'localhost')
    port = os.getenv('DB_PORT', '5432')
    name = os.getenv('DB_NAME', 'myapp')
    user = os.getenv('DB_USER', 'user')
    password = os.getenv('DB_PASSWORD', '')
    
    return f"postgresql://{user}:{password}@{host}:{port}/{name}"

# Create database engine
engine = create_engine(get_database_url())

# Create sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
