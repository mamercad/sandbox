#!/usr/bin/env bash

r=0
while true; do
  r=$((r+1))
  d=$(date)
  c=$(curl -s -m1 $(kubectl -n sandbox get svc hello-python-service -o jsonpath="{.status.loadBalancer.ingress[*].ip}"):6000 2>&1)
  echo "$r: $c"
  sleep 0.3
done
