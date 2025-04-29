from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class UserProfile(BaseModel):
    id: str
    userName: str
    name: str
    role: str
    interestedIn: Optional[str] = None
    gender: Optional[str] = None
    dob: Optional[datetime] = None
    images: List[str] = []
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    radius: Optional[float] = None
    address: Optional[str] = None
    bio: Optional[str] = None
    profession: Optional[str] = None
    language: Optional[str] = None

class UserDataResponse(BaseModel):
    myData: UserProfile
    usersData: List[UserProfile]

class APIResponse(BaseModel):
    success: bool
    statusCode: int
    message: str
    data: UserDataResponse

class Match(BaseModel):
    userId: str
    name: str
    distance_km: float
    commonInterests: List[str]
    score: float

class MatchesResponse(BaseModel):
    matches: List[Match] 