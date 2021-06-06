FROM ubuntu:latest

RUN apt update -y && \
    apt upgrade -y && \
    apt install -y \
    python3

WORKDIR /client
COPY client.py .
COPY client.sh .
COPY inputfile .

ENTRYPOINT [ "bash" ]