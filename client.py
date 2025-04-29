import os
from typing import Optional
import httpx
from models import APIResponse
from fastapi import HTTPException

class UserDataClient:
    def __init__(self):
        self.base_url = os.getenv("USER_API_BASE_URL", "http://localhost:8000")
        self.client = httpx.AsyncClient()

    async def get_user_data(self, token: str) -> APIResponse:
        headers = {"Authorization": f"Bearer {token}"}
        try:
            response = await self.client.get(
                f"{self.base_url}/api/v1/users/llm-users-details",
                headers=headers
            )
            response.raise_for_status()
            return APIResponse(**response.json())
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise HTTPException(status_code=401, detail="Invalid or expired token")
            raise HTTPException(status_code=502, detail="Error fetching user data from upstream service")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def close(self):
        await self.client.aclose() 