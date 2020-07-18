#!/usr/bin/env python3

from datetime import datetime
import json
import os
import time
import pytz
import subprocess
import requests
import sys
import signal
from requests.exceptions import HTTPError

reqs_per_sec = 3

k8s_namespace = os.getenv('K8S_NAMESPACE', default='sandbox')
k8s_service   = os.getenv('K8S_SERVICE',   default='hello')
endpoint      = None
port          = None

attempts     = 0
successes    = 0
failures     = 0

try:
    endpoint = subprocess.check_output('kubectl -n {} get svc {} -o jsonpath="{{.status.loadBalancer.ingress[*].ip}}"'.format(k8s_namespace, k8s_service), shell=True, universal_newlines=True)
    port     = subprocess.check_output('kubectl -n {} get svc {} -o jsonpath="{{.spec.ports[*].port}}"'.format(k8s_namespace, k8s_service), shell=True, universal_newlines=True)
except Exception as e:
    print(f'Exception: {e}')
    sys.exit(1)

def signal_handler(signal, frame):
    global attempts, successes, failures
    successe_rate = 100.0 * successes / attempts
    failure_rate  = 100.0 * failures  / attempts
    print()
    print('-'*120)
    print(f'attempts:  {attempts}')
    print(f'successes: {successes} ({successe_rate}%)')
    print(f'failures:  {failures} ({failure_rate}%)')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

while True:

    attempts    += 1
    status_code =  0

    try:

        d = datetime.now(pytz.timezone("UTC"))
        j = {
            'year'       : d.year,
            'month'      : d.month,
            'day'        : d.day,
            'hour'       : d.hour,
            'minute'     : d.minute,
            'second'     : d.second,
            'microsecond': d.microsecond,
        }

        req_start   = time.time()
        r           = requests.get('http://{}:{}'.format(endpoint, port), timeout=1)
        req_finish  = time.time()
        status_code = r.status_code

        r.raise_for_status()

        remote_date = r.json()['date']
        remote_tag  = r.json()['tag']
        ttlb        = req_finish - req_start

        print('-'*120)
        print(f'attempt: {attempts} (HTTP {status_code}) (TAG {remote_tag})')
        print(f'  local date:  {j}')
        print(f'  remote date: {remote_date}')
        print(f'  ttlb:        {ttlb}')

        successes += 1

    except Exception as e:

        print('-'*120)
        print(f'attempt: {attempts} (HTTP {status_code})')
        print(f'  local date: {j}')
        print(f'  exception:  {e}')

        failures += 1

    time.sleep( 1 / reqs_per_sec )
