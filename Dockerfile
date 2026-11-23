FROM python:3.11-slim

WORKDIR /work
COPY requirements.txt /tmp/benchmark-requirements.txt
RUN python -m pip install --no-cache-dir -r /tmp/benchmark-requirements.txt \
    && rm /tmp/benchmark-requirements.txt

USER 65534:65534
