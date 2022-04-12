FROM python:slim-buster

WORKDIR /usr/src/app

RUN apt -y update && apt -y upgrade
RUN apt install git
RUN pip install quickboard

EXPOSE 8050