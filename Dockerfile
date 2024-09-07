FROM python:3

ENV PYTHONBUFFERED=1

WORKDIR /code

COPY reqs.txt /code/

RUN pip install -r reqs.txt

COPY . /code/