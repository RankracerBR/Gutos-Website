FROM python:3
FROM node:lts

ENV PYTHONBUFFERED=1

WORKDIR /code

COPY requirements.txt /code/

RUN pip install -r requirements.txt
RUN npm install
RUN apt-get update && apt-get install -y nodejs npm

COPY . /code/
