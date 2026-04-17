def chunk_text(text: str, max_chars: int = 1000, overlap: int = 200) -> list[str]:
    """Split text into overlapping chunks by character count.

    Simple char-based splitter. Tries to break at newlines/periods
    within the max_chars window.
    """
    if len(text) <= max_chars:
        return [text] if text.strip() else []

    chunks: list[str] = []
    start = 0

    while start < len(text):
        end = start + max_chars

        if end < len(text):
            # try to break at newline or period
            for sep in ["\n\n", "\n", ". "]:
                break_at = text.rfind(sep, start + max_chars // 2, end)
                if break_at != -1:
                    end = break_at + len(sep)
                    break

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        start = end - overlap if end < len(text) else len(text)

    return chunks
