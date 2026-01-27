from collections import defaultdict

def density_task_separation(global_df, window=3, threshold=0.3):
    freq = defaultdict(int)
    co = defaultdict(int)

    keys = global_df["log_key"].tolist()

    for i in range(len(keys)):
        freq[keys[i]] += 1
        for j in range(i+1, min(i+window+1, len(keys))):
            co[(keys[i], keys[j])] += 1

    graph = defaultdict(set)
    for (i, j), v in co.items():
        if v / freq[i] >= threshold:
            graph[i].add(j)

    tasks = defaultdict(list)
    for idx, row in global_df.iterrows():
        key = row["log_key"]
        assigned = False
        for t, nodes in tasks.items():
            if key in nodes:
                tasks[t].append(row["raw_idx"])
                assigned = True
                break
        if not assigned:
            tasks[len(tasks)] = [row["raw_idx"]]

    return tasks
