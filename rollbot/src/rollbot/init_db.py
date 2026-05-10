from src.db.models import Base
from src.db.session import engine

Base.metadata.create_all(engine)
