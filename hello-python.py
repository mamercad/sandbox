from datetime import datetime
from flask import Flask
import sys

app = Flask(__name__)

@app.route("/")
def hello():
    d = datetime.now()
    return('{} ({})'.format(d.isoformat('T'), sys.argv[1]))

if __name__ == "__main__":
    app.run(host='0.0.0.0')
