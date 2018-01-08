FROM python:3.6.4-alpine
MAINTAINER Vitor Mantovani <vtrmantovani@gmail.com>

RUN apk add --no-cache --update bash git openssh mariadb-dev libffi-dev linux-headers alpine-sdk

RUN addgroup luizalabs && adduser -D -h /home/luizalabs -G luizalabs luizalabs

USER luizalabs
RUN mkdir /home/luizalabs/lem
RUN mkdir /home/luizalabs/migrations
RUN mkdir /home/luizalabs/utils
RUN mkdir /home/luizalabs/logs
ADD wsgi.py /home/luizalabs/
ADD requirements.txt /home/luizalabs/
ADD lem /home/luizalabs/lem
ADD utils /home/luizalabs/utils
ADD migrations /home/luizalabs/migrations
ADD manager.py /home/luizalabs/

RUN cd /home/luizalabs && rm -rf /home/luizalabs/.venv && /usr/local/bin/python -m venv .venv \
    && /home/luizalabs/.venv/bin/pip install --upgrade pip
RUN cd /home/luizalabs && /home/luizalabs/.venv/bin/pip install -r requirements.txt

USER root
RUN chown luizalabs.luizalabs /home/luizalabs -R

USER luizalabs
ADD ./dockerfiles/uwsgi.ini /home/luizalabs/

ADD ./dockerfiles/newrelic.ini /home/luizalabs/
ENV NEW_RELIC_CONFIG_FILE=/home/luizalabs/newrelic.ini

EXPOSE 9000
CMD ["/home/luizalabs/.venv/bin/newrelic-admin", "run-program", "/home/luizalabs/.venv/bin/uwsgi", "--ini", "/home/luizalabs/uwsgi.ini"]