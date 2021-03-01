FROM python:3.8.6-slim-buster AS base
RUN apt-get update && apt-get install -y curl
WORKDIR /app
COPY /todo_app ./todo_app/
ENV POETRY_HOME=/poetry
ENV PATH=${POETRY_HOME}/bin:${PATH}
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
COPY poetry.toml pyproject.toml README.md poetry.lock ./
RUN poetry install
EXPOSE 5000
ENTRYPOINT ["poetry", "run", "gunicorn", "-b", "0.0.0.0:5000", "todo_app.app:app"]

FROM base as production

FROM base AS development
ENTRYPOINT ["poetry", "run", "flask", "run", "--host", "0.0.0.0"]

FROM base AS test
ENTRYPOINT ["poetry", "run", "pytest"]