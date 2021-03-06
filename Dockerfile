# Work in progress
# docker build -t usvisa-il-app .
# docker run --env-file .env -v $PWD:/shared/ --rm usvisa-il-app
FROM python:3.8.7-slim
MAINTAINER Avi Friedman

ARG GECKO_VERSION=0.30.0

COPY . /usvisa-il-app
WORKDIR /usvisa-il-app

RUN apt-get -y update && apt-get -y upgrade &&\
    apt-get install -y --no-install-recommends firefox-esr xvfb wget &&\
    wget https://github.com/mozilla/geckodriver/releases/download/v${GECKO_VERSION}/geckodriver-v${GECKO_VERSION}-linux64.tar.gz &&\
    tar -C /usr/local/bin/ -xvf geckodriver-v${GECKO_VERSION}-linux64.tar.gz &&\
    rm geckodriver-v${GECKO_VERSION}-linux64.tar.gz &&\
    pip3 install -r requirements.txt &&\
    chmod +x ./src/main.py

CMD ["./src/main.py"]