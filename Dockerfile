# Use an official Python runtime as a paretn image
FROM python:3.7

WORKDIR /app

RUN pip install --no-cache-dir gunicorn==19.9.0

ADD requirements.txt /app/

RUN pip install -r requirements.txt

ADD . /app

EXPOSE 8000

CMD ["gunicorn", "-w 3", "-b :8080", "icpcsite.wsgi"]
