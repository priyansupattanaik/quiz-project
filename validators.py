import re

# regex functions for validation
def validate_username(username):
    # 3 to 20 alphanumeric characters
    return bool(re.match(r"^[a-zA-Z0-9]{3,20}$", username))

def validate_password(password):
    # minimum 4 characters
    return bool(re.match(r"^.{4,}$", password))

def validate_answer(ans):
    # exactly one digit from 1 to 4
    return bool(re.match(r"^[1-4]$", ans.strip()))