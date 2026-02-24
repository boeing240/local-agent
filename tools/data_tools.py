import csv
import json
from pathlib import Path


def read_csv(path: str, max_rows: int = 50) -> str:
    try:
        with open(path, encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            rows = []
            for i, row in enumerate(reader):
                if i >= max_rows:
                    rows.append(f"... (showing first {max_rows} rows)")
                    break
                rows.append(str(dict(row)))
            if not rows:
                return "(empty file)"
            return "\n".join(rows)
    except Exception as e:
        return f"Error reading CSV: {e}"


def read_json(path: str) -> str:
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return json.dumps(data, indent=2, ensure_ascii=False)
    except Exception as e:
        return f"Error reading JSON: {e}"


def analyze_csv(path: str) -> str:
    try:
        with open(path, encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        if not rows:
            return "Empty CSV file."
        columns = list(rows[0].keys())
        return (
            f"Rows: {len(rows)}\n"
            f"Columns ({len(columns)}): {', '.join(columns)}\n\n"
            f"First row sample:\n{json.dumps(rows[0], ensure_ascii=False, indent=2)}"
        )
    except Exception as e:
        return f"Error analyzing CSV: {e}"
