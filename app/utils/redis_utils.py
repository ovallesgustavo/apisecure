# app/utils/redis_utils.py
from datetime import timedelta

import redis

from app.core.config import settings

redis_client = redis.StrictRedis(
    host=settings.redis_host,
    port=settings.redis_port,
    password=settings.redis_password,
    decode_responses=settings.redis_decode_responses,
)


def add_to_redis(key: str, value: str, expiration: timedelta):
    """
    Agrega un valor a Redis con un tiempo de expiración.
    """
    redis_client.set(key, value, ex=int(expiration.total_seconds()))


def get_from_redis(key: str):
    """Obtiene un valor de Redis."""
    return redis_client.get(key)


def delete_from_redis(key: str):
    """Elimina un valor de Redis."""
    redis_client.delete(key)


def is_key_in_redis(key: str) -> bool:
    """Verifica si una clave existe en Redis."""
    return redis_client.exists(key) == 1
