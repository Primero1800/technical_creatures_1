FROM python:3.12
RUN apt-get update -y
RUN apt-get upgrade -y

WORKDIR /app

COPY ./requirements.txt ./
RUN pip install -r requirements.txt
COPY ./catloader ./catloader

CMD [ "python3", "./catloader/manage.py", "runserver", "0.0.0.0:8000" ]