from dataclasses import dataclass
from hashlib import sha256
from typing import Optional, Dict, Any

from sqlalchemy import (
    Column,
    Integer,
    String,
)

from app.store.database.sqlalchemy_base import db


@dataclass
class Admin:
    id: int
    email: str
    password: Optional[str] = None

    def check_password(self, password):
        return self.password == sha256(password.encode()).hexdigest()


class AdminModel(db):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True)
    email = Column(String(64), unique=True, index=True, nullable=False)
    password = Column(String(128), nullable=False)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "email": self.email,
            "password": self.password
        }
