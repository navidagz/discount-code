FROM python:3.9.6-buster

WORKDIR /app

RUN apt-get -y update && apt-get -y upgrade

COPY ./requirements.txt ./requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./ ./
ENV LOG_LEVEL info
ENV PYTHONPATH=.

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait
RUN chmod +x /wait
RUN chmod -R +x /app/scripts


CMD /wait && sh /app/scripts/entry_point.sh

