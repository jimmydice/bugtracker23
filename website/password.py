import re

# Match at least one special character
special_char_pattern = r'[!@#$%^&*(),.?":{}|<>]'

# Function to validate the password
def is_valid_password(password):
    """
    Validates a password based on the following criteria:
    
    1. The password must be at least 6 characters long.
    2. The password must contain at least one special character.
    
    Args:
        password (str): The password to be validated.

    Returns:
        bool: True if the password meets the criteria, False otherwise.
    """
    # Check if the password is at least 6 characters long
    if len(password) < 6:
        return False

    # Check if the password contains at least one special character
    if not re.search(special_char_pattern, password):
        return False

    return True


