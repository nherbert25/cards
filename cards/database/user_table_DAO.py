from cards.database.models import User
from sqlalchemy.orm import Session
from flask_bcrypt import check_password_hash


class UserTableDAO:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_user_by_username(self, username: str):
        return self.db_session.query(User).filter_by(username=username).first()

    def get_user_by_email(self, email: str):
        return self.db_session.query(User).filter_by(email=email).first()

    def verify_password(self, user: User, password: str) -> bool:
        return check_password_hash(user.password, password)

    def add_user_to_database(self, user: User):
        self.db_session.add(user)
        self.db_session.commit()
        return
