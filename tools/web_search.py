from duckduckgo_search import DDGS


def web_search(query: str, max_results: int = 5) -> str:
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=max_results))
    if not results:
        return "No results found."
    lines = []
    for r in results:
        lines.append(f"Title: {r['title']}\nURL: {r['href']}\nSnippet: {r['body']}\n")
    return "\n".join(lines)
