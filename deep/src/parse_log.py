import os
import json
import pandas as pd
from logparser.logparser import Drain

RAW_DIR = "data/raw/"
OUT_DIR = "data/structured/"
LOG_FILE = "HDFS_2k.log"

LOG_FORMAT = "<Date> <Time> <Pid> <Level> <Component>: <Content>"

REGEX = [
    r"(?<=blk_)[-\d]+",        # block id
    r"\d+\.\d+\.\d+\.\d+",     # IP
    r"(/[-\w]+)+",             # file path
]

def parse_hdfs():
    os.makedirs(OUT_DIR, exist_ok=True)

    parser = Drain.LogParser(
        log_format=LOG_FORMAT,
        indir=RAW_DIR,
        outdir=OUT_DIR,
        depth=5,
        st=0.5,
        rex=REGEX,
        keep_para=False
    )
    parser.parse(LOG_FILE)

def build_logkey_mapping():
    tpl = pd.read_csv(f"{OUT_DIR}/{LOG_FILE}_templates.csv")
    tpl.sort_values("Occurrences", ascending=False, inplace=True)

    mapping = {
        eid: idx + 1
        for idx, eid in enumerate(tpl["EventId"])
    }

    with open(f"{OUT_DIR}/hdfs_log_templates.json", "w") as f:
        json.dump(mapping, f)

if __name__ == "__main__":
    parse_hdfs()
    build_logkey_mapping()
