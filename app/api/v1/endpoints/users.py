from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import PasswordValidationModel, get_current_user
from app.db.session import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import create_user, get_user_by_email

router = APIRouter()


@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Validar la contraseña
    try:
        user.password = PasswordValidationModel(password=user.password).password
    except ValueError:
        raise HTTPException(status_code=400, detail="Contraseña invalida")

    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )
    return create_user(db, user)


@router.get("/current", response_model=UserResponse)
def get_current_user_data(current_user=Depends(get_current_user)):
    """
    Obtiene los datos del usuario actualmente logeado.
    Excluye campos sensibles como la contraseña.
    """
    try:
        # Devolver los datos del usuario sin incluir la contraseña
        return current_user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user data"
        )
