from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from pathlib import Path


# Base class transform attributes to mapped data and link them to database table.
class Base(DeclarativeBase):
    pass

# Prepare test database settings
test_engine = create_engine("sqlite:///:memory:", echo=True)
New_session = sessionmaker(bind=test_engine)
test_session = New_session()

# Create database path
db_path = Path(__file__).parent.joinpath("database")

# Check if directory already exists
if not db_path.is_dir():
    db_path.mkdir()

# Prepare database file
DATABASE_URL = f"sqlite:///{db_path}/database.db"

# This engine allows to connect SQLAlchemy with a database.
# Official documentation: https://docs.sqlalchemy.org/en/14/core/engines.html
engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)
# WARNING: 'create_engine()' method does not connect directly to database, just defines its motor!

# Session allows interactions with the database.
session = Session()
