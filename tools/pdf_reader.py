try:
    import pymupdf
    _AVAILABLE = True
except ImportError:
    _AVAILABLE = False


def read_pdf(path: str, max_pages: int = 10) -> str:
    if not _AVAILABLE:
        return "Error: pymupdf is not installed. Run: pip install pymupdf"
    try:
        doc = pymupdf.open(path)
        pages = min(len(doc), max_pages)
        text = ""
        for i in range(pages):
            text += f"--- Page {i + 1} ---\n"
            text += doc[i].get_text()
        if len(doc) > max_pages:
            text += f"\n... (showing first {max_pages} of {len(doc)} pages)"
        return text.strip() or "(no text found in PDF)"
    except Exception as e:
        return f"Error reading PDF: {e}"
