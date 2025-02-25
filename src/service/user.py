import os
import datetime
from dotenv import load_dotenv
# from jose import jwt
import jwt
from fastapi.security import HTTPAuthorizationCredentials

from src.model.user import User
# from passlib.context import CryptContext

import src.utils.crypt_functions as crypt

load_dotenv()

if os.getenv('FAKE') == str(True):
    import src.mock.user as data
else:
    import src.data.user as data

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain: str, hash_password: str) -> bool:
    """Хеширование строки <plain> и сравнение с записью <hash> из базы данных"""
    # return pwd_context.verify(plain, hash_password)
    return crypt.verify_hash(plain, hash_password)


def get_hash(plain: str) -> str:
    """Возврат хеша строки <plain>"""
    # return pwd_context.hash(plain)
    return crypt.get_hash(plain).decode()


def get_jwt_username(token_cred:str) -> dict | None:
    """Возврат имени пользователя из JWT-доступа <token>"""
    try:
        # payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        payload = crypt.jwt_decode(token_cred=token_cred)
        print('!!!!!!!!!!!!! PAYLOAD !!!!!!!!!!!!!!!', payload)
        if not (username := payload.get("sub")):
            return {}
    # except jwt.JWTError:
    except jwt.PyJWTError as error:
        print('!!!!!!!!!!!!!!!!!!!!!!! JWT Error !!!!!!!!!!!!!!!!!!!!!!!!!!! ', error)
        raise error
    result = {'username': username}
    del payload['sub']
    return {**result, **payload}


def get_current_user(token_cred: str | HTTPAuthorizationCredentials) -> dict | None:
    if isinstance(token_cred, HTTPAuthorizationCredentials):
        token_cred = token_cred.credentials
    """Декодирование токена <token> доступа OAuth и возврат объекта User"""
    jwt_info = get_jwt_username(token_cred)
    print("!!!!!!!!!!!!!!!! JWT INFO !!!!!!!!!!!!!!!!!!!", jwt_info)
    # if not jwt_info or not isinstance(jwt_info, dict):
    #     return {}
    username = jwt_info.get('username', None)
    result = {}
    if user := lookup_user(username):
        result['user'] = user
        del jwt_info['username']
        result.update(jwt_info)
    return result


def lookup_user(username: str) -> User | None:
    """Возврат совпадающего пользователя из базы данных для строки <name>"""
    if user := data.get_one(username):
        return user
    return None


def auth_user(name: str, plain: str) -> User | None:
    """Аутентификация пользователя <name> и <plain> пароль"""
    if not (user := lookup_user(name)):
        return None
    if not verify_password(plain, user.hash):
        return None
    return user


def create_access_token(
        data: dict,
        expires: datetime.timedelta | None = None
):
    """Возвращение токена доступа JWT"""
    src = data.copy()
    now = datetime.datetime.now(datetime.UTC)
    if not expires:
        expires = datetime.timedelta(minutes=15)
    src.update({
        "exp": now + expires,
        "iat": now,
    })
    encoded_jwt = crypt.jwt_encode(src)
    print('-------------------------------------------------------------- ENCODED JWT --------------------------------------------------', encoded_jwt)
    return encoded_jwt


# --- CRUD-пассивный материал

def get_all() -> list[User]:
    return data.get_all()


def get_one(name) -> User:
    return data.get_one(name)


def create(user: User) -> User:
    return data.create(User(name=user.name, hash=get_hash(user.hash)))


def modify(name: str, params: dict) -> User:
    return data.modify(name, params)


def replace(user: User) -> User:
    return data.replace(user)


def delete(name: str) -> None:
    return data.delete(name)