import logging
import uvicorn

from contextlib import asynccontextmanager
from fastapi import FastAPI

from models import CharacterPayload, ChannelPayload, ChannelSettingsPayload

from db.session import SessionLocal
from db.models import Channel as ChannelModel
from db.repositories.guilds import get_or_create_guild
from db.repositories.channels import get_or_create_channel, update_channel_settings, get_channel
from db.repositories.characters import create_character as create_character_db
from db.repositories.characters import set_character_to_channel, get_character, get_channel_characters, delete_character
from db.repositories.players import get_or_create_player


def initialize_logger():
    logger = logging.getLogger('API_gate')
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s : %(name)s : %(message)s')

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    # On Load
    logger = initialize_logger()
    app.state.logger = logger
    app.state.logger.info('RollBot API Gate live.')
    yield
    # On Teardown

app = FastAPI(lifespan=lifespan)


@app.post("/channel/")
async def create_guild_and_channel(channel_payload: ChannelPayload):
    guild_id = channel_payload.guild_id
    channel_id = channel_payload.channel_id
    app.state.logger.info(f'Validating {channel_id} in {guild_id}')
    with SessionLocal() as session:
        guild = get_or_create_guild(session, guild_id)
        channel = get_or_create_channel(session, guild_id, channel_id)
        channel_data = {
                'channel_id': channel.id,
                'guild_id': channel.guild_id,
                'system': channel.system,
                'prefix': channel.prefix
                }
        session.commit()
    return channel_data

@app.post("/character/")
async def create_character(character_payload: CharacterPayload):
    author_id = character_payload.author_id
    name = character_payload.name
    character_sheet = character_payload.character_sheet
    channel_id = character_payload.channel_id
    app.state.logger.info(f'Creating character: {name}')
    with SessionLocal() as session:
        player_db = get_or_create_player(session, author_id)
        character_db = create_character_db(session, author_id, name, character_sheet)
        session.commit()
        app.state.logger.info(f'Created character for {author_id}.')
        char_id = character_db.id
        set_character_to_channel(session, char_id, channel_id)
        app.state.logger.info(f'Connected character to channel')
        session.commit()
    return {"status": "OK", "character_id": char_id}


@app.put("/channel/")
async def update_channel(channel_payload: ChannelSettingsPayload):
    channel_id = channel_payload.channel_id
    prefix = channel_payload.prefix
    system = channel_payload.system
    app.state.logger.info(f'Changing settings in {channel_id} to prefix {prefix} and/or system {system}') 
    with SessionLocal() as session:
        update_channel_settings(session, channel_id, prefix, system)
        session.commit()
    return {}


@app.get("/characters/{channel_id}")
async def get_characters(channel_id: str):
    with SessionLocal() as session:
        db_characters = get_channel_characters(session, channel_id)
        characters = [{"id": character.id, "player": character.player.id, "name": character.name, "sheet_data": character.sheet_data} for character in db_characters]
    app.state.logger.info(characters)
    return characters


@app.get("/guilds")
async def get_guilds():
    with SessionLocal() as session:
        guilds = session.query(GuildModel).all()

        return [
            {
                "id": guild.id,
                "channels": len(guild.channels)
            }
            for guild in guilds
        ]

@app.get("/channels")
async def get_channels():
    with SessionLocal() as session:
        channels = session.query(ChannelModel).all()

        return [
            {
                "id": channel.id,
                "guild_id": channel.guild_id,
                "prefix": channel.prefix,
                "system": channel.system,
                "character_count": len(channel.channel_characters)
            }
            for channel in channels
        ]

@app.get("/channel/{channel_id}")
async def get_channel_data(channel_id: str):
    with SessionLocal() as session:
        channel = get_channel(session, channel_id)

        if channel is None:
            return {}

        return {
            "id": channel.id,
            "guild_id": channel.guild_id,
            "prefix": channel.prefix,
            "system": channel.system,
            "characters": [
                {
                    "id": link.character.id,
                    "name": link.character.name,
                    "player_id": link.player_id
                }
                for link in channel.channel_characters
            ]
        }

@app.get("/character/{character_id}")
async def get_character_data(character_id: int):
    with SessionLocal() as session:
        character = get_character(session, character_id)

        if character is None:
            return {}

        return {
            "id": character.id,
            "player_id": character.player_id,
            "name": character.name,
            "system": character.system,
            "sheet_data": character.sheet_data,
            "channels": [
                link.channel_id
                for link in character.channel_links
            ]
        }

@app.delete("/character/{character_id}")
async def delete_character_endpoint(character_id: int):
    with SessionLocal() as session:
        success = delete_character(session, character_id)

        if success:
            session.commit()

        return {
            "deleted": success
        }

@app.get("/health")
async def health():
    return {
        "status": "OK"
    }

@app.get("/")
async def root():
    return {"status": "OK"}



# Entry Point

if __name__ == '__main__':
    uvicorn.run('service:app',
                reload=True,
                port=11037)
