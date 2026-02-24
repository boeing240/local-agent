import os
from pathlib import Path


def read_file(path: str) -> str:
    try:
        return Path(path).read_text(encoding="utf-8")
    except Exception as e:
        return f"Error reading file: {e}"


def write_file(path: str, content: str) -> str:
    try:
        Path(path).write_text(content, encoding="utf-8")
        return f"File written: {path}"
    except Exception as e:
        return f"Error writing file: {e}"


def search_files(directory: str, pattern: str) -> str:
    matches = []
    for root, dirs, files in os.walk(directory):
        for fname in files:
            full = os.path.join(root, fname)
            try:
                text = Path(full).read_text(encoding="utf-8", errors="ignore")
                if pattern.lower() in text.lower():
                    matches.append(full)
            except Exception:
                pass
    return "\n".join(matches) if matches else "No matches found."
