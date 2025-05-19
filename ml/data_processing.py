import os
import json
import pandas as pd

def key_to_name(key):
    mapping = {"ArrowUp": "Up", "ArrowDown": "Down", "ArrowLeft": "Left", "ArrowRight": "Right"}
    return mapping.get(key, "Unknown")

def movements_to_sequence(movements):
    return [key_to_name(m.get('key')) for m in movements if 'key' in m]

def load_sessions(data_path):
    all_sessions = []
    for filename in os.listdir(data_path):
        if filename.endswith(".json"):
            with open(os.path.join(data_path, filename), 'r') as f:
                session = json.load(f)
                duration = session.get("duration_ms", 0)
                apples = session.get("applesEaten", 0)
                movements = session.get("movements", [])
                all_sessions.append({
                    "filename": filename,
                    "duration_ms": duration,
                    "applesEaten": apples,
                    "movements_count": len(movements)
                })
    df = pd.DataFrame(all_sessions)
    df["duration_sec"] = df["duration_ms"] / 1000
    return df
