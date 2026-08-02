import logging
import os

from contextlib import asynccontextmanager
from src.system_base import RolePlayingSystem
from src.shared.clients.registry import RegistryClient
from src.shared.clients.dice import DiceClient
from src.shared.clients.api import ApiClient
from src.shared.models import EngineRegistrationPayload
from fastapi import FastAPI

def initialize_logger(engine):
    logger = logging.getLogger(f'{engine.key()} Engine')
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s : %(name)s : %(message)s')

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger

def create_lifespan(engine: RolePlayingSystem): 
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # On Load
        logger = initialize_logger(engine)
        app.state.logger = logger
        app.state.logger.info(f'{engine.key()} game engine up')

        reg_client = RegistryClient(os.getenv('REGISTRY_URL'))
        registration = EngineRegistrationPayload(ruleset=engine.key(), url=engine.url)
        response = await reg_client.register(registration)

        app.state.logger.info('Registered!')
        
        api_client = ApiClient(response['api_url'])
        app.state.api_client = api_client

        dice_client = DiceClient(response['data']['dice_roller_url'])
        engine.set_dice_client(dice_client)

        yield
        # On Teardown
        app.state.logger.info('Shutting down.')

    return lifespan

def create_app(engine: RolePlayingSystem):
    app = FastAPI(lifespan=create_lifespan(engine))

    @app.get("/metadata")
    def metadata():
        return engine.metadata()

    app = engine.register_routes(app)
    return app
