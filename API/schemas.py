from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str

class User(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True  # Allows Pydantic to work with SQLAlchemy models

# Schema for Cleaned Data
class CleanedData(BaseModel):
    message: str
    timestamp: str
