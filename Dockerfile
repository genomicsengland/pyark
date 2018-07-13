FROM ubuntu:latest

RUN mkdir /cip_api_tests
WORKDIR /cip_api_tests

env DEBIAN_FRONTEND noninteractive
RUN apt-get update && \ 
    apt-get install -y build-essential python \ 
    python-dev python-pip python-virtualenv postgresql \ 
    postgresql-contrib libpq-dev \
    libsasl2-dev libldap2-dev libssl-dev git \
    libz-dev
ENV INTERPRETATION_DB_HOST db
ENV PYTHONUNBUFFERED 1
ENV CIPAPI_SWAGGER_FORCE_HTTPS False
ADD . /cip_api_tests

RUN pip install --upgrade pip==9.0.3 && pip install .[test] --index-url=https://pypi.gel.zone/genomics/dev
