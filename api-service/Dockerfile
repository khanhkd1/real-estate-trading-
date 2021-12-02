FROM python:3.8-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1

# Install python/pip
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip install --no-cache --upgrade pip setuptools

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache mariadb-dev

RUN apk add build-base
RUN apk add libffi-dev
RUN apk add --no-cache mysql-client
RUN pip install --upgrade pip setuptools
RUN apk add --no-cache mariadb-dev
RUN apk add mpc1-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/app/
EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0:8000", "--workers=1", "--threads=1", "run:app"]
