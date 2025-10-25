from sqlalchemy import text


def add_card(session, model):
    """
    :param session:
    :param model:
    :return:
    """

    session.add(model)
    session.commit()
    print(f"Added card: {model}")


def try_add_card(session, model):
    try:
        add_card(session, model)
    except Exception as e:
        print(e)
        pass


def find_similar_card(session, target_phash):
    """Find the most similar card by perceptual hash."""

    query = text("""
        SELECT name, card_set, phash, id,
               bit_count(
                   ('x' || encode(phash, 'hex'))::bit(128) # ('x' || encode(:target_phash, 'hex'))::bit(128)
               ) AS hamming_distance
        FROM cards
        ORDER BY hamming_distance ASC
        LIMIT 1;
    """)

    result = session.execute(query, {"target_phash": target_phash}).fetchone()

    if result and result.hamming_distance < 100:
        print(f"🔹 Best Match: {result.name} from {result.card_set} (Hamming Distance: {result.hamming_distance})")
        return result


def find_similar_name(session, query_name):
    """string matching based on OCR characters"""

    query = text("""
        CREATE EXTENSION IF NOT EXISTS fuzzystrmatch;
        
        SELECT *
        FROM cards 
        ORDER BY LEVENSHTEIN(name, :query_name) ASC
        LIMIT 1
        """)

    result = session.execute(query, {"query_name": query_name}).fetchone()

    if result:
        print(f"🔹 Best Match: {result.name} from {result.card_set}")
        return result
