from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

from flask_login import UserMixin

from cards.database.database import db


class User(db.Model, UserMixin):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Blackjack(db.Model, UserMixin):
    __tablename__ = "blackjack"

    userid = db.Column(db.String(36), db.ForeignKey('user.id'), primary_key=True)
    coins = db.Column(db.Integer, nullable=False, default=500)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
