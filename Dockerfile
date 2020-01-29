FROM python:3.7-slim

RUN pip install pipenv

RUN groupadd --gid 1000 sampleloader && useradd --create-home --system --uid 1000 --gid sampleloader sampleloader
WORKDIR /home/sampleloader

ENV RABBITMQ_SERVICE_HOST rabbitmq
ENV RABBITMQ_SERVICE_PORT 5672
ENV RABBITMQ_VHOST /
ENV RABBITMQ_QUEUE case.sample.inbound
ENV RABBITMQ_USER guest
ENV RABBITMQ_PASSWORD guest

COPY Pipfile* /home/sampleloader/
RUN pipenv install --system --deploy
USER sampleloader

COPY --chown=sampleloader . /home/sampleloader