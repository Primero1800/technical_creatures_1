import uvicorn
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette import status

from src.config.app_config import create_app
from src.config.swagger_config import config_swagger

app = create_app(
    docs_url=None,
    redoc_url=None,
)

APP_TITLE = 'Who'

basic = HTTPBasic()

SECRET_USER: str = 'primero'
SECRET_PASSWORD: str = 'primero'


@app.get("/who", status_code=status.HTTP_200_OK, include_in_schema=False)
@app.get("/who/", status_code=status.HTTP_200_OK)
def get_user(creds: HTTPBasicCredentials = Depends(basic)):
    print(
        '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! HELLO FROM AUTH SERVER APP !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    if (creds.username == SECRET_USER and
            creds.password == SECRET_PASSWORD):
        return {
            "username": creds.username,
            "password": creds.password
        }
    else:
        raise HTTPException(status_code=401, detail="Hey! Go away!")


config_swagger(app, APP_TITLE)


if __name__ == "__main__":
    uvicorn.run("auth:app", reload=True)
