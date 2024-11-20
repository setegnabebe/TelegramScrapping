from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

# Base class for SQLAlchemy models
Base = declarative_base()

# User model
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

# CleanedData model
class CleanedData(Base):
    __tablename__ = "cleaned_data"
    
    id = Column(Integer, primary_key=True, index=True)
    raw_data = Column(Text, nullable=False)
    cleaned_data = Column(Text, nullable=False)
