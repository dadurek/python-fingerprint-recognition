FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
	libglib2.0-0 \
	libsm6 \
	libxext6 \
    libgl1 \
	libxrender-dev

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --trusted-host pypi.python.org -r /code/requirements.txt

COPY ./src /code/src

EXPOSE 8000

WORKDIR /code/src

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
