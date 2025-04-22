from cryptography.fernet import Fernet


# Clave de encriptación para el email
encryption_key: str = "9B7yFgX-fsSMkSsqk4qcb6id1V4xCCg_ZwffBXCnzgE="


# Clave de encriptación para el email
cipher_suite = Fernet(encryption_key.encode())


def encrypt_data(data: str) -> str:
    """Encripta datos usando Fernet."""
    return cipher_suite.encrypt(data.encode()).decode()


def decrypt_data(encrypted_data: str) -> str:
    """Desencripta datos usando Fernet."""
    return cipher_suite.decrypt(encrypted_data.encode()).decode()


# Prueba de encriptación/desencriptación
original_data = "test@example.com"
encrypted_data = encrypt_data(original_data)
decrypted_data = decrypt_data(encrypted_data)

assert decrypted_data == original_data
print("Prueba exitosa: Los datos coinciden.")
