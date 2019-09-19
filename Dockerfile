# Use an official Python runtime as a paretn image
FROM python:3.6.6

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

EXPOSE 8000

