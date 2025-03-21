from sqlalchemy.orm import Session
from cards.database.database import db
from cards.database.models import Blackjack


class BlackjackTableDAO:
    def __init__(self, db_session: Session = None):
        self.db_session = db_session or db.session

    def get_user_by_uuid(self, uuid: str) -> Blackjack | None:
        return self.db_session.query(Blackjack).filter_by(user_uuid=uuid).first()

    def add_user_to_database(self, user: Blackjack) -> None:
        self.db_session.add(user)
        self.db_session.commit()
        return

    def update_coins(self, user_uuid: str, coin_change: int) -> None:
        user_blackjack = self.get_user_by_uuid(user_uuid)
        if user_blackjack:
            user_blackjack.coins += coin_change
            self.db_session.add(user_blackjack)
            self.db_session.commit()
            return
