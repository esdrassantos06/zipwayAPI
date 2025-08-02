from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

DEFAULT_LIMITS = {
    "general": "100/minute",
    "shorten": "20/minute",     
    "redirect": "200/minute",
    "admin": "10/minute"
}