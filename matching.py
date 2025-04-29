from typing import List, Optional
from geopy.distance import geodesic
from models import UserProfile, Match

class Matchmaker:
    def __init__(self, radius_km: Optional[float] = None):
        self.radius_km = radius_km

    def calculate_distance(self, user1: UserProfile, user2: UserProfile) -> Optional[float]:
        if not all([user1.latitude, user1.longitude, user2.latitude, user2.longitude]):
            return None
        
        coords1 = (user1.latitude, user1.longitude)
        coords2 = (user2.latitude, user2.longitude)
        return geodesic(coords1, coords2).kilometers

    def get_common_interests(self, user1: UserProfile, user2: UserProfile) -> List[str]:
        interests1 = set([user1.interestedIn]) if user1.interestedIn else set()
        interests2 = set([user2.interestedIn]) if user2.interestedIn else set()
        return list(interests1.intersection(interests2))

    def calculate_match_score(self, user1: UserProfile, user2: UserProfile, distance: float) -> float:
        # Base score components
        distance_score = max(0, 1 - (distance / 100)) if distance else 0  # Normalize distance to 0-1
        interest_score = 1.0 if self.get_common_interests(user1, user2) else 0.0
        
        # Gender preference matching
        gender_score = 0.0
        if user1.interestedIn and user2.gender:
            if user1.interestedIn == "BOTH":
                gender_score = 1.0
            elif user1.interestedIn == "GIRLS" and user2.gender == "FEMALE":
                gender_score = 1.0
            elif user1.interestedIn == "BOYS" and user2.gender == "MALE":
                gender_score = 1.0

        # Weighted sum of scores
        return (distance_score * 0.4 + interest_score * 0.3 + gender_score * 0.3) * 100

    def find_matches(self, my_profile: UserProfile, candidates: List[UserProfile]) -> List[Match]:
        matches = []
        
        for candidate in candidates:
            # Skip self
            if candidate.id == my_profile.id:
                continue
                
            # Calculate distance
            distance = self.calculate_distance(my_profile, candidate)
            if distance is None:
                continue
                
            # Apply radius filter if specified
            if self.radius_km and distance > self.radius_km:
                continue
                
            # Calculate match score
            score = self.calculate_match_score(my_profile, candidate, distance)
            
            # Create match object
            match = Match(
                userId=candidate.id,
                name=candidate.name,
                distance_km=distance,
                commonInterests=self.get_common_interests(my_profile, candidate),
                score=score
            )
            matches.append(match)
        
        # Sort matches by score in descending order
        return sorted(matches, key=lambda x: x.score, reverse=True) 