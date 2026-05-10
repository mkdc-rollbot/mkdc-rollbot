from src.db.models import Character

def get_character(session, character_id):
    return session.get(Character, character_id)

def create_character(session, player_id, name,  sheet_data: dict):
    character = Character(
            player_id=player_id,
            name=name,
            sheet_data=sheet_data
            )
    
    session.add(character)
    session.commit()
    return character
