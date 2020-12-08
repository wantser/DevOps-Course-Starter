FROM python:3.8
RUN apt-get update && apt-get install -y curl
COPY ./todo_app/ ./todo_app/ ./poetry.lock ./poetry.lock ./poetry.toml ./poetry.toml 
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python  && pip install poetry

