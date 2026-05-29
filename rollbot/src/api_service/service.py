import logging
import uvicorn

from contextlib import asynccontextmanager
from fastapi import FastAPI

from models import CharacterPayload, ChannelPayload

from db.session import SessionLocal
from db.models import Channel as ChannelModel
from db.repositories.guilds import get_or_create_guild
from db.repositories.channels import get_or_create_channel, update_channel_settings, get_channel
from db.repositories.characters import create_character as create_character_db
from db.repositories.characters import set_character_to_channel, get_character
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
async def create_character(author_id,
                           name,
                           character_sheet,
                           channel_id
                           ):
    with SessionLocal() as session:
        player_db = get_or_create_player(session, author_id)
        character_db = create_character_db(session, author_id, name, character_sheet)
        self._logger.info(f'Created character for {author}.')
        char_id = character_db.id
        set_character_to_channel(session, char_id, channel_settings.id)
        session.commit()
    return {"status": "OK", "character_id": char_id}




@app.get("/")
async def root():
    return {"status": "OK"}



# Entry Point

if __name__ == '__main__':
    uvicorn.run('service:app',
                reload=True,
                port=11037)
