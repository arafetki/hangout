from random_username.generate import generate_username
from app.core.utils.constants import Constants


def generate_random_username() -> str:
    return generate_username(1)[0]


def is_valid_nanoid(id: str) -> bool:
    """Check if the given string is a valid NanoID."""
    if len(id) != Constants.NANOID_SIZE:
        return False
    return all(char in Constants.NANOID_ALPHABET for char in id)
