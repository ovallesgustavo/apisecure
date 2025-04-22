# app/core/security.py
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from cryptography.fernet import Fernet
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.session import get_db
from app.db.models import User
from app.utils.redis_utils import is_key_in_redis
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
    return cipher_suite.decrypt(encrypted_data.encode()).decode()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Crea un token JWT con datos encriptados."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})

    # Encripta el email antes de incluirlo en el payload
    if "email" in to_encode:
        to_encode["email"] = encrypt_data(to_encode["email"])

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Obtiene el usuario actual a partir del token JWT.
    Verifica si el token está en la lista negra antes de validar el usuario.
    """
    # Verificar si el token está en la lista negra
    if is_key_in_redis(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has been revoked")

    try:
        # Decodificar el token
        payload = decode_token(token)
        if not payload:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        # Desencriptar el campo 'sub' (email)
        email = decrypt_data(payload.get("sub"))
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return user
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
