FROM python:3.6-alpine

RUN apk --update add bash \
    supervisor \
    zip \
    mysql-client \
    openssl \
    openssh \
    python3-dev \
    curl \
    curl-dev \
    libffi-dev \
    make \
    gcc \
    g++ \
    linux-headers \
    musl-dev \
    pcre-dev \
    mariadb-dev && \ 
    # install libkafka
    # curl -fSL https://github.com/edenhill/librdkafka/archive/v0.11.4.tar.gz -o librdkafka-0.11.4.tar.gz && \
    #	tar -zxvf librdkafka-0.11.4.tar.gz && cd librdkafka-0.11.4 && \
    # ./configure && make && make install && \
    # cd / && rm -rf librdkafka-0.11.4.tar.gz librdkafka-0.11.4 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip uwsgi Flask setuptools cython alembic nose coverage ujson requests mysqlclient elasticsearch pika python-rapidjson \
    datadog hiredis redis arrow paramiko s3cmd boto3 structlog && \
    # pykafka structlog confluent-kafka confluent-kafka[avro] && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    rm -r /root/.cache && \
    mkdir -p /srv/root && \
    mkdir -p /var/log/supervisor && \
    mkdir -p /srv/root && \
    mkdir -p /var/log/gibson && \
    apk del gcc linux-headers musl-dev make libffi-dev g++ git

ADD conf/supervisord.conf /etc/supervisord.conf

# Add Scripts
ADD scripts/start.sh /start.sh
RUN chmod 755 /start.sh

# Add ini
ADD conf/uwsgi-service.ini /uwsgi-service.ini

# copy in code
ADD src/ /srv/root/

EXPOSE 80

CMD ["/start.sh"]
