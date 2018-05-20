FROM alpine:3.7
MAINTAINER Jong-Hyouk Yun <ageldama@gmail.com>
RUN apk add --update \
    build-base \
    python3 python3-dev py3-pip \
    postgresql-client postgresql-dev
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
ENV UNTERTAXI_API_CONFIG docker
RUN python3 manage.py db upgrade
ENTRYPOINT ["python"]
CMD ["manage.py", "runserver"]