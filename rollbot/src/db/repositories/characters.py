from datetime.datetime import now

from src.db.models import Character, ChannelCharacter

def get_character(session, character_id):
    return session.get(Character, character_id)

def create_character(session, player_id, name,  sheet_data: dict):
    character = Character(
            player_id=player_id,
            name=name,
            sheet_data=sheet_data
            )
    
    session.add(character)
    return character

def set_character_to_channel(session, character_id, channel_id):
    character = session.get(Character, character_id)
    if not character:
        raise ValueError f'No character with id {character_id}'

    db_object = ChannelCharacter(
            channel_id=channel_id,
            character_id=character_id,
            player_id=character.player_id,
            joined_at=now()
            )

    session.add(db_object)
    return db_object
