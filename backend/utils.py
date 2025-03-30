import string
import random
import hashlib
import base64

def generate_short_code(url:string, length: int = 6):
    hash_digest = hashlib.sha256(url.encode()).digest()
    encoded = base64.urlsafe_b64encode(hash_digest).decode()
    return encoded[:length]    

def validate_url(url: str):
    if not url.startswith(("http://", "https://")):
        raise ValueError("Invalid URL format")
    return True

