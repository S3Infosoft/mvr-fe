FROM python:3.7-slim-stretch
MAINTAINER S3-Infosoft

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN mkdir -p /vol/logs/
RUN mkdir -p /vol/web/media/
RUN mkdir -p /vol/web/static_root/
RUN adduser --disabled-password --gecos "" user
RUN chown -R user:user /vol/
RUN chmod -R 755 /vol/logs/
RUN chmod -R 755 /vol/web/
USER user