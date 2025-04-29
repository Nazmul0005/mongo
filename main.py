from fastapi import FastAPI, Depends, HTTPException, Header
from typing import Optional
from models import MatchesResponse
from client import UserDataClient
from matching import Matchmaker
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Matchmaking Service",
    description="A service for finding compatible matches based on location and preferences",
    version="1.0.0"
)

# Dependency to get the authorization token
async def get_token(authorization: str = Header(...)) -> str:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header format")
    return authorization.split(" ")[1]

@app.on_event("startup")
async def startup_event():
    app.state.client = UserDataClient()

@app.on_event("shutdown")
async def shutdown_event():
    await app.state.client.close()

@app.get("/matches", response_model=MatchesResponse)
async def get_matches(
    token: str = Depends(get_token),
    radius_km: Optional[float] = None
):
    """
    Get potential matches for the authenticated user.
    
    - **radius_km**: Optional filter to only show matches within this distance in kilometers
    """
    try:
        # Get user data from external API
        user_data = await app.state.client.get_user_data(token)
        
        # Initialize matchmaker with optional radius filter
        matchmaker = Matchmaker(radius_km=radius_km)
        
        # Find matches
        matches = matchmaker.find_matches(
            user_data.data.myData,
            user_data.data.usersData
        )
        
        return MatchesResponse(matches=matches)
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 