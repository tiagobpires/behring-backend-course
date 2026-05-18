from factory import db
from datetime import datetime, timezone
from pydantic import BaseModel
from typing import Optional


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(128), unique=True, nullable=False, index=True)
    birthdate = db.Column(db.DateTime)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f"<User {self.username}>"


class UserCreate(BaseModel):
    email: str
    username: str
    birthdate: Optional[datetime]


class UserResponse(UserCreate):
    id: int
    created_at: datetime
