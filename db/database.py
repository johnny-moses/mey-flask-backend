from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

engine = create_engine(f"mysql+pymysql://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}"
                       f"@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}/{os.getenv('MYSQL_DATABASE')}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """
    Creates and yields a new database session, and closes it after use.
    """
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()


class DatabaseSession:
    def __init__(self):
        """
        Initializes a new DatabaseSession instance with a new session.
        """
        self.session = SessionLocal()

    def __enter__(self):
        """
        Provides the mechanism for context management.
        """
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Handles exiting the context management, by closing the session.
        """
        self.session.close()


db_session = get_db().__next__()
