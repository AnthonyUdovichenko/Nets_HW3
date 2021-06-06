FROM ubuntu:latest

RUN apt update -y && \
    apt upgrade -y && \
    apt install -y \
    python3

WORKDIR /server
COPY server.py .
COPY server.sh .

ENTRYPOINT [ "bash" ]