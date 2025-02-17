import uvicorn
from fastapi import Depends, FastAPI
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette import status

app = FastAPI()
basic = HTTPBasic()


@app.get("/who", status_code=status.HTTP_200_OK, include_in_schema=False)
@app.get("/who/", status_code=status.HTTP_200_OK)
def get_user(creds: HTTPBasicCredentials = Depends(basic)):
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! HELLO FROM AUTH SERVER APP !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    return {"username": creds.username, "password": creds.password}


if __name__ == "__main__":
    uvicorn.run("auth:app", reload=True)