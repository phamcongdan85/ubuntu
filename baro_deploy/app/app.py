# app/app.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import time
from bocpd_wrapper import detect_and_write

# --------------------------------------------
# FastAPI application khởi tạo
# --------------------------------------------
app = FastAPI(title="BARO BOCPD API")


# --------------------------------------------
# Định nghĩa schema cho input payload
# --------------------------------------------
class IngestPoint(BaseModel):
    metric_id: str
    timestamps: Optional[List[int]] = None  # list of epoch seconds
    columns: List[str]
    data: List[List[float]]  # mỗi hàng là 1 timestep vector khớp với columns


# --------------------------------------------
# API: POST /ingest
# --------------------------------------------
@app.post("/ingest")
def ingest(payload: IngestPoint):
    """
    Nhận một batch dữ liệu thời gian cho 1 metric (chuỗi đa biến).
    Ví dụ payload:
    {
      "metric_id": "serviceA_latency",
      "timestamps": [169...,169...],
      "columns": ["latency","error_rate"],
      "data": [[100,0.01],[120,0.03],...]
    }
    """
    start = time.time()
    anomalies = detect_and_write(
        payload.metric_id,
        payload.timestamps,
        payload.columns,
        payload.data
    )
    dur = time.time() - start
    return {"status": "ok", "anomalies": anomalies, "took": dur}


# --------------------------------------------
# API: GET /health
# --------------------------------------------
@app.get("/health")
def health():
    """Endpoint kiểm tra tình trạng API"""
    return {"status": "ok"}
