FROM alpine:3.7
MAINTAINER Jong-Hyouk Yun <ageldama@gmail.com>

RUN apk add --update \
    build-base \
    python3 python3-dev py3-pip \
    postgresql-client postgresql-dev

RUN apk add --no-cache openssl
ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz

COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
ENV UNTERTAXI_API_CONFIG docker
ENTRYPOINT ["sh"]
CMD ["./docker-compose/run-with-db-upgrade.sh"]
