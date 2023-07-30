#FROM python:3.8-slim-buster
FROM python:3.9.6-alpine

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apk add libmagic

RUN pip install --upgrade pip
RUN pip install python-magic==0.4.15

COPY requirements.txt app/requirements.txt
RUN pip3 install -r app/requirements.txt


COPY . /app

#ENTRYPOINT [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


