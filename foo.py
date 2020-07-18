#!/usr/bin/env python3

from datetime import datetime
import sys, pytz, json

print(len(sys.argv))

d = datetime.now(pytz.timezone("UTC"))
r = {
    'year': d.year,
    'month': d.month,
    'day': d.day,
    'hour': d.hour,
    'minute': d.minute,
    'second': d.second,
    'microsecond': d.microsecond,
}
print(json.dumps(r))
