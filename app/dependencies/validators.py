import re
import unicodedata
import validators
from typing import Optional, Tuple

class URLValidator:
    """URL validation utilities"""
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate if the provided URL is valid"""
        return validators.url(url)
    
    @staticmethod
    def sanitize_alias(alias: str) -> str:
        """Sanitize the alias removing special characters and applying security rules"""
        if not alias:
            return ""

        # Remove spaces at the beginning and end
        alias = alias.strip()

        # Convert to lowercase
        alias = alias.lower()

        # Remove accents and normalize unicode characters
        alias = unicodedata.normalize('NFD', alias)
        alias = ''.join(char for char in alias if unicodedata.category(char) != 'Mn')

        # Remove characters not allowed (keep only letters, numbers, hyphens and underscores)
        alias = re.sub(r'[^a-zA-Z0-9\-_]', '', alias)

        # Remove multiple hyphens/underscores consecutively
        alias = re.sub(r'[-_]{2,}', '-', alias)

        # Remove hyphens/underscores at the beginning and end
        alias = re.sub(r'^[-_]+|[-_]+$', '', alias)

        # Limit the size (maximum 50 characters)
        alias = alias[:50]

        return alias

    @staticmethod
    def validate_alias(alias: str) -> Tuple[bool, Optional[str]]:
        """Validate the sanitized alias. Returns: (is_valid, error_message)"""
        sanitized = URLValidator.sanitize_alias(alias)

        if not sanitized:
            return False, "Alias cannot be empty after sanitization"

        if len(sanitized) < 2:
            return False, "Alias must have at least 2 characters"

        # Check if it is only numbers
        if re.match(r'^\d+$', sanitized):
            return False, "Alias cannot be only numbers"

        # Check suspicious patterns
        suspicious_patterns = [
            r'^(admin|root|api|www|mail)$',  # System names
            r'^\d+$',  # Only numbers
            r'^[_-]+$',  # Only symbols
        ]

        for pattern in suspicious_patterns:
            if re.match(pattern, sanitized):
                return False, "This alias pattern is not allowed"

        return True, None
    
    @staticmethod
    def check_reserved_paths(short_id: str) -> bool:
        """Check if the ID is in the list of reserved paths"""
        reserved_paths = [
            "", "shorten", "stats", "docs", "ping",
            # Authentication
            "login", "register", "auth", "signin", "signup", "logout",
            # API and Next.js
            "api", "_next", "_vercel", "vercel",
            # Static assets
            "favicon", "favicon.ico", "robots", "robots.txt", "sitemap", "sitemap.xml",
            # Main pages of the user
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
        
        return short_id in reserved_paths 