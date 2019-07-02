FROM python:3.7.3-alpine

RUN apk update && apk add bash curl gcc g++ git postgresql-dev musl-dev openldap-dev

COPY . /adjustable-invoice

WORKDIR /adjustable-invoice

RUN pip install -r requirements.txt
