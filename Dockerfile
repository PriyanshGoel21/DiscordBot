FROM python:3.10-buster
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY . /code/

RUN apt-get update && apt-get install -y \
    ffmpeg \
    libffi-dev \
    libnacl-dev

RUN pip install -r requirements.txt