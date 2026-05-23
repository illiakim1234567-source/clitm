import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent / "tasks.json"

def get_tasks() -> dict:
    if not DATA_FILE.exists():
        DATA_FILE.write_text("{}", encoding="utf-8")
    with DATA_FILE.open(encoding="utf-8") as f:
        return json.load(f)

def update_tasks(tasks: dict):
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=4, ensure_ascii=False)