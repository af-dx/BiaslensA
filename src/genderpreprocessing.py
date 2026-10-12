"""Shared text preprocessing — imported by both training and serving."""
import re

MENTION_RE = re.compile(r"MENTION\d+")

def tokenize(text):
    """Lowercase, collapse mention IDs, strip leading RT."""
    toks = MENTION_RE.sub("<mention>", str(text)).lower().split()
    return toks[1:] if toks and toks[0] == "rt" else toks
