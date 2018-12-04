FROM ubuntu:18.04

RUN apt-get update \
    && apt-get install -y chromium-chromedriver \
    && apt-get install -y locales \
    && apt-get install -y python3 python3-dev python3-pip python3-venv \
    && apt-get install -y libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8

WORKDIR /home/thumbsup

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY . .
RUN chmod +x boot.sh

ENTRYPOINT '/home/thumbsup/boot.sh'
