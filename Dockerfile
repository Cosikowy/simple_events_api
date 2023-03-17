FROM python:3.11.2

WORKDIR /app/

RUN apt update -y && apt upgrade -y

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY . .
