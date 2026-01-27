import pandas as pd
import json

STRUCTURED_LOG = "data/structured/HDFS_2k.log_structured.csv"
MAPPING_FILE = "data/structured/hdfs_log_templates.json"

def build_global_sequence():
    df = pd.read_csv(
        STRUCTURED_LOG,
        dtype={"Date": str, "Time": str}
    )

    with open(MAPPING_FILE) as f:
        mapping = json.load(f)

    df["log_key"] = df["EventId"].apply(lambda x: mapping.get(x, -1))

    global_df = pd.DataFrame({
        "raw_idx": df.index,
        "timestamp": pd.to_datetime(
            df["Date"] + df["Time"],
            format="%y%m%d%H%M%S"
        ),
        "log_key": df["log_key"],
        "content": df["Content"]
    })

    global_df = global_df.sort_values("timestamp").reset_index(drop=True)
    return global_df

if __name__ == "__main__":
    g = build_global_sequence()
    print("ok chua????")
    g.to_csv("data/output/global_sequence.csv", index=False)
