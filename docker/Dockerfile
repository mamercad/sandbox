FROM ubuntu:focal

ENV DEBIAN_FRONTEND=noninteractive

SHELL ["/bin/bash", "-c"]

RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get update --yes && \
    apt-get install --yes python3 python3-dev python3-pip python3-venv

COPY requirements.txt /

RUN python3 -m venv /venv && \
    source /venv/bin/activate && \
    pip3 install -r /requirements.txt
