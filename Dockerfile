FROM python:3.7

RUN mkdir /srv/ansible_runserver
COPY . /srv/ansible_runserver

RUN pip install -r /srv/ansible_runserver/requirements.txt

WORKDIR /srv/ansible_runserver
