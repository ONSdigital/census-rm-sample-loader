FROM python:3.6

ENV RABBITMQ_HOST rabbitmq
ENV RABBITMQ_PORT 5672
ENV RABBITMQ_VHOST /
ENV RABBITMQ_QUEUE Case.CaseDelivery.binding
ENV RABBITMQ_USER guest
ENV RABBITMQ_PASSWORD guest
ENV RABBITMQ_EXCHANGE collection-outbound-exchange


WORKDIR /app
COPY . /app
RUN pip install pika
RUN pip install jinja2
RUN pip install redis