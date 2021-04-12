FROM python:3.8 as base

MAINTAINER Sean Davis <seandavi@gmail.com>
FROM base as builder
RUN apt-get update
RUN apt-get install -y gcc musl-dev libffi-dev openssl make postgresql libzmq3-dev rustc cargo
RUN pip install poetry
COPY . /src/
WORKDIR /src
COPY curatedmetagenomicdata-60b3f98b417c.json .
RUN python -m venv /env && . /env/bin/activate && poetry install --no-dev

FROM base
#RUN apt-get install -y postgresql-libs
COPY --from=builder /env /env
COPY --from=builder /src /src
WORKDIR /src

ENV PORT=80
EXPOSE $PORT

CMD /env/bin/uvicorn --host 0.0.0.0 --port $PORT cmgd_web.asgi:app
