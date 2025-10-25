from util.json_parser import get_cards_from_set_code_json
from util.set_getter import *
from util.phasher import convert_image_url_to_phash
from util.db_operations import try_add_card
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from card import Base, Card
import os

DATABASE_URL = "postgresql://postgres:admin@localhost/cards_db"

engine = create_engine(DATABASE_URL, echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

set_code = input("Which set would you like to process?")
fp = f"json_sets/{set_code}.json"

set_list = [p if p != "__name__" else p for p in os.listdir()]
if fp not in set_list:
    get_full_set(set_code)

times = 0
cards = get_cards_from_set_code_json(fp)
for card in cards:
    perceptual_hash = convert_image_url_to_phash(card.image_url)
    new_card = Card(
        name=card.name,
        oracle_id=card.oracle_id,
        phash=perceptual_hash,
        card_set=card.set
    )
    try_add_card(session, new_card)
