from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from API.crud import create_user, get_user, get_users, update_user, delete_user, store_cleaned_data
from API.schemas import User, UserCreate
from API.database import get_db  
from script.scrapping import main  # Updated to match your import
from script.dataCleaning import clean_data
from script.imageDetection import detect_objects

# Initialize FastAPI app
app = FastAPI()

# API endpoint to create a user
@app.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

# API endpoint to get a user by ID
@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# API endpoint to get all users
@app.get("/users/", response_model=list[User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = crud.get_users(db=db, skip=skip, limit=limit)
    return users

# API endpoint to update a user
@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db=db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# API endpoint to delete a user
@app.delete("/users/{user_id}", response_model=User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# API endpoint to scrape data from Telegram
@app.get("/scrape")
async def scrape_data():
    try:
        data = await scrape_channel()  # Updated function name to match import
        return {"message": "Data scraping started", "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")

# API endpoint to clean and store data
@app.post("/clean")
def clean_and_store_data(db: Session = Depends(get_db)):
    raw_data = fetch_raw_data()  # Fetch raw data from your temporary storage (adjust as needed)
    cleaned_data = clean_data(raw_data)
    # Store cleaned data in DB
    crud.store_cleaned_data(db, cleaned_data)
    return {"message": "Data cleaned and stored"}

# API endpoint to detect objects in images
@app.post("/detect_objects")
async def detect_objects(image_path: str):
    detections = detect_objects_in_image(image_path)
    return {"detections": detections}
