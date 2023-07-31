FROM python:3.9.6-alpine

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apk add libmagic

RUN pip3 install --upgrade pip
RUN pip3 install python-magic==0.4.15

COPY requirements.txt app/requirements.txt
RUN pip3 install -r app/requirements.txt

COPY . /app
