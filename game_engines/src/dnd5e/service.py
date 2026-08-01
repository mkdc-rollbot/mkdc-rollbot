from src.framework import create_app
from src.dnd5e.engine import Dnd5e

engine = Dnd5e()
app = create_app(engine)
