# FastAPI Matchmaking Service

A production-ready matchmaking service that finds compatible matches based on location and preferences.

## Features

- Token-based authentication
- Location-based matching using geodesic distance
- Interest and preference-based scoring
- Configurable search radius
- Async API endpoints
- Proper error handling
- Type-safe with Pydantic models

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
Create a `.env` file with:
```
USER_API_BASE_URL=http://your-api-url
```

3. Run the service:
```bash
uvicorn main:app --reload
```

## API Endpoints

### GET /matches

Get potential matches for the authenticated user.

**Headers:**
- `Authorization: Bearer <token>`

**Query Parameters:**
- `radius_km` (optional): Filter matches within this distance in kilometers

**Response:**
```json
{
  "matches": [
    {
      "userId": "string",
      "name": "string",
      "distance_km": 0.0,
      "commonInterests": ["string"],
      "score": 0.0
    }
  ]
}
```

## Error Handling

The service handles various error scenarios:
- 401: Invalid or missing authorization token
- 502: Upstream service errors
- 500: Internal server errors

## Testing

To test the service, you can use the following curl command:

```bash
curl -X GET "http://localhost:8000/matches?radius_km=50" \
     -H "Authorization: Bearer your-token"
``` 