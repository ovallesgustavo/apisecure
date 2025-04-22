from cryptography.fernet import Fernet

key = Fernet.generate_key()
print(key.decode())  # Copia esto en tu archivo .env
