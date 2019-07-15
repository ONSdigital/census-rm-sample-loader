FROM python:3.6-slim

ENV RABBITMQ_HOST rabbitmq
ENV RABBITMQ_PORT 5672
ENV RABBITMQ_VHOST /
ENV RABBITMQ_QUEUE case.sample.inbound
ENV RABBITMQ_USER guest
ENV RABBITMQ_PASSWORD guest
ENV RABBITMQ_EXCHANGE collection-outbound-exchange

WORKDIR /app
COPY . /app
RUN pip install pipenv
RUN pipenv install --system --deploy