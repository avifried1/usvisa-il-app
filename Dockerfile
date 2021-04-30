# Work in progress
# docker build -t usvisa-il-app .
# docker run --env-file .env --rm usvisa-il-app
FROM python:3.8.7-slim
MAINTAINER Avi Friedman

COPY . /usvisa-il-app
WORKDIR /usvisa-il-app

RUN apt-get -y update && apt-get -y upgrade &&\
    apt-get install -y --no-install-recommends firefox-esr xvfb wget &&\
    wget https://github.com/mozilla/geckodriver/releases/download/v0.29.1/geckodriver-v0.29.1-linux64.tar.gz &&\
    tar -C /usr/local/bin/ -xvf geckodriver-v0.29.1-linux64.tar.gz &&\
    rm geckodriver-v0.29.1-linux64.tar.gz &&\
    pip3 install -r requirements.txt &&\
    chmod +x ./src/usvisa-linux.py

CMD ["./src/usvisa-linux.py"]