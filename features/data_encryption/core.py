from pathlib import Path

from cryptography.fernet import Fernet

from shared.logger_setup import main_log as log

# Create KEY path
KEY_PATH = Path(__file__).parent


def __load_key() -> bytes | None:

    # Prepare key for encrypt
    try:
        with open(rf"{KEY_PATH}\key.key", "rb") as key_file:
            key = key_file.read()
        return key

    except FileNotFoundError as not_found:
        log.error(f"{type(not_found).__name__} | No se ha encontrado el archivo 'key': {not_found}")
    except Exception as unknown:
        log.error(
            f"{type(unknown).__name__} | Un error inesperado a ocurrido al tratar de abrir el archivo 'key': {unknown}"
        )


def encrypt_data(new_data: str) -> str:
    data_coded = new_data.encode(encoding="utf-8", errors="replace")  # 'Replace' changes character by official '�'
    key = __load_key()

    # Prepare data_encryption module
    try:
        fernet = Fernet(key)

        # Encrypt data
        encrypted_data = fernet.encrypt(data_coded)
        return encrypted_data.decode()

    except TypeError as current_type:
        log.error(f"{type(current_type).__name__} | No se ha podido encriptar el archivo: {current_type}")
        return data_coded.decode()
    except Exception as unknown:
        log.error(
            f"{type(unknown).__name__} | Un error inesperado ha ocurrido al tratar de encriptar el archivo: {unknown}"
        )
        return data_coded.decode()


def decrypt_data(load_data: str) -> str:
    data_coded = load_data.encode()
    key = __load_key()

    # Prepare data_encryption module
    try:
        fernet = Fernet(key)

        # Decrypt data
        decrypted_data = fernet.decrypt(data_coded)
        return decrypted_data.decode(encoding="utf-8", errors="replace")

    except TypeError as current_type:
        log.error(f"{type(current_type).__name__} | No se ha podido desencriptar el archivo: {current_type}")
        return data_coded.decode()
    except Exception as unknown:
        log.error(
            f"{type(unknown).__name__} | "
            f"Un error inesperado ha ocurrido al tratar de desencriptar el archivo: {unknown}"
        )
        return data_coded.decode()
