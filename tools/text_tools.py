def translate_text(text: str, target_language: str) -> str:
    return f"Translate the following text to {target_language}. Return only the translation:\n\n{text}"


def summarize_text(text: str, max_sentences: int = 3) -> str:
    return f"Summarize the following text in {max_sentences} sentences. Return only the summary:\n\n{text}"


def generate_code(description: str, language: str = "Python") -> str:
    return f"Write {language} code for the following task. Return only the code with brief comments:\n\n{description}"
