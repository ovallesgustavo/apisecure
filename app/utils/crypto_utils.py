# app/utils/crypto_utils.py
from cryptography.fernet import Fernet
from app.core.config import settings

# Clave de encriptación para el email
cipher_suite = Fernet(settings.encryption_key.encode())


def encrypt_data(data: str) -> str:
    """Encripta datos usando Fernet."""
    return cipher_suite.encrypt(data.encode()).decode()


def decrypt_data(encrypted_data: str) -> str:
    """Desencripta datos usando Fernet."""
    return cipher_suite.decrypt(encrypted_data.encode()).decode()
