FROM python:3.10.1-bullseye

WORKDIR /app

COPY Pipfile Pipfile.lock /app/
RUN pip install pipenv

ENV PIP_USER=1
RUN pipenv sync --system