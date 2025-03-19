import os
from pathlib import Path

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
        log.info(f"¡Archivo {repr(KEY_FILE)} creado!")
    except PermissionError as permission:
        log.error(f"{type(permission).__name__} | "
                  f"No se disponen de permisos para la creación del archivo {repr(KEY_FILE)}: {permission}")
    except FileExistsError as already_exists:
        log.error(f"{type(already_exists).__name__} | "
                  f"El archivo {repr(KEY_FILE)} ya existe: {already_exists}")
    except Exception as unknown:
        log.error(f"{type(unknown).__name__} | "
                  f"Un error inesperado a ocurrido al tratar de crear el archivo {repr(KEY_FILE)}: {unknown}")


# Check if key already exists:
if KEY_FILE not in os.listdir(KEY_PATH):
    log.info(f"No se ha encontrado {repr(KEY_FILE)}. Se procede a su creación.")
    create_key()
