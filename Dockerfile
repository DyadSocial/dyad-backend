# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
RUN apt update \
    && apt install -y --no-install-recommends libpcre3 libpcre3-dev 
RUN pip install uwsgi --no-cache-dir
EXPOSE 8000
