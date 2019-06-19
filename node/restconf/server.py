import json
from flask import Flask

app = Flask(__name__)

@app.route("/config/transceiver/")
def hello():
    return "Hello World!"

@app.route("/config/transceiver/slice/monitoring/ber/")
def ber():
    ber = { "ber" : 10 }
    return json.dumps(ber)

if __name__ == "__main__":
    app.run(ssl_context='adhoc')
