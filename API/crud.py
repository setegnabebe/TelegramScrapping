from sqlalchemy.orm import Session
from API.models import User, CleanedData  # Adjusted import for models
from API.schemas import UserCreate, CleanedData as CleanedDataSchema

# Create a new user
def create_user(db: Session, user: UserCreate):
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Get a user by ID
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

# Get all users
def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()

# Update user details
def update_user(db: Session, user_id: int, user: UserCreate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db_user.name = user.name
        db_user.email = user.email
        db.commit()
        db.refresh(db_user)
        return db_user
    return None

# Delete a user
def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return db_user
    return None

# Store cleaned data
def store_cleaned_data(db: Session, cleaned_data: list):
    """
    This function stores cleaned data in the database.
    It assumes the cleaned_data is a list of dictionaries 
    that can be directly passed to the CleanedData model.
    """
    for data in cleaned_data:
        db_data = CleanedData(**data)  # Assuming the CleanedData schema matches the data
        db.add(db_data)
    db.commit()
