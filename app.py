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

@app.route("/weather", methods=["GET", "POST"])
def receive():
    data = {**request.args.to_dict(), **request.form.to_dict()}
    if not data:
        return "No data", 400
    point = Point("ecowitt")
    written = 0
    for key, value in data.items():
        try:
            point = point.field(key, float(value))
            written += 1
        except (ValueError, TypeError):
            pass
    if written > 0:
        write_api.write(bucket=INFLUX_BUCKET, record=point)
        return "OK", 200
    return "No numeric data", 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
