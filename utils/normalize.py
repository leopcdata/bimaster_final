import re

def normalize_name(name):
    """
    Normalize a company name by:
      - Converting to lowercase
      - Removing trailing dots, commas, apostrophes, hyphens and quotes
      - Removing common business words
      - Removing extra whitespace
    """
    if not isinstance(name, str):
        return ""

    normalized = name.lower().strip().replace("\xa0", " ")

    if normalized.endswith("."):
        normalized = normalized[:-1]

    normalized = re.sub(r"[,\-\'\"]", "", normalized)

    remove_words = [
        "inc", "s/a", "sa", "ltda", "company", "corporation", "lp", "llp",
        "ltd", "llc", "co", "corp", "limited", "the", "incorporated",
        "holding", "group"
    ]
    pattern = r"\b(?:" + "|".join(remove_words) + r")\b"
    normalized = re.sub(pattern, "", normalized)

    normalized = re.sub(r"\s+", " ", normalized)
    return normalized.strip()

