import unittest
from sqlalchemy import inspect
from sqlalchemy.orm import Mapped, mapped_column

from data.db_orm import Base, test_engine, test_session

from shared.logger_setup import test_logger as logger

##### NOTE: It can't be implemented 'deleting' tests because unittest does not run tests in order.

class TableBuilder(Base):
    __tablename__ = "test_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    def __init__(self) -> None:
        super().__init__()
        self.id: int = 1
        self.name: str = "Test01"

    def with_id(self, new_id: int) -> "TableBuilder":
        self.id = new_id
        return self

    def with_name(self, new_name: str) -> "TableBuilder":
        self.name = new_name
        return self

    def build(self) -> "TableBuilder":
        return self

    def __repr__(self) -> str:
        return f"(id: {repr(self.id)}, name: {repr(self.name)})"


class TestDatabase(unittest.TestCase):
    def setUp(self):
        logger.info("Preparing DATATABLE...")

        # Create table
        Base.metadata.create_all(bind=test_engine)

        # Helps to get info
        self.inspector = inspect(test_engine)

        logger.info("DATATABLE ready for test...")

    def tearDown(self):
        test_session.close()

    def test_tableExists(self) -> None:
        self.assertTrue(self.inspector.has_table("test_table"), msg="Test table doesn't exists.")
        logger.info(">>> Confirm if TEST TABLE exists...   OK")

    def test_tableAddElement(self) -> None:
        element = TableBuilder().build()

        # Add one element
        test_session.add(element)
        test_session.commit()

        self.assertTrue(test_session.query(TableBuilder).filter_by(id=1).first(), msg="Test table DOESN'T HAVE id=1")
        logger.info(">>> Confirm if TEST TABLE has ID 1.")

    def test_tableAddMultipleElements(self) -> None:
        element02 = TableBuilder().with_id(2).build()
        element03 = TableBuilder().with_id(3).with_name("Test02").build()
        element04 = TableBuilder().with_id(4).build()

        # Add multiple elements
        test_session.add_all([element02, element03, element04])
        test_session.commit()

        self.assertEqual(first=test_session.query(TableBuilder).count(), second=4, msg="Test table DOESN'T HAVE 4 "
                                                                                       "rows.")
        logger.info(">>> Confirm if TEST TABLE has 4 ROWS.")

    def test_tableQueryFirstElement(self) -> None:

        # One element request (first)
        element = test_session.query(TableBuilder).order_by(TableBuilder.id).first()

        self.log_query_result(element)
        self.assertIsInstance(element, TableBuilder, msg="Test table DOESN'T FIND first element.")
        logger.info(">>> Confirm if TEST TABLE returns first element.")

    def test_tableQuerySpecificElement(self) -> None:

        # One specific element request
        element = test_session.query(TableBuilder).filter_by(id=3).first()

        self.log_query_result(element)
        self.assertEqual(first=element.name, second="Test02", msg="Test table DOESN'T FIND element with id=3.")
        logger.info(">>> Confirm if TEST TABLE return specific element.")

    def test_tableQueryMultipleElements(self) -> None:

        # Multiple elements request
        elements = test_session.query(TableBuilder).all()

        self.log_query_result(elements)
        self.assertEqual(first=len(elements), second=4, msg="Test table DOESN'T HAVE 4 rows (all elements).")
        logger.info(">>> Confirm if TEST TABLE return all elements.")

    def test_tableQuerySpecificMultipleElements(self) -> None:

        # Multiple specific elements request
        elements = test_session.query(TableBuilder).filter_by(name="Test01").all()

        self.log_query_result(elements)
        self.assertEqual(first=len(elements), second=3,
                         msg="Test table DOESN'T HAVE specific elements with name=Test02.")
        logger.info(">>> Confirm if TEST TABLE return filtered multiple elements.")

    @staticmethod
    def log_query_result(result: TableBuilder | list[TableBuilder]) -> None:
        logger.debug(result)


if __name__ == "__main__":
    unittest.main()
