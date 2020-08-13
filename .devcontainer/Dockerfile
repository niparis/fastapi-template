FROM python:3.8.5-slim

# Copy default endpoint specific user settings overrides into container to specify Python path
COPY .devcontainer/settings.vscode.json /root/.vscode-remote/data/Machine/settings.json

ENV PYTHONUNBUFFERED 1

RUN mkdir /workspace
WORKDIR /workspace

ENV SHELL /bin/bash

RUN apt-get update
RUN apt-get install -y --no-install-recommends \
    curl \
    git \
    ssh

RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

RUN /bin/bash -c "source $HOME/.poetry/env && poetry config virtualenvs.create false && poetry install --no-ansi --no-root"

RUN echo export PATH=$PATH:$HOME/.poetry/bin >> ~/.bashrc

