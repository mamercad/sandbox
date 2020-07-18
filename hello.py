from datetime import datetime
from flask import Flask
import json
import pytz
import sys

app = Flask(__name__)

tag = 'blue'
if len(sys.argv) > 1:
    tag = sys.argv[1]

@app.route('/')
def hello():
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
    r = { 'date': j, 'tag': tag }
    return(json.dumps(r))

if __name__ == '__main__':
    app.run(host='0.0.0.0')
