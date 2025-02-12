from pathlib import Path
import os
from cryptography.fernet import Fernet

from shared.logger_setup import main_logger as logger


def create_key() -> None:
    new_key = Fernet.generate_key()
    try:
        with open(f"{key_path}/key.key", "xb") as key_file:
            key_file.write(new_key)

    except PermissionError as permission:
        logger.error(f"{type(permission).__name__} ::: No se disponen de permisos para la creación del archivo 'key'.")
    except FileExistsError as already_exists:
        logger.error(f"{type(already_exists).__name__} ::: El archivo 'key' ya existe.")
    except Exception as unknown:
        logger.error(f"{type(unknown).__name__} ::: Un error inesperado a ocurrido al tratar de crear el archivo "
                     f"'key'.")


# Create key path
key_path = Path(__file__).parent


# Check if key already exists:
if "key.key" not in os.listdir(key_path):
    create_key()
