from sqlalchemy.orm import Session
from cards.database.database import db
from cards.database.models import User
from cards.app_setup import bcrypt


class UserTableDAO:
    def __init__(self, db_session: Session = None):
        self.db_session = db_session or db.session

    def get_user_by_username(self, username: str) -> User | None:
        return self.db_session.query(User).filter_by(username=username).first()

    def get_user_by_email(self, email: str) -> User | None:
        return self.db_session.query(User).filter_by(email=email).first()

    def add_user_to_database(self, user: User) -> None:
        self.db_session.add(user)
        self.db_session.commit()
        return

    @staticmethod
    def verify_password(pw_hash: str, password: str) -> bool:
        return bcrypt.check_password_hash(pw_hash, password)
