from config import db
from dataclasses import dataclass
from sqlalchemy_utils import UUIDType
import uuid
import datetime


@dataclass
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(UUIDType, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, email, password):
        self.id = uuid.uuid4()
        self.email = email
        self.password = password


@dataclass
class Score(db.Model):
    __tablename__ = 'scores'
    user_id = db.Column(UUIDType, db.ForeignKey("users.id"), primary_key=True)
    created_at = db.Column(db.DateTime, primary_key=True,
                           index=True, default=datetime.datetime.utcnow)
    score = db.Column(db.Integer, nullable=False, index=True)
    level = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id, score, level):
        self.user_id = user_id
        self.score = score
        self.level = level
