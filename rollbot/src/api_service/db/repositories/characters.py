from datetime import datetime

from db.models import Character, ChannelCharacter, CharacterVariant

def get_character(session, character_id):
    return session.get(Character, character_id)

def create_character(session, player_id, name,  character_sheet):
    sheet_data = character_sheet.toJson()
    character = Character(
            player_id=player_id,
            name=name,
            sheet_data=sheet_data
            )

    session.add(character)
    session.commit()
    return character

def set_character_to_channel(session, character_id, channel_id, variant_id=None):
    if not character_id:
        raise ValueError(f'No ID given.')
    character = session.get(Character, character_id)
    if not character:
        raise ValueError(f'No character with id {character_id}')

    variant = None

    if variant_id:
        variant = session.get(CharacterVariant, variant_id)
        if not variant:
            raise ValueError(f'No character variant with id {variant_id}.')
        if variant.character_id != character.id:
            raise ValueError(f'Variant doesn\'t match character.')
    else:
        variant = CharacterVariant(
                character_id=character.id,
                diff_data=dict(),
                )
        session.add(variant)
        session.flush()

    # Delete possible existing connection
    existing = (
        session.query(ChannelCharacter)
        .filter_by(
            channel_id=channel_id,
            player_id=character.player_id,
        )
        .first()
    )

    if existing:
        session.delete(existing)
    
    db_object = ChannelCharacter(
            channel_id=channel_id,
            character_id=character_id,
            player_id=character.player_id,
            variant_id=variant.id,
            joined_at=datetime.utcnow()
            )

    session.add(db_object)
    return db_object
