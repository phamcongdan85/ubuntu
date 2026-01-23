import json
import pandas as pd
import time

# -----------------------------
# InfluxDB v2 connection
# -----------------------------
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

INFLUX_URL = "http://influxdb:8086"   # service name từ docker-compose
INFLUX_TOKEN = "XkJd8V8n2Gq1..."      # ⚠️ thay bằng token thật của bạn
INFLUX_ORG = "my-org"                 # ⚠️ đúng org name bạn đã tạo
INFLUX_BUCKET = "metrics"             # ⚠️ đúng bucket name bạn dùng

try:
    client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    print("[INFO] ✅ Connected to InfluxDB v2")
except Exception as e:
    print("❌ Failed to connect InfluxDB v2:", e)
    client = None
    write_api = None

# -----------------------------
# Import BOCPD từ thư viện baro
# -----------------------------
from baro.anomaly_detection import bocpd
from baro.root_cause_analysis import robust_scorer
from baro.utility import download_data, read_data


def detect_and_write(metric_id, timestamps, columns, data_matrix):
    """
    Thực hiện phát hiện bất thường (BOCPD) và ghi kết quả vào InfluxDB v2.
    """
    df = pd.DataFrame(data_matrix, columns=columns)

    print(f"[DEBUG] metric_id={metric_id}")
    print(f"[DEBUG] timestamps len={len(timestamps) if timestamps else 0}")
    print(f"[DEBUG] columns={columns}")
    print(f"[DEBUG] data shape={df.shape}")

    # -----------------------------
    # Gọi BOCPD để phát hiện anomaly
    # -----------------------------
    try:
        anomalies = bocpd(df)
        print(f"[DEBUG] anomalies={anomalies}")
    except Exception as e:
        print("❌ Error running bocpd:", e)
        anomalies = []

    # -----------------------------
    # Ghi anomaly vào InfluxDB v2
    # -----------------------------
    if not write_api:
        print("⚠️ InfluxDB client not initialized, skipping write.")
        return anomalies

    for a in anomalies:
        try:
            if isinstance(a, int) and timestamps and 0 <= a < len(timestamps):
                ts_val = int(timestamps[a])
            elif isinstance(a, (float, int)):
                ts_val = int(a)
            else:
                ts_val = int(time.time())
        except Exception:
            ts_val = int(time.time())

        try:
            p = (
                Point(metric_id)
                .tag("source", "baro_bocpd")
                .field("anomaly", 1)
                .time(ts_val, WritePrecision.S)
            )
            write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=p)
            print(f"[DEBUG] ✅ Wrote anomaly at {ts_val}")
        except Exception as e:
            print("❌ Influx write error:", e)

    return anomalies
