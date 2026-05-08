from src.db.models import Character

def get_character(session, character_id):
    return session.get(Character, character_id)
