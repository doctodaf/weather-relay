from flask import Flask, request
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import os

app = Flask(__name__)

INFLUX_URL = os.environ["INFLUX_URL"]
INFLUX_TOKEN = os.environ["INFLUX_TOKEN"]
INFLUX_ORG = os.environ["INFLUX_ORG"]
INFLUX_BUCKET = os.environ["INFLUX_BUCKET"]

client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)

@app.route("/weather", methods=["POST"])
def receive():
    data = request.form.to_dict()
    point = Point("ecowitt")
    for key, value in data.items():
        try:
            point = point.field(key, float(value))
        except (ValueError, TypeError):
            pass
    write_api.write(bucket=INFLUX_BUCKET, record=point)
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)