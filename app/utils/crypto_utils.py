# app/utils/crypto_utils.py
import binascii
import traceback

from cryptography.fernet import Fernet

from app.core.config import settings

# Clave de encriptación para el email
cipher_suite = Fernet(settings.encryption_key.encode())


def encrypt_data(data: str) -> str:
    """Encripta datos usando Fernet."""
    return cipher_suite.encrypt(data.encode()).decode()


def decrypt_data(encrypted_data: str) -> str:
    """Desencripta datos usando Fernet."""
    try:
        # Asegúrate de que encrypted_data sea una cadena válida
        if not encrypted_data or not isinstance(encrypted_data, str):
            raise ValueError("Invalid encrypted data: must be a non-empty string")

        # Intenta desencriptar el dato
        decrypted_data = cipher_suite.decrypt(encrypted_data.encode()).decode()
        return decrypted_data
    except binascii.Error:
        raise ValueError("Invalid encrypted data: incorrect padding")
    except Exception:
        traceback.print_exc()
        raise ValueError("Decryption failed")
