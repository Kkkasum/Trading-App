FROM python:3.11

RUN mkdir /fastapi_app

WORKDIR /fastapi_app

COPY poetry.lock pyproject.toml ./

RUN pip3 install poetry

RUN poetry install

RUN apt-get update && apt-get install -y --no-install-recommends uvicorn gunicorn

COPY . .

WORKDIR src

CMD gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000