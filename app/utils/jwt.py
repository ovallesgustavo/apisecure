from datetime import datetime, timedelta

from jose import JWTError, jwt

from app.core.config import settings
from app.utils.crypto_utils import decrypt_data, encrypt_data
from app.utils.redis_utils import (add_to_redis, delete_from_redis,
                                   is_key_in_redis)


def create_access_token(data: dict):
    """
    Crea un token JWT con datos encriptados.
    Encripta el campo 'sub' (email) antes de incluirlo en el payload.
    """
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode = data.copy()
    to_encode.update({"exp": expire})

    # Encriptar el campo 'sub' (email)
    if "sub" in to_encode:
        to_encode["sub"] = encrypt_data(to_encode["sub"])

    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def create_refresh_token(data: dict):
    """
    Crea un refresh token JWT con datos encriptados.
    Almacena el refresh token en Redis con un tiempo de expiración.
    """
    expire = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
    to_encode = data.copy()
    to_encode.update({"exp": expire})

    # Encriptar el campo 'sub' (email)
    if "sub" in to_encode:
        to_encode["sub"] = encrypt_data(to_encode["sub"])

    refresh_token = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )

    # Almacenar el refresh token en Redis con expiración
    add_to_redis(
        refresh_token,
        data["sub"],
        expiration=timedelta(days=settings.refresh_token_expire_days),
    )

    return refresh_token


def is_refresh_token_valid(refresh_token: str):
    """
    Verifica si un refresh token es válido (existe en Redis).
    """
    return is_key_in_redis(refresh_token)


def invalidate_refresh_token(refresh_token: str):
    """
    Invalida un refresh token eliminándolo de Redis.
    """
    delete_from_redis(refresh_token)


def decode_token(token: str):
    """
    Decodifica un token JWT y desencripta el campo 'sub' (email).
    """
    try:
        # Decodificar el token
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )

        # Desencriptar el campo 'sub' (email)
        if "sub" in payload:
            payload["sub"] = decrypt_data(payload["sub"])

        return payload
    except JWTError:
        return None
