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
# There's nothing special about the commit 7d0f4fb7e911120fd09075049233b587936b0a65 other than than it doesn't
# cause this error
RUN pip install --upgrade pip==19.3.1 && pip install .[test]
