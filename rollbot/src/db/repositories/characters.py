from db.models import Character

def get_channel(session, character_id):
    return session.get(Character, character_id)
