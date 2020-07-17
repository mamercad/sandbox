from datetime import datetime
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    d = datetime.now()
    return(d.isoformat('T'))

if __name__ == "__main__":
    app.run(host='0.0.0.0')
