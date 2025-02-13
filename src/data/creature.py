from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.utils import get_db_connection


CONNECTION_STRING = get_db_connection()
Base = declarative_base()
# Создание движка
engine = create_engine(CONNECTION_STRING)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
