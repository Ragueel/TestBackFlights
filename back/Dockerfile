# base image
FROM python:3.6.9-alpine

# set working directory
WORKDIR /usr/src/app
RUN apk add --no-cache make build-base
# add requirements
COPY ./requirements.txt /usr/src/app/requirements.txt

# install requirements
RUN pip install -r requirements.txt

RUN pip install celery
# add app
COPY . /usr/src/app