from game_engines.framework import create_app
from game_engines.dnd5e.engine import Dnd5e

engine = Dnd5e()
app = create_app(engine)
