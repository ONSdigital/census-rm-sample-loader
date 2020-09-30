#!/usr/bin/env bash

if [ -z "$IMAGE" ]; then
   IMAGE=eu.gcr.io/census-rm-leo-howard-mark4/rm/census-rm-sample-loader
fi

echo "Image $IMAGE"

kubectl run sampleloader -it --rm \
   --generator=run-pod/v1 \
   --image $IMAGE\
   --env=RABBITMQ_USER=$(kubectl get secret rabbitmq -o=jsonpath="{.data.rabbitmq-username}" | base64 --decode) \
   --env=RABBITMQ_PASSWORD=$(kubectl get secret rabbitmq -o=jsonpath="{.data.rabbitmq-password}" | base64 --decode) \
   --env=RABBITMQ_SERVICE_HOST=rabbitmq \
   --env=RABBITMQ_SERVICE_PORT=5672 \
   --env=RABBITMQ_QUEUE='case.sample.inbound' \
   --env=RABBITMQ_VHOST='/' \
   --env=RABBITMQ_EXCHANGE='' \
   -- /bin/bash