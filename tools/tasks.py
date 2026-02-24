import json
from pathlib import Path

DATA_FILE = Path(__file__).parent.parent / "data" / "tasks.json"


def _load() -> dict:
    if not DATA_FILE.exists():
        DATA_FILE.parent.mkdir(exist_ok=True)
        return {"tasks": [], "notes": []}
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def _save(data: dict) -> None:
    DATA_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def add_task(text: str) -> str:
    data = _load()
    new_id = max((t["id"] for t in data["tasks"]), default=0) + 1
    data["tasks"].append({"id": new_id, "text": text, "done": False})
    _save(data)
    return f"Task #{new_id} added."


def list_tasks() -> str:
    tasks = _load()["tasks"]
    if not tasks:
        return "No tasks."
    return "\n".join(
        f"[{'x' if t['done'] else ' '}] #{t['id']} {t['text']}" for t in tasks
    )


def complete_task(task_id: int) -> str:
    data = _load()
    for t in data["tasks"]:
        if t["id"] == task_id:
            t["done"] = True
            _save(data)
            return f"Task #{task_id} marked done."
    return f"Task #{task_id} not found."


def add_note(text: str) -> str:
    data = _load()
    new_id = max((n["id"] for n in data["notes"]), default=0) + 1
    data["notes"].append({"id": new_id, "text": text})
    _save(data)
    return f"Note #{new_id} saved."


def list_notes() -> str:
    notes = _load()["notes"]
    if not notes:
        return "No notes."
    return "\n".join(f"#{n['id']}: {n['text']}" for n in notes)
