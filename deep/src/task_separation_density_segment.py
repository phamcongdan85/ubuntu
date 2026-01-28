from collections import defaultdict

def build_transition_density(global_df, window=3):
    """
    Compute pd(i -> j) = freq(i, j) / freq(i)
    """
    freq = defaultdict(int)
    trans = defaultdict(int)

    keys = global_df["log_key"].tolist()

    for i in range(len(keys)):
        freq[keys[i]] += 1
        for j in range(i+1, min(i+window+1, len(keys))):
            trans[(keys[i], keys[j])] += 1

    pd = {
        (i, j): trans[(i, j)] / freq[i]
        for (i, j) in trans
    }
    return pd

def density_based_segmentation(global_df, pd, threshold=0.2):
    """
    Segment global sequence into tasks based on transition density
    """
    tasks = defaultdict(list)
    current_task = 0

    keys = global_df["log_key"].tolist()
    raw_idxs = global_df["raw_idx"].tolist()

    tasks[current_task].append(raw_idxs[0])

    for t in range(1, len(keys)):
        prev_k = keys[t-1]
        curr_k = keys[t]

        score = pd.get((prev_k, curr_k), 0)

        if score >= threshold:
            # continue same task
            tasks[current_task].append(raw_idxs[t])
        else:
            # break → new task
            current_task += 1
            tasks[current_task].append(raw_idxs[t])

    return tasks

def density_task_separation_segment(global_df, window=3, threshold=0.2):
    pd = build_transition_density(global_df, window)
    tasks = density_based_segmentation(global_df, pd, threshold)
    return tasks


