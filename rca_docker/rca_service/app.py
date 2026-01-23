from fastapi import FastAPI
from influxdb_client import InfluxDBClient, Point, WritePrecision
import os, random, datetime

app = FastAPI(title="RCA Demo Service")

influx_url = os.getenv("INFLUX_URL", "http://localhost:8086")
influx_token = os.getenv("INFLUX_TOKEN", "my-token")
influx_org = os.getenv("INFLUX_ORG", "rca_org")
influx_bucket = os.getenv("INFLUX_BUCKET", "rca_bucket")

client = InfluxDBClient(url=influx_url, token=influx_token, org=influx_org)
write_api = client.write_api()

@app.get('/')
def health():
    return {"status":"ok","service":"rca_service"}

@app.post('/infer')
def infer():
    nodes = ["API_GW","AuthService","BillingService","DBService","CacheService","DBReplica"]
    root = random.choice(nodes)
    conf = round(random.uniform(0.6, 0.99), 2)
    now = datetime.datetime.utcnow()

    p = Point("rca_result").tag("root", root).field("confidence", conf).time(now, WritePrecision.NS)
    write_api.write(bucket=influx_bucket, org=influx_org, record=p)

    return {"root_cause": root, "confidence": conf, "timestamp": now.isoformat()}
