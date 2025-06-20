from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request, Depends, status
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import shortuuid
import os
from dotenv import load_dotenv
import validators
import logging
import re
import unicodedata
from typing import Optional


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

from .models import URLBase, URLInfo
from .database import (
    createTable,
    insert_url,
    get_url_by_id,
    increment_clicks,
    check_id_exists,
    get_url_stats,
    delete_url
)
from .auth import validate_admin_token
from .limiter import limiter, _rate_limit_exceeded_handler, RateLimitExceeded, DEFAULT_LIMITS
load_dotenv()

PORT = int(os.getenv("PORT", 8000))
HOST = os.getenv("HOST", "0.0.0.0")
ENV = os.getenv("ENV", "development")  # development, staging, production

@asynccontextmanager
async def lifespan(app: FastAPI):
    createTable()
    yield

app = FastAPI(title="Zipway - Url Shortener (API VERSION)", description="A simple and efficient URL shortening service", version="1.0.0", lifespan=lifespan)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

allow_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")

if ENV != "production":
    allow_origins.append("http://localhost:3000")
    allow_origins.append("http://frontend:3000")
    
app.add_middleware(
    CORSMiddleware,
    allow_origins= allow_origins,
    allow_methods=["GET", "POST", "PUT", "DELETE"], 
    allow_headers=["*"],
    allow_credentials=True
)

@app.get("/", tags=["Information"])
async def root(): 
    return {
        "app": "URL Shortener",
        "version": "1.0.0",
        "endpoints": {
            "POST /shorten": "Create a Short URL",
            "GET /{short_id}": "Redirect to the original URL",
            "GET /stats": "Get use stats"
        }
    }
    
@app.get("/ping", tags=["Health"])
@app.head("/ping", tags=["Health"])
async def ping():
    return {"status": "ok"}
    
def sanitize_alias(alias: str) -> str:
    """
    Sanitizes the alias by removing special characters and applying security rules
    """
    if not alias:
        return ""
    
    # Remove spaces at the beginning and end
    alias = alias.strip()
    
    # Convert to lowercase
    alias = alias.lower()
    
    # Remove accents and normalize unicode characters
    alias = unicodedata.normalize('NFD', alias)
    alias = ''.join(char for char in alias if unicodedata.category(char) != 'Mn')
    
    # Remove disallowed characters (keep only letters, numbers, hyphens, and underscores)
    alias = re.sub(r'[^a-zA-Z0-9\-_]', '', alias)
    
    # Remove multiple consecutive hyphens/underscores
    alias = re.sub(r'[-_]{2,}', '-', alias)
    
    # Remove hyphens/underscores at the beginning and end
    alias = re.sub(r'^[-_]+|[-_]+$', '', alias)
    
    # Limit size (max 50 characters)
    alias = alias[:50]
    
    return alias

def validate_alias(alias: str) -> tuple[bool, Optional[str]]:
    """
    Validates the sanitized alias
    Returns: (is_valid, error_message)
    """
    sanitized = sanitize_alias(alias)
    
    if not sanitized:
        return False, "Alias cannot be empty after sanitization"
    
    if len(sanitized) < 2:
        return False, "Alias must have at least 2 characters"
    
    # Check if it's only numbers
    if re.match(r'^\d+$', sanitized):
        return False, "Alias cannot be only numbers"
    
    # Check for suspicious patterns
    suspicious_patterns = [
        r'^(admin|root|api|www|mail)$',  # System names
        r'^\d+$',  # Only numbers
        r'^[_-]+$',  # Only symbols
    ]
    
    for pattern in suspicious_patterns:
        if re.match(pattern, sanitized):
            return False, "This alias pattern is not allowed"
    
    return True, None


@app.post("/shorten", response_model=URLInfo, tags=["URLs"])
@limiter.limit(DEFAULT_LIMITS["shorten"])
async def create_short_url(url: URLBase, request: Request):
    if not validators.url(url.target_url):
        raise HTTPException(status_code=400, detail="Invalid URL format. Please provide a valid URL.")
        
    reserved_paths = [
        "", "shorten", "stats", "docs", "ping",
        # Authentication
        "login", "register", "auth", "signin", "signup", "logout",
        # API and Next.js
        "api", "_next", "_vercel", "vercel",
        # Static assets
        "favicon", "favicon.ico", "robots", "robots.txt", "sitemap", "sitemap.xml",
        # Main user pages
        "home", "dashboard", "profile", "settings", "admin", "user", "account",
        # Institutional pages
        "about", "contact", "help", "support", "terms", "privacy", "policy",
        # System resources
        "public", "static", "assets", "images", "img", "css", "js", "fonts",
        # Error pages
        "404", "500", "error", "not-found",
        # Webhooks and integrations
        "webhook", "webhooks", "callback", "oauth",
        # Monitoring and system
        "health", "status", "metrics", "monitoring", "ping",
        # Other common paths
        "www", "mail", "email", "ftp", "blog", "news", "shop", "store",
        # Admin area
        "administrator", "manage", "management", "console",
        # Additional resources
        "download", "upload", "file", "files", "media"
    ]

    
    if url.custom_id:
        sanitized_alias = sanitize_alias(url.custom_id)
        
        is_valid, error_message = validate_alias(sanitized_alias)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_message)
        
        short_id = sanitized_alias
        
        if short_id in reserved_paths:
            raise HTTPException(status_code=400, detail="This custom ID is reserved for system use. Please choose another one.")
        
        if check_id_exists(short_id):
            raise HTTPException(status_code=400, detail="Custom ID already exists")

    else: 
        while True:
            short_id = shortuuid.uuid()[:7]
            if not check_id_exists(short_id):
                break
    
    success = insert_url(short_id, url.target_url)
    if not success:
        raise HTTPException(status_code=500, detail="Error saving URL")
    
    base_url = os.getenv("BASE_URL")
    short_url = f"{base_url}/{short_id}"
    
    return URLInfo(id=short_id, target_url=url.target_url, short_url=short_url)
    


@app.get("/stats", tags=["Statistics"])
@limiter.limit(DEFAULT_LIMITS["admin"])
async def get_statistics(request: Request, limit: int= 10, token: str = Depends(validate_admin_token)):
    stats = get_url_stats(limit)
    return {
        "top_urls": stats,
        "total": len(stats)
    }

    
@app.get("/{short_id}", tags=["URLs"])
@limiter.limit(DEFAULT_LIMITS["redirect"])
async def redirect_to_target(short_id: str, request: Request):
    
    url_data = get_url_by_id(short_id)
    
    if not url_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Short URL not found")

    
    increment_clicks(short_id)
    
    return RedirectResponse(url=url_data["target_url"])

@app.delete("/delete_url", tags=["URLs"])
@limiter.limit(DEFAULT_LIMITS["admin"])
async def delete_short_url(short_id: str, request: Request, token: str = Depends(validate_admin_token)):
    
    url_data = get_url_by_id(short_id)
    
    if not url_data:
        raise HTTPException(status_code=404, detail="URL not found")
    
    success = delete_url(short_id)
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete URL")
    
    return {"detail": "URL deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=True)