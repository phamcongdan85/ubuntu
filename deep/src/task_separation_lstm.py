import numpy as np
from collections import defaultdict
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense

def lstm_task_separation(global_df, window=10, epochs=3):
    keys = global_df["log_key"].tolist()
    max_key = max(keys) + 1

    X, y = [], []
    for i in range(len(keys) - window):
        X.append(keys[i:i+window])
        y.append(keys[i+window])

    X, y = np.array(X), np.array(y)

    model = Sequential([
        Embedding(max_key, 32),
        LSTM(64),
        Dense(max_key, activation="softmax")
    ])
    model.compile("adam", "sparse_categorical_crossentropy")
    model.fit(X, y, epochs=epochs, batch_size=128, verbose=1)

    tasks = defaultdict(list)
    for i in range(len(keys) - window):
        pred = np.argmax(model.predict(X[i:i+1], verbose=0))
        tasks[pred].append(global_df.iloc[i]["raw_idx"])

    return tasks
