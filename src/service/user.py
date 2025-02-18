import os
import datetime
from dotenv import load_dotenv
from jose import jwt

from src.model.user import User

load_dotenv()

if os.getenv('FAKE') == str(True):
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! FAKE DATA !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    import src.mock.user as data
else:
    import src.data.user as data

from passlib.context import CryptContext

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain: str, hash: str) -> bool:
    """Хеширование строки <plain> и сравнение с записью <hash> из базы данных"""
    return pwd_context.verify(plain, hash)


def get_hash(plain: str) -> str:
    """Возврат хеша строки <plain>"""
    return pwd_context.hash(plain)


def get_jwt_username(token:str) -> str | None:
    """Возврат имени пользователя из JWT-доступа <token>"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print('!!!!!!!!!!!!! PAYLOAD !!!!!!!!!!!!!!!', payload)
        if not (username := payload.get("sub")):
            return None
    except jwt.JWTError:
        print('!!!!!!!!!!!!!!!!!!!!!!! JWT Error !!!!!!!!!!!!!!!!!!!!!!!!!!!')
        return None
    return username


def get_current_user(token: str) -> User | None:
    """Декодирование токена <token> доступа OAuth и возврат объекта User"""
    if not (username := get_jwt_username(token)):
        return None
    if user := lookup_user(username):
        return user
    return None


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
    src.update({"exp": now + expires})
    encoded_jwt = jwt.encode(src, SECRET_KEY, algorithm=ALGORITHM)
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


def delete(name: str) -> None:
    return data.delete(name)