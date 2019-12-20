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

# Need to install ultrajson like this because of https://github.com/esnme/ultrajson/issues/326#issuecomment-461717667
# we were seeing ImportError: /usr/local/lib/python2.7/dist-packages/ujson.so: undefined symbol: Buffer_AppendShortHexUnchecked
RUN pip install --upgrade pip==9.0.3 && pip install git+https://github.com/esnme/ultrajson.git .[test]
