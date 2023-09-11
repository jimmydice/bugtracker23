import re

# Regular expression to match at least one special character
special_char_pattern = r'[!@#$%^&*(),.?":{}|<>]'

# Function to validate the password
def is_valid_password(password):
    # Check if the password is at least 6 characters long
    if len(password) < 6:
        return False

    # Check if the password contains at least one special character
    if not re.search(special_char_pattern, password):
        return False

    return True


