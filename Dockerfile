FROM rusvaleev/ubuntu-chrome


WORKDIR /home/thumbsup

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY . .
RUN chmod +x boot.sh

ENTRYPOINT ./boot.sh
