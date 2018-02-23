FROM python:3.6-alpine

LABEL maintainer André "decko" de Brito <decko@birosca.mobi>

RUN apk add --no-cache python-dev gcc musl-dev linux-headers
RUN apk add --no-cache --virtual=build-dependencies wget ca-certificates
RUN apk add --no-cache postgresql-dev
RUN apk add --no-cache git
RUN pip install virtualenv uwsgi
# ADD this so pip can see the requirements.txt file.
ADD ["./requirements.txt","/var/uwsgi/requirements.txt"]
RUN ls -lha /var/uwsgi
RUN pip install -r /var/uwsgi/requirements.txt

RUN apk del python-dev gcc musl-dev linux-headers wget build-dependencies git

WORKDIR /var/uwsgi
EXPOSE 8000 8001

ENTRYPOINT ["uwsgi", "--http", ":8000", "--wsgi-file", "/var/uwsgi/epracas/wsgi.py", "--master", "--stats", ":8001", "--chdir", "/var/uwsgi"]
