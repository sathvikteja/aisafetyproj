import re

def parse_prompts(text):
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    prompts = []
    for line in lines:
        # Remove leading numbering/bulleting (e.g. "1.", "2)", "-", "*", "+")
        cleaned = re.sub(r"^\s*(?:\d+[\.)]|[\-\*\+])\s*", "", line)
        # If line is clearly a multiple-choice option (A), B), etc.), skip
        if re.match(r"^[A-Z]\)", cleaned):
            continue
        cleaned = cleaned.strip()
        if cleaned:
            prompts.append(cleaned)
    return prompts


def parse_verdict(text):
    if "UNSAFE" in text:
        return "UNSAFE"
    return "SAFE"