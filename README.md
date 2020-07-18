# hello

Simple Kubernetes deployment (which runs a simple Python web application) that returns:

```bash
❯ curl 192.168.1.231:5000
{"date": {"year": 2020, "month": 7, "day": 18, "hour": 15, "minute": 48, "second": 56, "microsecond": 674045}, "tag": "blue"}
```

Requirements:

* Docker
* `python3`
* Kubernetes
* `make`

As far as the Kubernetes deployment goes, it consists of a `Namespace`, `Service` and `Deployment`. The service type is `LoadBalancer`. Port `5000/tcp` is mapped to port `5000/tcp`.

```bash
❯ kubectl get service hello
NAME    TYPE           CLUSTER-IP       EXTERNAL-IP     PORT(S)          AGE
hello   LoadBalancer   10.152.183.144   192.168.1.231   5000:32667/TCP   61m
```

The deployment makes use of liveness and readiness probes to ensure that requests aren't lost. There's a `Dockerfile` which builds the custom image, a simple Python Flask web application that returns the current date and time, along with the "tag" -- which is passed as an argument in the `ENTRYPOINT`. This makes it easy to see which deployment is being served up from the perspective of the client (`client.py`).

The client hits the endpoint multiple times a second (hardcoded at `reqs_per_sec`, but, can easily be changed), capturing `attempts`, `successes` and `failures`. The client traps and handles `SIGKILL` and once received, will dump out the statistics of its lifetime.

An abbreviated run looks like this:

```bash
> ./client.py
...
------------------------------------------------------------------------------------------------------------------------
attempt: 1199 (HTTP 200) (TAG green)
  local date:  {'year': 2020, 'month': 7, 'day': 18, 'hour': 15, 'minute': 41, 'second': 33, 'microsecond': 494411}
  remote date: {'year': 2020, 'month': 7, 'day': 18, 'hour': 15, 'minute': 41, 'second': 33, 'microsecond': 490632}
  ttlb:        0.012790203094482422
------------------------------------------------------------------------------------------------------------------------
attempt: 1200 (HTTP 200) (TAG green)
  local date:  {'year': 2020, 'month': 7, 'day': 18, 'hour': 15, 'minute': 41, 'second': 33, 'microsecond': 843922}
  remote date: {'year': 2020, 'month': 7, 'day': 18, 'hour': 15, 'minute': 41, 'second': 33, 'microsecond': 838813}
  ttlb:        0.011906862258911133
^C
------------------------------------------------------------------------------------------------------------------------
attempts:  1200
successes: 1200 (100.0%)
failures:  0 (0.0%)
```

The `Makefile` has a bunch of useful targets.
