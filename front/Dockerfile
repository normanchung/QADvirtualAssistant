FROM ubuntu:18.04

RUN apt-get update && apt-get -y install curl gnupg && curl -sL https://deb.nodesource.com/setup_15.x  | bash - && apt-get -y install nodejs


WORKDIR /app/front
COPY . /app/front

RUN npm install 

VOLUME /app/front

CMD npm start