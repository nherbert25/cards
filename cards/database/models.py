from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

from flask_login import UserMixin

from cards.database.database import db


class User(db.Model, UserMixin):
    user_uuid = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    def __eq__(self, other):
        if isinstance(other, User):
            return self.user_uuid == other.user_uuid
        return False


class Blackjack(db.Model):
    __tablename__ = "blackjack"

    user_uuid = db.Column(db.String(36), db.ForeignKey('user.user_uuid'), primary_key=True)
    coins = db.Column(db.Integer, nullable=False, default=500)

    def __repr__(self):
        return f"User('{self.user_uuid}', '{self.coins}')"

    def __eq__(self, other):
        if isinstance(other, User):
            return self.user_uuid == other.user_uuid
        return False
