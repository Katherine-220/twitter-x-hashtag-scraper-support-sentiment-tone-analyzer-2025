from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional

@dataclass
class User:
    type: str
    id: int
    username: str
    name: str
    url: str
    isVerified: bool
    isBlueVerified: bool
    profilePicture: str
    coverPicture: Optional[str]
    description: str
    location: str
    followers: int
    following: int
    favouritesCount: int
    mediaCount: int
    statusesCount: int
    listedCount: int
    protected: bool
    createdAt: datetime

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "url": self.url,
            "isVerified": self.isVerified,
            "isBlueVerified": self.isBlueVerified,
            "profilePicture": self.profilePicture,
            "coverPicture": self.coverPicture,
            "description": self.description,
            "location": self.location,
            "followers": self.followers,
            "following": self.following,
            "favouritesCount": self.favouritesCount,
            "mediaCount": self.mediaCount,
            "statusesCount": self.statusesCount,
            "listedCount": self.listedCount,
            "protected": self.protected,
            "createdAt": self.createdAt.isoformat(),
        }