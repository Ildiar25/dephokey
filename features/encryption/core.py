from cryptography.fernet import Fernet
from pathlib import Path

from shared.logger_setup import main_logger as logger


def load_key() -> bytes | None:
    try:
        # Create key path
        key_path = Path(__file__).parent

        with open(f"{key_path}/key.key", "rb") as key_file:
            key = key_file.read()

    except FileNotFoundError as not_found:
        logger.error(f"{type(not_found).__name__} ::: No se ha encontrado el archivo 'key'.")
    except Exception as unknown:
        logger.error(f"{type(unknown).__name__} ::: Un error inesperado a ocurrido al tratar de abrir el archivo "
                     f"'key'.")

    else:
        return key


def encrypt_data(new_data: str) -> str:
    data_coded = new_data.encode(encoding="utf-8", errors="replace")  # 'Replace' changes character by official '�'
    key = load_key()

    # Prepare encryption module
    try:
        fernet = Fernet(key)

        # Encrypt data
        encrypted_data = fernet.encrypt(data_coded)

        return encrypted_data.decode()

    except TypeError as current_type:
        logger.error(f"{type(current_type).__name__} ::: No se ha podido encriptar el archivo.")
        return data_coded.decode()


def decrypt_data(load_data: str) -> str:
    data_coded = load_data.encode()
    key = load_key()

    # Prepare encryption module
    try:
        fernet = Fernet(key)

        # Decrypt data
        decrypted_data = fernet.decrypt(data_coded)

        return decrypted_data.decode(encoding="utf-8", errors="replace")

    except TypeError as current_type:
        logger.error(f"{type(current_type).__name__} ::: No se ha podido desencriptar el archivo.")
        return data_coded.decode()
