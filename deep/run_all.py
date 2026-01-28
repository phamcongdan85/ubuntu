from src.build_global_sequence import build_global_sequence
from src.task_separation_density import density_task_separation
from src.task_separation_lstm import lstm_task_separation
from src.task_separation_density_segment import density_task_separation_segment
from src.evaluation import extract_blockid, evaluate

global_df = build_global_sequence()
gt = extract_blockid(global_df)

# tasks_density = density_task_separation(global_df)

tasks_density = density_task_separation_segment(
    global_df,
    window=3,
    threshold=0.2
)

print(tasks_density[:5])
tasks_lstm = lstm_task_separation(global_df)

print("Density-based:", evaluate(tasks_density, gt))
print("LSTM-based:", evaluate(tasks_lstm, gt))
