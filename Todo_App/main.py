# Import FastAPI framework and Depends for dependency injection
from fastapi import FastAPI, Depends, HTTPException, Path
from starlette import status

from pydantic import BaseModel, Field

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

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool

# Database Dependency Function
# This function creates a database session for each request
def get_db():
    db = SessionLocal()   # Create a new DB session (connection)
    try:
        yield db          # Provide the session to API
    finally:
        db.close()        # Close session after request ends



# Dependency Type (Advanced clean syntax)
# This creates a reusable dependency type
# Instead of writing Depends(get_db) everywhere
db_dependency = Annotated[Session, Depends(get_db)]


# API Endpoint
# GET endpoint to fetch all todos

@app.get("/")
async def welcome():
    return {
        "app": "Todo App",
        "version": "1.0",
        "message": "Welcome to Todo App 🚀",
        "docs": "/docs"
    }
    
@app.get("/todo", status_code= status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Todos).all()

# get request for pull information
@app.get("/todo/{todo_id}", status_code= status.HTTP_200_OK)
async def read_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found")

# post request for create new list
@app.post("/todo/create", status_code= status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_request: TodoRequest):
    todo_model = Todos(**todo_request.model_dump())
    
    db.add(todo_model)
    db.commit()
    
# Put request for update the database
@app.put("/todo/update/{todo_id}", status_code= status.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependency,
                      todo_request: TodoRequest, 
                      todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete
    
    db.add(todo_model)
    db.commit()
    
# Delet
@app.delete("/todo/delete/{todo_id}", status_code= status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.query(Todos).filter(Todos.id == todo_id).delete()
    
    db.commit()