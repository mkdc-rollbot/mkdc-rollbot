from sqlalchemy import create_engine
from sqlaclhemy.orm import sessionmaker

from db.models import Base

DATABASE_URL = "sqlite:///bot.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(engine)
