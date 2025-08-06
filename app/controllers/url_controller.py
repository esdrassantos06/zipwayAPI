from ..services.url_service import UrlService
from ..models._init_ import URLBase, URLInfo
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from ..repositories.url_repository import UrlRepository
from ..database import get_db

class UrlController:
    """
    Controller responsible for managing URL operations
    """

    def __init__(self, url_service: UrlService):
        self.url_service = url_service

    def create_short_url(self, url: URLBase) -> URLInfo:
        """
        Create a short URL
        """
        try:
            created_url = self.url_service.create_short(url)
            return URLInfo(
                id=created_url.id,
                target_url=created_url.target_url,
                short_url=f"/url/{created_url.id}"
            )
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    def get_short_url(self, short_id: str) -> URLInfo:
        """
        Get a short URL
        """
        url = self.url_service.get_short_url(short_id)
        if not url:
            raise HTTPException(status_code=404, detail="URL not found")
        
        return URLInfo(
            id=url.id,
            target_url=url.target_url,
            short_url=f"/url/{url.id}"
        )
    
    def increment_clicks(self, short_id: str) -> None:
        """
        Increment the clicks of a short URL
        """
        return self.url_service.increment_clicks(short_id)
    
    
    def redirect_target_url(self, short_id: str) -> str:
        """
        Return the target URL of a short URL
        """
        target_url = self.url_service.return_target_url(short_id)
        if not target_url:
            raise HTTPException(status_code=404, detail="URL not found")
        
        # Increment clicks when URL is accessed
        self.increment_clicks(short_id)
        
        return target_url
    
def get_url_controller(db: Session = Depends(get_db)) -> UrlController:
    """
    Factory function to create UrlController with its dependencies
    """
    url_repository = UrlRepository(db)
    url_service = UrlService(url_repository)
    return UrlController(url_service)