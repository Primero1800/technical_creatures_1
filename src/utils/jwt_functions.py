import jwt

from src.settings import settings


def jwt_encode(
        payload: dict,
        private_key: str = settings.auth_jwt.private_key.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
):
    return jwt.encode(
        payload=payload,
        key=private_key,
        algorithm=algorithm,
    )


def jwt_decode(
        token: str | bytes,
        public_key: str = settings.auth_jwt.public_key.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
):
    return jwt.decode(
        token=token,
        key=public_key,
        algorithms=[algorithm],
    )