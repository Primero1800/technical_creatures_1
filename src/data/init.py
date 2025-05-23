import os
import sys

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()


def get_db_connection():
    db_name = os.getenv('DB_NAME_TEST') if 'pytest' in sys.modules else os.getenv('DB_NAME')
    return '{}://{}:{}@{}:{}/{}'.format(
        os.getenv('DB_ENGINE'),
        os.getenv('DB_USER'),
        os.getenv('DB_PASSWORD'),
        os.getenv('DB_HOST'),
        os.getenv('DB_PORT'),
        db_name,
    )


Base = declarative_base()
# Создание движка
CONNECTION_STRING = get_db_connection()
engine = create_engine(CONNECTION_STRING)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def init_creature():
    with Session() as session:
        session.execute(text("""
            CREATE TABLE IF NOT EXISTS creature (
                name VARCHAR(255) primary key,
                description VARCHAR(255),
                country VARCHAR(255),
                area VARCHAR(255),
                aka VARCHAR(255)
            )
        """))
        session.commit()


def init_explorer():
    with Session() as session:
        session.execute(text("""
            CREATE TABLE IF NOT EXISTS explorer (
                name VARCHAR(255) primary key,
                country VARCHAR(255),
                description VARCHAR(255)
            )
        """))
        session.commit()


def init_user():
    with Session() as session:
        session.execute(text("""
            CREATE TABLE IF NOT EXISTS user_active (
                name VARCHAR(255) primary key,
                hash VARCHAR(255)
            )
        """))

        session.execute(text("""
            CREATE TABLE IF NOT EXISTS user_deleted (
                name VARCHAR(255) primary key,
                hash VARCHAR(255)
            )
        """))

        session.commit()


init_creature()
init_explorer()
init_user()
