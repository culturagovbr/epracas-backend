FROM python:3.6-alpine

LABEL maintainer André "decko" de Brito <decko@birosca.mobi>

RUN apk add --no-cache python-dev gcc musl-dev linux-headers
RUN apk add --no-cache --virtual=build-dependencies wget ca-certificates
RUN apk add --no-cache postgresql-dev
RUN apk add --no-cache git
RUN pip install virtualenv uwsgi
RUN git clone https://gitlab.com/decko/epracas-backend /var/uwsgi
RUN pip install -r /var/uwsgi/requirements.txt

EXPOSE 8000 8001

# RUN uwsgi --http :8000 --wsgi-file /var/uwsgi/epracas/wsgi.py --master --stats :8001 --chdir /var/uwsgi
# ENTRYPOINT ["uwsgi", "--http localhost:8000", "--wsgi-file /var/uwsgi/epracas/wsgi.py", "--master", "--stats :8001", "--chdir /var/uwsgi"]
ENTRYPOINT ["uwsgi", "--http", ":8000", "--wsgi-file", "/var/uwsgi/epracas/wsgi.py", "--master", "--stats", ":8001", "--chdir", "/var/uwsgi"]
