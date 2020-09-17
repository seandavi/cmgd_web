FROM python:3.8-alpine as base

MAINTAINER Sean Davis <seandavi@gmail.com>
FROM base as builder
RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev make postgresql-dev
RUN pip install poetry
COPY . /src/
WORKDIR /src
RUN python -m venv /env && . /env/bin/activate && poetry install

FROM base
RUN apk add --no-cache postgresql-libs
COPY --from=builder /env /env
COPY --from=builder /src /src
WORKDIR /src
CMD ["/env/bin/gunicorn", "cmgd_web.asgi:app", "-b", "0.0.0.0:80", "-k", "uvicorn.workers.UvicornWorker"]