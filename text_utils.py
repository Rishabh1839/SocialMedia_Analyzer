import re

# ---------------------------------------------
# Clean and Normalize Text
# ---------------------------------------------
def clean_text(text: str) -> str:
    """
    Removes extra spaces, line breaks, and weird characters.
    """
    if not isinstance(text, str):
        return ""

    # Remove non-printable chars & trim
    cleaned = re.sub(r'[^\x20-\x7E]+', '', text)
    return cleaned.strip()


def normalize_name(name: str) -> str:
    """
    Converts the input name to a standardized format for dictionary lookup.
    Example:
        '  john  DOE ' -> 'john doe'
    """
    if not isinstance(name, str):
        return ""
    name = clean_text(name)
    name = name.lower()
    
    # Collapse multiple spaces
    name = re.sub(r'\s+', ' ', name)
    return name


# ---------------------------------------------
# Keyword Highlighting
# ---------------------------------------------
SUSPICIOUS_KEYWORDS = [
    "breach", "hack", "password", "leak", "leaked",
    "malware", "hackers", "compromised", "ransom",
    "ddos", "dark web", "breached", "phishing",
    "exploit", "zero-day", "sold", "illegal"
]

def highlight_keywords(text: str) -> str:
    """
    Highlights suspicious keywords in text.
    Used to visually alert users.
    """
    cleaned = clean_text(text)

    for keyword in SUSPICIOUS_KEYWORDS:
        pattern = re.compile(rf"\b{re.escape(keyword)}\b", re.IGNORECASE)
        cleaned = pattern.sub(f"[!! {keyword.upper()} !!]", cleaned)

    return cleaned


# ---------------------------------------------
# Extract Fields Safely
# ---------------------------------------------
def safe_get(data: dict, key: str, default="N/A"):
    """
    Safely retrieves a dictionary value.
    Prevents KeyErrors and ensures consistent output.
    """
    return data.get(key, default)


# ---------------------------------------------
# Keyword Scanner (for risk scoring system)
# ---------------------------------------------
def keyword_risk_score(posts: list) -> int:
    """
    Returns a risk score based on the number of suspicious keywords across posts.
    This works together with analyzer.py.
    """
    score = 0

    for post in posts:
        text = clean_text(post).lower()
        for word in SUSPICIOUS_KEYWORDS:
            if word in text:
                score += 5  # every hit increases risk

    return score


# ---------------------------------------------
# Post Analyzer (formatting)
# ---------------------------------------------
def format_posts(posts: list) -> list:
    """
    Returns posts with highlighted suspicious keywords.
    """
    formatted = []
    for post in posts:
        formatted.append(highlight_keywords(post))
    return formatted
