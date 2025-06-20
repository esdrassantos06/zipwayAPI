from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)

DEFAULT_LIMITS = {
    "general": "100/minute",
    "shorten": "20/minute",     
    "redirect": "200/minute",
    "admin": "10/minute"
}