from datetime import datetime, timedelta, timezone
import jwt
import uuid
from passlib.context import CryptContext
from typing import Optional
from app.domain.exceptions import AuthenticationError
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    if not settings.SECRET_KEY:
        raise ValueError("SECRET_KEY must be set in the configuration.")

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})

    to_encode.update({"jti": str(uuid.uuid4())})

    encoded_token = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return encoded_token


def decode_access_token(token: str) -> dict:
    if not settings.SECRET_KEY:
        raise ValueError("SECRET_KEY must be set in the configuration.")

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            options={"verify_exp": True},
        )
        return payload

    except jwt.ExpiredSignatureError:
        raise AuthenticationError("Token expired.")
    except jwt.InvalidTokenError:
        raise AuthenticationError("Invalid token.")
    except Exception as e:
        raise AuthenticationError(f"Error decoding token: {str(e)}")
