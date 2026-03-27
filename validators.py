import re

# -------------------------------------------------------
# validators.py — Input validation using Regular Expressions
# Requirement: Regex-based validation
# -------------------------------------------------------

def validate_username(username):
    """
    Username: 3 to 20 characters, letters and digits only.
    """
    pattern = r"^[a-zA-Z0-9]{3,20}$"
    try:
        return bool(re.match(pattern, username))
    except Exception as e:
        print(f"[VALIDATION ERROR] {e}")
        return False


def validate_password(password):
    """
    Password: minimum 4 characters, any characters allowed.
    """
    pattern = r"^.{4,}$"
    try:
        return bool(re.match(pattern, password))
    except Exception as e:
        print(f"[VALIDATION ERROR] {e}")
        return False


def validate_answer(answer_str):
    """
    Quiz answer: exactly one digit from 1 to 4.
    """
    pattern = r"^[1-4]$"
    try:
        return bool(re.match(pattern, answer_str.strip()))
    except Exception as e:
        print(f"[VALIDATION ERROR] {e}")
        return False
