#!/bin/sh
docker build . -t storj-linkshare-api
docker stop storj-linkshare-api
docker rm storj-linkshare-api
docker run \
    --name storj-linkshare-api \
    -p 127.0.0.1:9895:9895 \
    -e API_TOKEN=$API_TOKEN \
    -e ACCESS_TOKEN=$ACCESS_TOKEN \
    -e BUCKET_NAME=$BUCKET_NAME \
    storj-linkshare-api