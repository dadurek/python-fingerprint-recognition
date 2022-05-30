#FROM nginx:latest
FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
	libglib2.0-0 \
	libsm6 \
	libxext6 \
    libgl1 \
	libxrender-dev

COPY ./requirements.txt /app
RUN pip install --trusted-host pypi.python.org -r requirements.txt

COPY . /app

ENTRYPOINT ["/app/core/run.sh"]
