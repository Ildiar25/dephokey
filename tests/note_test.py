from features.models.note import Note
from shared.logger_setup import test_logger


def main():
    new_note = Note("Test01", "Test_example", "user")
    test_logger.info(new_note)


if __name__ == '__main__':
    main()
