FROM ubuntu:23.04

RUN apt-get update && apt-get install -y bash python3 python3-poetry

WORKDIR /workdir
COPY ./pyproject.toml /workdir/
COPY ./poetry.lock /workdir/

RUN poetry install

CMD ["/bin/bash"]