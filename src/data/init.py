import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()


def get_db_connection():
    return '{}://{}:{}@{}:{}/{}'.format(
        os.getenv('DB_ENGINE'),
        os.getenv('DB_HOST'),
        os.getenv('DB_PORT'),
        os.getenv('DB_USER'),
        os.getenv('DB_PASSWORD'),
        os.getenv('DB_NAME')
    )


Base = declarative_base()
# Создание движка
CONNECTION_STRING = get_db_connection()
engine = create_engine(CONNECTION_STRING)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def init():
    with Session() as session:
        session.execute(text("""
            CREATE TABLE IF NOT EXISTS creature (
                name VARCHAR(255),
                description VARCHAR(255),
                country VARCHAR(255),
                area VARCHAR(255),
                aka VARCHAR(255)
            )
        """))


init()
