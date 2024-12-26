from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from pathlib import Path

DB_BASE_PATH = Path(__file__).parent
LANGUAGE = "sqlite"


# This engine allows to connect SQLAlchemy with a database.
# Official documentation: https://docs.sqlalchemy.org/en/14/core/engines.html
engine = create_engine(f"{LANGUAGE}:///{DB_BASE_PATH}/database/database.db", echo=False)

# WARNING: 'create_engine()' method does not connect directly to database, just defines its motor!

# Session allows interactions with the database.
Session = sessionmaker(bind=engine)
session = Session()


# Base class transform attributes to mapped data and link them to database table.
class Base(DeclarativeBase):
    pass
