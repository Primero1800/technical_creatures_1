FROM python:3.12
RUN apt-get update -y
RUN apt-get upgrade -y

WORKDIR /app

COPY ./requirements.txt ./
RUN pip install -r requirements.txt
COPY ./src ./src

CMD [ "uvicorn",  "src.main:app", "--host",  "0.0.0.0", "--reload" ]
