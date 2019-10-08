FROM python:3.7

COPY . /app
WORKDIR /app
#RUN apk add make automake gcc g++ subversion python3-dev
RUN pip install -r requirements.txt

CMD python ./main.py
