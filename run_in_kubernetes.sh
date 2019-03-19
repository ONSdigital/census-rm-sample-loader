#!/usr/bin/env bash
kubectl run sampleloader -it --rm \
    --generator=run-pod/v1 \
    --image eu.gcr.io/census-rm-ci/census-rm-sample-loader \
    --env=REDIS_SERVICE_HOST=$(kubectl get configmap redis-config -o=jsonpath="{.data.redis-host}") \
    --env=REDIS_SERVICE_PORT=$(kubectl get configmap redis-config -o=jsonpath="{.data.redis-port}") \
    -- /bin/bash
