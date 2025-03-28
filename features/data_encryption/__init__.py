import os
from pathlib import Path

from cryptography.fernet import Fernet

from shared.logger_setup import main_log as log

# Key settings
__KEY_PATH = Path(__file__).parent
__KEY_FILE = "key.key"


def __create_key() -> None:
    new_key = Fernet.generate_key()

    try:
        with open(__KEY_PATH.joinpath(__KEY_FILE).__str__(), "xb") as key_file:
            key_file.write(new_key)
        log.info(f"¡Archivo {repr(__KEY_FILE)} creado!")

    except PermissionError as permission:
        log.error(
            f"{type(permission).__name__} | "
            f"No se disponen de permisos para la creación del archivo {repr(__KEY_FILE)}: {permission}"
        )
    except FileExistsError as already_exists:
        log.error(
            f"{type(already_exists).__name__} | El archivo {repr(__KEY_FILE)} ya existe: {already_exists}"
        )
    except Exception as unknown:
        log.error(
            f"{type(unknown).__name__} | "
            f"Un error inesperado a ocurrido al tratar de crear el archivo {repr(__KEY_FILE)}: {unknown}"
        )


# Check if key already exists:
if __KEY_FILE not in os.listdir(__KEY_PATH):
    log.info(f"No se ha encontrado {repr(__KEY_FILE)}. Se procede a su creación.")
    __create_key()
