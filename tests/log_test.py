from shared.logger import *


def main():
    logger = logging.getLogger(__name__)
    logger.debug("Esto es un mensaje del modo DEBUG.")
    logger.info("Esto es un mensaje del modo INFO.")
    logger.warning("Esto es un mensaje del modo WARNING.")
    logger.error("Esto es un mensaje del modo ERROR.")
    logger.critical("Esto es un mensaje del modo CRITICAL.")


if __name__ == '__main__':
    main()
