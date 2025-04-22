import binascii
import re
import traceback

from cryptography.fernet import Fernet
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from passlib.context import CryptContext
from pydantic import BaseModel, validator
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.models import User
from app.db.session import get_db
from app.utils.jwt import decode_token

# Configuración de pwd_context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuración de JWT
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

# Clave de encriptación para el email
cipher_suite = Fernet(settings.encryption_key.encode())

oauth2_scheme = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si una contraseña en texto plano coincide con su hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Genera un hash seguro para una contraseña."""
    return pwd_context.hash(password)


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


# Definir los requisitos de la contraseña
PASSWORD_REGEX_UPPERCASE = re.compile(r".*[A-Z].*")  # Al menos una letra mayúscula
PASSWORD_REGEX_LOWERCASE = re.compile(r".*[a-z].*")  # Al menos una letra minúscula
PASSWORD_REGEX_DIGIT = re.compile(r".*\d.*")  # Al menos un número
PASSWORD_REGEX_SPECIAL = re.compile(
    r".*[-.*+/$].*"
)  # Al menos uno de los símbolos permitidos: . * + / - $
PASSWORD_MIN_LENGTH = 9  # Longitud mínima de 9 caracteres


class PasswordValidationModel(BaseModel):
    password: str

    @validator("password")
    def validate_password(cls, value):
        if not PASSWORD_REGEX_UPPERCASE.match(value):
            raise ValueError("La contraseña debe tener al menos una letra mayúscula")
        if not PASSWORD_REGEX_LOWERCASE.match(value):
            raise ValueError("La contraseña debe tener al menos una letra minúscula")
        if not PASSWORD_REGEX_DIGIT.match(value):
            raise ValueError("La contraseña debe tener al menos un número")
        if not PASSWORD_REGEX_SPECIAL.match(value):
            raise ValueError("La contraseña debe tener al menos un símbolo especial")
        if len(value) < PASSWORD_MIN_LENGTH:
            raise ValueError(
                "La contraseña debe tener una longitud mínima de 9 caracteres"
            )
        return value


def get_current_user(
    token_credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    try:
        # Extraer el token real del objeto HTTPAuthorizationCredentials
        token = token_credentials.credentials

        # Decodificar el token
        payload = decode_token(token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )

        try:
            email = payload.get("sub")
        except binascii.Error:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid encrypted data",
            )
        except Exception:
            traceback.print_exc()
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Decryption error"
            )

        # Consultar el usuario en la base de datos
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
            )
        return user

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    except Exception:
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unexpected error"
        )
