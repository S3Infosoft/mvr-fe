FROM python:3.7-alpine
MAINTAINER S3-Infosoft

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-depends \
      gcc musl-dev zlib zlib-dev
RUN pip install -r requirements.txt
RUN apk del .tmp-build-depends

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN mkdir -p /vol/logs/
RUN mkdir -p /vol/web/media/
RUN mkdir -p /vol/web/static_root/
RUN adduser -D user
RUN chown -R user:user /vol/
RUN chmod -R 755 /vol/logs/
RUN chmod -R 755 /vol/web/
USER user