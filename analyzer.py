import sys
from mock_data import profiles
from text_utils import normalize_name, format_posts, safe_get
from scoring import calculate_risk_score, risk_level

# Terminal Colors
RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


# ----------------------------------------------------------
# Display Risk Level with Colors
# ----------------------------------------------------------
def colored_risk_text(level: str) -> str:
    if level == "HIGH":
        return f"{RED}{BOLD}HIGH RISK{RESET}"
    elif level == "MEDIUM":
        return f"{YELLOW}{BOLD}MEDIUM RISK{RESET}"
    else:
        return f"{GREEN}{BOLD}LOW RISK{RESET}"


# ----------------------------------------------------------
# Display Profile Information
# ----------------------------------------------------------
def display_profile(name: str, profile: dict):
    print(f"\n{CYAN}{BOLD}=== Social Media Profile Analysis ==={RESET}\n")

    print(f"{BOLD}Name:{RESET} {safe_get(profile, 'name')}")
    print(f"{BOLD}Username:{RESET} {safe_get(profile, 'username')}")
    print(f"{BOLD}Email:{RESET} {safe_get(profile, 'email')}")
    print(f"{BOLD}Profile Image:{RESET} {safe_get(profile, 'profile_image')}")
    
    print(f"\n{BOLD}Followers:{RESET} {safe_get(profile, 'followers')}")
    print(f"{BOLD}Following:{RESET} {safe_get(profile, 'following')}")

    # ------------------------------------------------------
    # Posts (with keyword highlighting)
    # ------------------------------------------------------
    print(f"\n{BOLD}Posts:{RESET}")

    formatted = format_posts(profile.get("posts", []))
    if not formatted:
        print(" - No posts available\n")
    else:
        for p in formatted:
            print(f" - {p}")

    # ------------------------------------------------------
    # Risk Scoring
    # ------------------------------------------------------
    score = calculate_risk_score(profile)
    level = risk_level(score)

    print(f"\n{BOLD}Risk Score:{RESET} {score}")
    print(f"{BOLD}Risk Level:{RESET} {colored_risk_text(level)}\n")

    print(f"{CYAN}{BOLD}======================================{RESET}\n")


# ----------------------------------------------------------
# Find profile by name (case-insensitive)
# ----------------------------------------------------------
def find_profile(input_name: str):
    normalized = normalize_name(input_name)

    # Normalize keys of mockdata
    for stored_name in profiles.keys():
        if normalize_name(stored_name) == normalized:
            return stored_name, profiles[stored_name]

    return None, None


# ----------------------------------------------------------
# Main Execution
# ----------------------------------------------------------
def main():
    print(f"{CYAN}{BOLD}Social Media Profile Analyzer{RESET}")
    print("Type a name to analyze (e.g., John Doe)\n")

    user_input = input("Enter profile name: ").strip()

    stored_key, profile = find_profile(user_input)

    if profile is None:
        print(f"\n{RED}{BOLD}Profile not found!{RESET}")
        print("Make sure you type the name exactly (e.g., John Doe)\n")
        sys.exit(1)

    display_profile(stored_key, profile)


if __name__ == "__main__":
    main()
