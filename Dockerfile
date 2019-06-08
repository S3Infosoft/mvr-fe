FROM python:3.7-alpine
MAINTAINER S3-Infosoft

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN mkdir -p /LOGS
RUN adduser -D user
RUN chown -R user:user /LOGS
RUN chmod -R 755 /LOGS
USER user