try:
    import pyperclip
    _AVAILABLE = True
except ImportError:
    _AVAILABLE = False


def clipboard_read() -> str:
    if not _AVAILABLE:
        return "Error: pyperclip is not installed. Run: pip install pyperclip"
    text = pyperclip.paste()
    return text if text else "(clipboard is empty)"


def clipboard_write(text: str) -> str:
    if not _AVAILABLE:
        return "Error: pyperclip is not installed. Run: pip install pyperclip"
    pyperclip.copy(text)
    return "Text copied to clipboard."
