import logging
import uvicorn

from contextlib import asynccontextmanager
from fastapi import FastAPI

from registry import Registry, EngineRegistration
from models import EnginePayload

def initialize_logger():
    logger = logging.getLogger('Game Engine Registry')
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

    app.state.registry = Registry()
    logger.info('Created engines registry')

    logger.info('Registry live.')
    yield
    # On Teardown
    logger.info('Shutting down.')

app = FastAPI(lifespan=lifespan)


@app.post("/registry/register")
async def register_engine(engine_payload: EnginePayload):
    registration = EngineRegistration(engine_payload.ruleset, engine_payload.url, True)
    app.state.registry.register(registration)
    app.state.logger.info(f'Registered {engine_payload.ruleset} to url {engine_payload.url}')
    return {"registered": True}


@app.get("/registry/{engine_key}")
async def get_engine(engine_key: str):
    engine = app.state.registry.resolve(engine_key)
    return engine


@app.get("/health")
async def health():
    return {
        "status": "OK"
    }

@app.get("/")
async def root():
    return {"status": "OK"}
