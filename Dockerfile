FROM gliderlabs/alpine:3.3

ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

RUN apk-install python3 curl 

RUN curl "https://bootstrap.pypa.io/get-pip.py" | python3    \
    && pip3 install --upgrade pip setuptools click requests

RUN mkdir -p /opt /app

ADD . /app
WORKDIR /app
RUN python3 setup.py develop
CMD anchorage ${ANCHORAGE_MODULE} ${ANCHORAGE_BOSUN_URL} ${ANCHORAGE_BOSUN_TOKEN} --debug

# vim: set expandtab tabstop=4 shiftwidth=4 autoindent smartindent:
