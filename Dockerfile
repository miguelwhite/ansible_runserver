FROM python:3.7

COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

RUN mkdir /srv/ansible_runserver
COPY . /srv/ansible_runserver

WORKDIR /srv/ansible_runserver
