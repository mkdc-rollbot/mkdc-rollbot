import logging

from contextlib import asynccontextmanager
from src.system_base import RolePlayingSystem
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
