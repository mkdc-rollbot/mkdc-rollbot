import logging

from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.db.session import SessionLocal
from src.db.models import Channel as ChannelModel
from src.db.repositories.guilds import get_or_create_guild
from src.db.repositories.channels import get_or_create_channel, update_channel_settings, get_channel
from src.db.repositories.characters import create_character as create_character_db
from src.db.repositories.characters import set_character_to_channel, get_character
from src.db.repositories.players import get_or_create_player


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


@app.get("/")
async def root():
    return {"status": "OK"}


app = FastAPI(lifespan=lifespan)
