FROM python:3.6-alpine

RUN apk add --no-cache python-dev gcc musl-dev linux-headers
RUN apk add --no-cache --virtual=build-dependencies wget ca-certificates
RUN apk add --no-cache postgresql-dev
RUN apk add --no-cache git
RUN pip install virtualenv uwsgi
COPY . /var/uwsgi
RUN ls -lha /var/uwsgi
RUN pip install -r /var/uwsgi/requirements.txt

RUN apk del python-dev gcc musl-dev linux-headers wget build-dependencies git

WORKDIR /var/uwsgi
EXPOSE 8000 8001
