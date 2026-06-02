def generate_summary(text):

    words = text.split()

    if len(words) <= 200:
        return text

    summary = " ".join(words[:200])

    return summary + " ..."