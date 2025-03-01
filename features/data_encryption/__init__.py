from pathlib import Path
import os
from cryptography.fernet import Fernet

from shared.logger_setup import main_log as log

# Key settings
KEY_PATH = Path(__file__).parent
KEY_FILE = "key.key"


def create_key() -> None:
    new_key = Fernet.generate_key()
    try:
        with open(KEY_PATH.joinpath(KEY_FILE).__str__(), "xb") as key_file:
            key_file.write(new_key)

    except PermissionError as permission:
        log.error(f"{type(permission).__name__} ::: No se disponen de permisos para la creación del archivo 'key'.")
    except FileExistsError as already_exists:
        log.error(f"{type(already_exists).__name__} ::: El archivo 'key' ya existe.")
    except Exception as unknown:
        log.error(f"{type(unknown).__name__} ::: Un error inesperado a ocurrido al tratar de crear el archivo "
                     f"'key'.")


# Check if key already exists:
if KEY_FILE not in os.listdir(KEY_PATH):
    log.info(f"No se ha encontrado {KEY_FILE}. Se procede a su creación...")
    create_key()
