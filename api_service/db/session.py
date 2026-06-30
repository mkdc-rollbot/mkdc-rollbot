from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from config import settings
from db.models import Base


DATABASE_URL = settings.database_url

engine = create_engine(DATABASE_URL, connect_args={"options": "-csearch_path=public"})
SessionLocal = sessionmaker(bind=engine)
