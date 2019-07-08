FROM python:3.7.3-alpine

RUN apk update && apk add bash curl gcc g++ git postgresql-dev musl-dev openldap-dev postgresql-client

WORKDIR /adjustable_invoice

# Copy over requirements.txt file first to utilize Docker's aggressive caching
# and prevent reinstalling modules on any app changes
COPY ./requirements.txt /adjustable_invoice/requirements.txt

RUN pip install -r requirements.txt

COPY . /adjustable_invoice
