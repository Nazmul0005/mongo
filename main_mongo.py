from fastapi import FastAPI, HTTPException
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# FastAPI app instance
app = FastAPI(title="User Matching API")

# MongoDB setup
uri = os.getenv("MONGO_URI")
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.kaskette
collection = db.users

# Pydantic models
class UserCreate(BaseModel):
    userName: str
    name: str
    email: str
    age: int
    gender: str
    interests: List[str]

@app.post("/users/")
async def create_user(user: UserCreate):
    existing_user = collection.find_one({"userName": user.userName})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    user_dict = user.model_dump()
    result = collection.insert_one(user_dict)
    return {"id": str(result.inserted_id), "message": "User created successfully"}

@app.get("/users/{username}")
async def get_user(username: str):
    user = collection.find_one({"userName": username})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user["_id"] = str(user["_id"])  # Convert ObjectId to string
    return user

@app.get("/health")
async def check_health():
    try:
        client.admin.command('ping')
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")