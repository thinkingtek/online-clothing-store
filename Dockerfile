FROM python:3.12.6

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY reqs.txt /code/

RUN pip install -r reqs.txt

COPY . /code/