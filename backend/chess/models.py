from . import db
from dataclasses import dataclass
import datetime


@dataclass
class User(db.Model):
    __tablename__ = 'users'

    email: str
    password: str
    created_at: datetime.datetime

    email = db.Column(db.String, unique=True, nullable=False, primary_key=True)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, email, password):
        self.email = email
        self.password = password


@dataclass
class Score(db.Model):
    __tablename__ = 'scores'

    user_email: str
    created_at: datetime.datetime
    score: int
    level: int

    user_email = db.Column(db.String, db.ForeignKey("users.email"), primary_key=True)
    created_at = db.Column(db.DateTime, primary_key=True,
                           index=True, default=datetime.datetime.utcnow)
    score = db.Column(db.Integer, nullable=False, index=True)
    level = db.Column(db.Integer, nullable=False)

    def __init__(self, user_email, score, level):
        self.user_email = user_email
        self.score = score
        self.level = level
