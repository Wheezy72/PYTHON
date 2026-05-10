"""HMAC signing helpers."""
import hmac, hashlib

def sign_message(secret, message):
    return hmac.new(secret.encode(), message.encode(), hashlib.sha256).hexdigest()

def verify_signature(secret, message, signature):
    return hmac.compare_digest(sign_message(secret, message), signature)
