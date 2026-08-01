import os

from dotenv import load_dotenv

from src.framework import create_app
from src.dnd5e.engine import Dnd5e

load_dotenv()
SERVICE_HOST = os.getenv('SERVICE_HOST')
SERVICE_PORT = os.getenv('SERVICE_PORT')
SERVICE_URL = f'http://{SERVICE_HOST}:{SERVICE_PORT}'

engine = Dnd5e(SERVICE_URL)
app = create_app(engine)
