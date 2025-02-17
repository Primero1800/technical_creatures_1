import os
from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from src.model.user import User

from dotenv import load_dotenv

load_dotenv()

if os.getenv("FAKE"):
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! FAKE SERVICE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    import src.mock.user as service
else:
    import src.service.user as service

from src.errors import Missing, Duplicate

ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(prefix = "/user")