from factory import db
from datetime import datetime, timezone
from pydantic import BaseModel, ConfigDict
from utils.response_schema import OrmBase, ResponseBase
from typing import Optional
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(128), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256))
    birthdate = db.Column(db.DateTime)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password: str):
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f"<User {self.username}>"


class UserUpdate(BaseModel):
    email: str
    username: str
    birthdate: Optional[datetime]


class UserCreate(UserUpdate):
    password: str


class UserResponse(OrmBase, UserUpdate):
    created_at: datetime


class UserResponseList(ResponseBase):
    users: list[UserResponse]
