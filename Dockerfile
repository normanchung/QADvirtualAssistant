FROM rasa/rasa:latest-full 

WORKDIR /app
COPY . /app
COPY ./data /app/data

USER root

RUN  rasa train

VOLUME /app
VOLUME /app/data
VOLUME /app/models

CMD [ "run","-m","/app/models","--enable-api","--cors","*","--debug" ]

# Switch back to a non-root user
USER 1001