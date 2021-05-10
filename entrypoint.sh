#!/bin/sh
mkdir -p config

echo "access: default" > config/config.yaml
echo "accesses.default: ${ACCESS_TOKEN}" >> config/config.yaml
echo "log.level: warn" >> config/config.yaml
echo "metrics.addr: \"\"" >> config/config.yaml

gunicorn --workers 18 --threads 9 --bind 0.0.0.0:9895 server:app