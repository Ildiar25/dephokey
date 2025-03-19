from pathlib import Path

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from shared.logger_setup import main_log, test_log

# Create database settings
DB_PATH = Path(__file__).parent.joinpath("database")
DB_FILENAME = "database.db"
DB_TEST_PATH = Path(":memory:")


class DatabaseManager:
    """
    Official documentation: https://docs.sqlalchemy.org/en/14/core/engines.html
    This class allows to handle a database with different settings.
    """

    def __init__(self, db_path: Path, db_filename: str | None = None, language: str = "sqlite") -> None:
        """
        Initialize a DatabaseManager instance.
        :param db_path: Path | Database's directory
        :param db_filename: str | The file's name
        :param language: str | Database language (sqlite by default)
        :return: None
        """

        # Create main attributes
        self.db_path = db_path
        self.db_filename = "" if db_filename is None else db_filename

        # Update database URL
        self.DB_URL: str = f"{language}:///{self.db_path.joinpath(self.db_filename)}"

        # Create database attributes
        self.engine: Engine | None = None

    def __set_up_test_engine(self) -> None:
        # This engine allows to connect SQLAlchemy with a database.
        if self.engine is None:
            self.engine = create_engine(self.DB_URL, echo=True)
            return

        test_log.warning(f"No se ha podido crear el engine para {self.DB_URL}.")

    def __set_up_main_engine(self) -> None:
        # Check if directory already exists
        if not self.db_path.is_dir():
            self.db_path.mkdir()
            main_log.info(f"Se ha creado el directorio {repr(self.db_path)}")

        # WARNING: 'create_engine()' method does not connect directly to database, just defines its motor!
        if self.engine is None:
            self.engine = create_engine(self.DB_URL, echo=False)
            return

        main_log.warning(f"No se ha podido crear el engine para {self.DB_URL}.")

    def get_main_session(self) -> sessionmaker[Session]:
        if self.engine is None:
            self.__set_up_main_engine()
            main_log.info(f"Preparada la conexión con {repr(self.DB_URL)}")

        return sessionmaker(bind=self.engine)

    def get_test_session(self) -> sessionmaker[Session]:
        if self.engine is None:
            self.__set_up_test_engine()
            test_log.info(f"Preparada la conexión con {repr(self.DB_URL)}")

        return sessionmaker(bind=self.engine)


class Base(DeclarativeBase):
    """This class transform attributes to mapped data and link them to database table."""
    pass

# Those databases allow to get the engine
test_database = DatabaseManager(DB_TEST_PATH)
main_database = DatabaseManager(DB_PATH, DB_FILENAME)

# Those sessions allow to interact with the databases
session = main_database.get_main_session()()
test_session = test_database.get_test_session()()
