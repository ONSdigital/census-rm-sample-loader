#!/usr/bin/env bash
kubectl run sampleloader -it --rm \
    --generator=run-pod/v1 \
    --image eu.gcr.io/census-rm-ci/census-rm-sample-loader \
    -- /bin/bash
