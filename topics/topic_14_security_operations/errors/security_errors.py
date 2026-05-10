"""Security validation errors."""
def require_secret(secret):
    if not isinstance(secret, str): raise TypeError("secret must be a string")
    if len(secret) < 8: raise ValueError("secret must be at least 8 characters")
    return secret
