from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import oauth2_scheme, verify_password
from app.db.models import User
from app.db.session import get_db
from app.schemas.token import TokenResponse
from app.schemas.user import UserLogin
from app.utils.jwt import (create_access_token, create_refresh_token,
                           decode_token, invalidate_refresh_token,
                           is_refresh_token_valid)
from app.utils.redis_utils import add_to_redis, is_key_in_redis

router = APIRouter()


@router.post("/login")
def login_user(user_credentials: UserLogin, db: Session = Depends(get_db)):
    # Buscar al usuario en la base de datos
    db_user = db.query(User).filter(User.email == user_credentials.email).first()
    if not db_user or not verify_password(
        user_credentials.password, db_user.hashed_password
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": db_user.email})
    refresh_token = create_refresh_token({"sub": db_user.email})
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/logout")
def logout_user(token_credentials=Depends(oauth2_scheme)):
    try:
        # Extraer el token real del objeto HTTPAuthorizationCredentials
        token = token_credentials.credentials

        # Decodificar el token
        payload = decode_token(token)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Verificar si el token ha expirado
        expiration_time = payload.get("exp", 0) - int(datetime.utcnow().timestamp())
        if expiration_time <= 0:
            raise HTTPException(status_code=401, detail="Token expired")

        # Verificar si el token está revocado
        if is_key_in_redis(token):
            raise HTTPException(status_code=401, detail="Token has been revoked")

        # Agregar el token a la lista negra en Redis
        add_to_redis(
            token, "blacklisted", expiration=timedelta(seconds=expiration_time)
        )

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    return {"message": "Successfully logged out"}


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(refresh_token: str):
    """
    Refresca el access_token usando un refresh_token válido.
    Invalida el refresh_token después de su uso.
    """
    try:
        # Verificar si el refresh_token es válido
        if not is_refresh_token_valid(refresh_token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token",
            )

        # Decodificar el refresh_token para obtener el payload
        payload = decode_token(refresh_token)
        if not payload or "sub" not in payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token payload",
            )

        # Crear un nuevo access_token
        new_access_token = create_access_token({"sub": payload["sub"]})

        # Invalidar el refresh_token usado
        invalidate_refresh_token(refresh_token)

        return {"access_token": new_access_token, "token_type": "bearer"}

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Failed to refresh token"
        )
