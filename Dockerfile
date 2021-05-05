FROM python:3.8.6-slim-buster AS production
RUN apt-get update && apt-get install -y curl
WORKDIR /app
ENV POETRY_HOME=/poetry
ENV PATH=${POETRY_HOME}/bin:${PATH}
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
COPY poetry.toml . pyproject.toml .
RUN poetry install
EXPOSE 5000
ENTRYPOINT ["poetry", "run", "gunicorn", "-b", "0.0.0.0:5000", "todo_app.app:app"]

FROM python:3.8.6-slim-buster AS development
RUN apt-get update && apt-get install -y curl
WORKDIR /app
ENV POETRY_HOME=/poetry
ENV PATH=${POETRY_HOME}/bin:${PATH}
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
COPY poetry.toml . pyproject.toml .
RUN poetry install
EXPOSE 5000
ENTRYPOINT ["poetry", "run", "flask", "run", "--host", "0.0.0.0"]
