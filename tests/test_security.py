import pytest

from app.core.security import (PasswordValidationModel, get_password_hash,
                               verify_password)


def test_verify_password():
    plain_password = "securepassword"
    hashed_password = get_password_hash(plain_password)
    assert verify_password(plain_password, hashed_password) is True
    assert verify_password("wrongpassword", hashed_password) is False


def test_password_hashing():
    password = "securepassword"
    hashed_password = get_password_hash(password)
    assert hashed_password is not None
    assert (
        hashed_password != password
    )  # Verifica que el hash no sea igual a la contraseña original


def test_valid_password():
    valid_password = "Password123$"
    validated_password = PasswordValidationModel(password=valid_password).password
    assert validated_password == valid_password


def test_invalid_password_missing_uppercase():
    invalid_password = "password123$"
    with pytest.raises(
        ValueError, match="La contraseña debe tener al menos una letra mayúscula"
    ):
        PasswordValidationModel(password=invalid_password)


def test_invalid_password_missing_lowercase():
    invalid_password = "PASSWORD123$"
    with pytest.raises(
        ValueError, match="La contraseña debe tener al menos una letra minúscula"
    ):
        PasswordValidationModel(password=invalid_password)


def test_invalid_password_missing_number():
    invalid_password = "Password$$$"
    with pytest.raises(ValueError, match="La contraseña debe tener al menos un número"):
        PasswordValidationModel(password=invalid_password)


def test_invalid_password_missing_special_char():
    invalid_password = "Password123"
    with pytest.raises(
        ValueError, match="La contraseña debe tener al menos un símbolo especial"
    ):
        PasswordValidationModel(password=invalid_password)


def test_invalid_password_too_short():
    invalid_password = "Pass1$"
    with pytest.raises(
        ValueError, match="La contraseña debe tener una longitud mínima de 9 caracteres"
    ):
        PasswordValidationModel(password=invalid_password)
