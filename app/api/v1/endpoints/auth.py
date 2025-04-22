from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import verify_password
from app.db.models import User
from app.schemas.user import UserLogin
from app.utils.jwt import create_access_token, create_refresh_token, decode_token
from app.utils.redis_utils import is_key_in_redis, add_to_redis
from app.db.session import get_db
from datetime import datetime, timedelta
from app.core.security import oauth2_scheme
import logging


router = APIRouter()


@router.post("/login")
def login_user(user_credentials: UserLogin, db: Session = Depends(get_db)):
    # Buscar al usuario en la base de datos
    db_user = db.query(User).filter(User.email == user_credentials.email).first()
    if not db_user or not verify_password(user_credentials.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": db_user.email})
    refresh_token = create_refresh_token({"sub": db_user.email})
    return {"access_token": access_token, "refresh_token": refresh_token}


# Configurar el logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


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
        add_to_redis(token, "blacklisted", expiration=timedelta(seconds=expiration_time))

    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

    return {"message": "Successfully logged out"}
