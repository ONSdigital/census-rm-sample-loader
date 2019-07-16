#!/usr/bin/env bash
kubectl run sampleloader -it --rm \
    --generator=run-pod/v1 \
    --image eu.gcr.io/census-rm-ci/rm/census-rm-sample-loader \
    --env=RABBITMQ_USER=$(kubectl get secret rabbitmq -o=jsonpath="{.data.rabbitmq-username}" | base64 --decode) \
    --env=RABBITMQ_PASSWORD=$(kubectl get secret rabbitmq -o=jsonpath="{.data.rabbitmq-password}" | base64 --decode) \
    --env=RABBIT_SERVICE_HOST=rabbitmq \
    --env=RABBITMQ_SERVICE_PORT=5572 \
    --env=RABBITMQ_QUEUE='case.sample.inbound' \
    --env=RABBITMQ_VHOST='/' \
    --env=RABBITMQ_EXCHANGE='' \
    -- /bin/bash
