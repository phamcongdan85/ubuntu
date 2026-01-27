import re
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score

def extract_blockid(global_df):
    gt = {}
    for _, row in global_df.iterrows():
        blk = re.findall(r"(blk_-?\d+)", row["content"])
        gt[row["raw_idx"]] = blk[0] if blk else None
    return gt

def evaluate(tasks, gt_blockid):
    y_true, y_pred = [], []

    for task_id, rows in tasks.items():
        for r in rows:
            if gt_blockid[r] is not None:
                y_true.append(gt_blockid[r])
                y_pred.append(task_id)

    return {
        "ARI": adjusted_rand_score(y_true, y_pred),
        "NMI": normalized_mutual_info_score(y_true, y_pred)
    }
