FROM python:3.9

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY ./requirements.txt /requirements.txt

RUN python -m pip install --upgrade pip

COPY . /code/


RUN pip install -r requirements.txt