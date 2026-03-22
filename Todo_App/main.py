"""app + create tables"""

# Import FastAPI framework and Depends for dependency injection
from fastapi import FastAPI, Depends

# Import models file (contains table definitions)
import models

# Import specific table (Todos model)
from models import Todos

# Import database engine and session creator
from database import engine, SessionLocal

# Annotated is used for better type + dependency combination
from typing import Annotated

# Session is the database session type (used for type hinting)
from sqlalchemy.orm import Session


# Create FastAPI application instance
app = FastAPI()


# Create tables in database automatically (if not already created)
# Reads models and creates corresponding tables in DB
models.Base.metadata.create_all(bind=engine)


# -------------------------------
# Database Dependency Function
# -------------------------------

# This function creates a database session for each request
def get_db():
    db = SessionLocal()   # Create a new DB session (connection)
    try:
        yield db          # Provide the session to API
    finally:
        db.close()        # Close session after request ends


# -------------------------------
# Dependency Type (Advanced clean syntax)
# -------------------------------

# This creates a reusable dependency type
# Instead of writing Depends(get_db) everywhere
db_dependency = Annotated[Session, Depends(get_db)]


# -------------------------------
# API Endpoint
# -------------------------------

# GET endpoint to fetch all todos
@app.get("/")
async def read_all(db: db_dependency):
    # db is automatically injected by FastAPI
    
    # Query all records from Todos table
    return db.query(models.Todos).all()