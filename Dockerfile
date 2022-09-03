FROM python:3.10.5

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

RUN apt-get update
RUN apt-get upgrade -y

COPY . /code/
RUN pip install -r requirements.txt
