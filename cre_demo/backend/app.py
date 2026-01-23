from fastapi import FastAPI, HTTPException
import pandas as pd
from joblib import load

app = FastAPI(title="Credit Risk Scoring API")

# Load trained pipeline (preprocess + model)
pipe = load("credit_model_pipeline.joblib")

# Load feature store (demo = CSV)
FEATURE_TABLE = pd.read_csv("data/feature_table.csv")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/predict/{customer_id}")
def predict(customer_id: int):
    row = FEATURE_TABLE[
        FEATURE_TABLE["SK_ID_CURR"] == customer_id
    ]

    if row.empty:
        raise HTTPException(
            status_code=404,
            detail="Customer ID not found"
        )

    X = row.drop(columns=["SK_ID_CURR"])

    pd_value = pipe.predict_proba(X)[0, 1]

    return {
        "customer_id": customer_id,
        "probability_of_default": round(float(pd_value), 4)
    }
