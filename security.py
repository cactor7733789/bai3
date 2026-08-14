from datetime import datetime, timedelta, timezone
import re

import bcrypt
import jwt

SECRET_KEY = "super-secret-key-ss21-min-32-bytes!!"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )


def create_access_token(data: dict, expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    payload["exp"] = expire
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


def validate_password_strength(password: str) -> str | None:
    if len(password) < 8:
        return "Mật khẩu phải có tối thiểu 8 ký tự"
    if not re.search(r"[A-Z]", password):
        return "Mật khẩu phải có ít nhất một chữ hoa"
    if not re.search(r"[a-z]", password):
        return "Mật khẩu phải có ít nhất một chữ thường"
    if not re.search(r"\d", password):
        return "Mật khẩu phải có ít nhất một chữ số"
    return None
