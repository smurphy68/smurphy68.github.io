from sqlalchemy import Column, Integer, String, LargeBinary, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, autoincrement=True)
    oracle_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    card_set = Column(String, nullable=False)
    phash = Column(LargeBinary, nullable=False)

    __table_args__ = (UniqueConstraint("name", "card_set", name="uq_card_name_set"),)

    def __repr__(self):
        return f"<Card(name={self.name}, guid={self.oracle_id}, phash={self.phash})>"


class CardModel:
    def __init__(self, name, oracle_id, card_set, image_url):
        self.oracle_id = oracle_id
        self.name = name
        self.set = card_set
        self.image_url = image_url
        self.phash = None

