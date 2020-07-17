#!/usr/bin/env python3

from datetime import datetime
import os, time, subprocess, requests, sys, signal

def signal_handler(sig, frame):
    global attempts, successes, failures
    print('You pressed Ctrl+C!')
    print('attempts: {}'.format(attempts))
    print('successes: {} ({}%)'.format(successes, 100.0*successes/attempts))
    print('failures: {} ({}%)'.format(failures, 100.0*failures/attempts))
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

endpoint = subprocess.check_output('kubectl -n sandbox get svc hello-python-service -o jsonpath="{.status.loadBalancer.ingress[*].ip}"', shell=True, universal_newlines=True)
port = subprocess.check_output('kubectl -n sandbox get svc hello-python-service -o jsonpath="{.spec.ports[*].port}"', shell=True, universal_newlines=True)

attempts = 0
successes = 0
failures = 0
while True:
  try:
    d = datetime.now()
    r = requests.get('http://{}:{}'.format(endpoint, port))
    print("{} : {} : {}".format(attempts, d, r.text))
    successes += 1
  except Exception as e:
    failures += 1
    print(e)
  finally:
    attempts += 1
  time.sleep(0.5)
