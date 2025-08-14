import secrets
import string

ALPHABET = string.ascii_letters + string.digits  # base62


def generate_code(length: int = 7) -> str:
    """Generate a URL-safe short code using base62 characters."""
    return ''.join(secrets.choice(ALPHABET) for _ in range(length))