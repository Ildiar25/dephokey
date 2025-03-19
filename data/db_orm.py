from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Create database path
DB_PATH = Path(__file__).parent.joinpath("database")
DB_FILENAME = "database.db"

# TODO: make a session class from all of this

# Base class transform attributes to mapped data and link them to database table.
class Base(DeclarativeBase):
    pass

# Prepare test database settings
test_engine = create_engine("sqlite:///:memory:", echo=True)
New_session = sessionmaker(bind=test_engine)
test_session = New_session()


# Check if directory already exists
if not DB_PATH.is_dir():
    DB_PATH.mkdir()

# Prepare database file
DATABASE_URL = f"sqlite:///{DB_PATH.joinpath(DB_FILENAME)}"

# This engine allows to connect SQLAlchemy with a database.
# Official documentation: https://docs.sqlalchemy.org/en/14/core/engines.html
engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)
# WARNING: 'create_engine()' method does not connect directly to database, just defines its motor!

# Session allows interactions with the database.
session = Session()
