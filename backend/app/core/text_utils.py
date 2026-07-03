import re
import unicodedata


def normalize_code(value: str) -> str:
    """Standardize identifier/code fields (equipment code, department code,
    username, borrow slip code) to unaccented Vietnamese, uppercase, hyphenated.

    Descriptive/free-text fields (names, notes, purpose) are NOT run through
    this — only fields that function as a "mã" (code/identifier).
    """
    value = value.strip().replace("Đ", "D").replace("đ", "d")
    value = unicodedata.normalize("NFD", value)
    value = "".join(c for c in value if unicodedata.category(c) != "Mn")
    value = value.upper()
    value = re.sub(r"[^A-Z0-9]+", "-", value).strip("-")
    return value
