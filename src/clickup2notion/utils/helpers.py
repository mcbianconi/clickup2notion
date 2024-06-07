def split_text(text, max_length=2000):
    if not text:
        return [""]
    return [text[i : i + max_length] for i in range(0, len(text), max_length)]
