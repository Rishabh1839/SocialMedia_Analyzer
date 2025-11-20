from text_utils import clean_text, keyword_risk_score

# ----------------------------------------------------------
# Main Risk Score Function
# ----------------------------------------------------------
def calculate_risk_score(profile: dict) -> int:
    """
    Computes a risk score from multiple cybersecurity-related factors.

    Factors considered:
    - Suspicious keywords in posts
    - High follower/following imbalance
    - Username patterns
    - Email legitimacy
    - Posting behavior
    """
    score = 0

    # ------------------------------------------------------
    # 1. Keyword-based scoring (posts with risky content)
    # ------------------------------------------------------
    posts = profile.get("posts", [])
    score += keyword_risk_score(posts)

    # ------------------------------------------------------
    # 2. Follower/Following Ratio Scoring
    # ------------------------------------------------------
    followers = profile.get("followers", 0)
    following = profile.get("following", 1)

    if followers == 0:
        ratio = 0
    else:
        ratio = followers / following

    # Suspicious ratios
    if ratio > 5:
        score += 10    # influencer-like but suspicious
    elif ratio < 0.2:
        score += 12    # bot-like behavior
    elif 2 < ratio <= 5:
        score += 5     # mild imbalance

    # ------------------------------------------------------
    # 3. Username Pattern Analysis
    # ------------------------------------------------------
    username = clean_text(profile.get("username", "")).lower()

    if any(term in username for term in ["hack", "breach", "dark", "root", "admin"]):
        score += 15

    # Excessive numbers (bot-like)
    if sum(c.isdigit() for c in username) >= 4:
        score += 10

    # Very short usernames = suspicious
    if len(username) <= 4:
        score += 5

    # ------------------------------------------------------
    # 4. Email Pattern Analysis
    # ------------------------------------------------------
    email = clean_text(profile.get("email", "")).lower()

    # Temporary / suspicious domains
    risky_domains = ["protonmail.com", "tutanota.com", "tempmail.com", "mailinator.com"]
    if any(email.endswith(domain) for domain in risky_domains):
        score += 10

    # Randomized emails (bot-like)
    local_part = email.split("@")[0]
    if sum(c.isdigit() for c in local_part) >= 5:
        score += 8

    # ------------------------------------------------------
    # 5. Posting Activity
    # ------------------------------------------------------
    num_posts = len(posts)

    if num_posts == 0:
        score += 8  # empty account = suspicious
    elif num_posts > 20:
        score += 5  # spam-like posting

    # Repetitive or short posts (bot-like)
    for p in posts:
        if len(p) < 10:
            score += 2

    # ------------------------------------------------------
    return score


# ----------------------------------------------------------
# Convert Score to Risk Category for Display
# ----------------------------------------------------------
def risk_level(score: int) -> str:
    """
    Converts the risk score into a human-readable category.
    """
    if score >= 60:
        return "HIGH"
    elif score >= 35:
        return "MEDIUM"
    else:
        return "LOW"
