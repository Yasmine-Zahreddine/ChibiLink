from fastapi import HTTPException, Request
from datetime import datetime, timedelta, timezone
from collections import defaultdict

class RateLimiter:
    def __init__(self, max_requests: int = 10, window: int = 60):
        self.max_requests = max_requests
        self.window = window
        self.requests = defaultdict(list)

    async def check_rate_limit(self, request: Request):
        client_ip = request.client.host
        now = datetime.now(timezone.utc)  # Use UTC timezone
        
        # Clean up old timestamps
        self.requests[client_ip] = [
            timestamp for timestamp in self.requests[client_ip]
            if now - timestamp < timedelta(seconds=self.window)
        ]

        # Check if rate limit is exceeded
        if len(self.requests[client_ip]) >= self.max_requests:
            raise HTTPException(
                status_code=429,  # Using standard rate limit status code
                detail=f"Rate limit exceeded. Try again in {self.window} seconds."
            )

        self.requests[client_ip].append(now)

def protect_against_spam(url: str) -> bool:
    spam_indicators = [
        "spam", "malware", "phishing",
        ".exe", ".bat", ".dll",
        "bitcoin", "crypto"
    ]
    
    url_lower = url.lower()
    return not any(indicator in url_lower for indicator in spam_indicators)