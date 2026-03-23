"""Utlities for security-related operations like password management."""
from datetime import datetime, timedelta, timezone

from pwdlib import PasswordHash
from pwdlib.exceptions import UnknownHashError
from pwdlib.hashers.bcrypt import BcryptHasher


password_hash = PasswordHash([BcryptHasher()])


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    try:
        verified = password_hash.verify(plain_password, hashed_password)
    except UnknownHashError:
        return False
    return verified
