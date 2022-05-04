# syntax=docker/dockerfile:1

FROM python:3.6
ENV PYTHONUNBUFFERRED=1
WORKDIR /custom-activation
COPY ./requirements.txt requirements.txt 
RUN pip install -r requirements.txt