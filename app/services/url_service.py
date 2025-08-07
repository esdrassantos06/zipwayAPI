from app.repositories.url_repository import UrlRepository
from ..models.url import URL, URLBase
from typing import List
import shortuuid
from ..dependencies.validators import URLValidator

class UrlService:
    def __init__(self, repo: UrlRepository):
        self.repo = repo

    def create_short(self, url_data: URLBase):
        if url_data.custom_id:
            sanitized_id = URLValidator.sanitize_alias(url_data.custom_id)
            is_valid, error_message = URLValidator.validate_alias(url_data.custom_id)
            
            if not is_valid:
                raise ValueError(error_message)
            
            if self.url_exists(sanitized_id):
                raise ValueError("Custom ID already exists")
            
            if URLValidator.check_reserved_paths(sanitized_id):
                raise ValueError("This ID is reserved and cannot be used")
            
            short_id = sanitized_id
        else:
            short_id = self.generate_short_id()
        
        if not URLValidator.validate_url(url_data.target_url):
            raise ValueError("Invalid URL provided")
        
        return self.repo.create(URL(id=short_id, target_url=url_data.target_url))

    def get_short_url(self, short_id: str):
        return self.repo.get(short_id=short_id)

    def increment_clicks(self, short_id: str):
        return self.repo.increment_clicks(short_id=short_id)

    def url_exists(self, short_id: str):
        return self.repo.exists(short_id)
    
    def get_stats(self, limit: int = 20) -> List[URL]:
        """Get statistics of the most clicked URLs"""
        return self.repo.stats(limit)
    
    def delete_url(self, short_id: str) -> bool:
        """Delete a shortened URL"""
        return self.repo.delete(short_id)
    
    def generate_short_id(self) -> str:
        """Generate a unique short ID"""
        while True:
            short_id = shortuuid.random(length=7)
            if not self.url_exists(short_id):
                return short_id
    
    def return_target_url(self, short_id: str) -> str | None:
        """Return the target URL of a short URL"""
        return self.repo.return_target_url(short_id)