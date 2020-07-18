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

try:
    endpoint = subprocess.check_output('kubectl -n sandbox get svc hello -o jsonpath="{.status.loadBalancer.ingress[*].ip}"', shell=True, universal_newlines=True)
    port = subprocess.check_output('kubectl -n sandbox get svc hello -o jsonpath="{.spec.ports[*].port}"', shell=True, universal_newlines=True)
except Exception as e:
    print(e)
    sys.exit(1)

def signal_handler(signal, frame):
    global attempts, successes, failures
    print()
    print('attempts: {}'.format(attempts))
    print('successes: {} ({}%)'.format(successes, 100.0*successes/attempts))
    print('failures: {} ({}%)'.format(failures, 100.0*failures/attempts))
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

attempts  = 0
successes = 0
failures  = 0

while True:

    attempts += 1
    status_code = 0

    try:

        d = datetime.now(pytz.timezone("UTC"))
        j = {
            'year': d.year,
            'month': d.month,
            'day': d.day,
            'hour': d.hour,
            'minute': d.minute,
            'second': d.second,
            'microsecond': d.microsecond,
        }
        req_start = time.time()
        r = requests.get('http://{}:{}'.format(endpoint, port), timeout=1)
        req_finish = time.time()
        status_code = r.status_code
        r.raise_for_status()

        # print("attempt: {}\n  local:  {}\n  remote: {}\n  tag:    {}\n".format(attempts, j, r.json()['date'], r.json()['tag']))
        # requests elapsed: The amount of time elapsed between sending the request and the arrival of the response (as a timedelta). This property specifically measures the time taken between sending the first byte of the request and finishing parsing the headers. It is therefore unaffected by consuming the response content or the value of the stream keyword argument.

        remote_date = r.json()['date']
        remote_tag  = r.json()['tag']

        print("attempt: {} ({})".format(attempts, remote_tag))
        print("  local date:  {}".format(j))
        print("  remote date: {}".format(remote_date))
        # print("  tag:         {}".format(remote_tag))
        # print("  ttfb: {}".format(r.elapsed))
        print("  ttlb:        {}".format(req_finish - req_start))

        successes += 1

    except HTTPError as http_e:

        print("{} : {} : {} : {}".format(attempts, j, status_code, http_e))
        failures += 1

    except Exception as e:

        print("{} : {} : {} : {}".format(attempts, j, status_code, e))
        failures += 1

    time.sleep(0.5)
