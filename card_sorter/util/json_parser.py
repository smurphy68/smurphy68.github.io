from card import CardModel
import json


def _selector(obj):
    return CardModel(
        oracle_id=obj["oracle_id"],
        name=obj["name"],
        card_set=obj["set"],
        image_url=obj["image_uris"]["normal"] # doesnt cater for dual faced cards which will be an issue
    )


def get_cards_from_set_code_json(fp):
    with open(fp, "r", encoding="utf-8") as json_file:
        json_cards = json.load(json_file)
    return [_selector(obj) for obj in json_cards]
