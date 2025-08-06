from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
from ..services.url_service import UrlService
from ..repositories.url_repository import UrlRepository
from ..views.admin_views import AdminStatsView, DeleteUrlResponse
from ..views.url_views import UrlStatsView
from ..database import get_db


class AdminController:
    """
    Controller responsible for managing administrative operations
    """
    
    def __init__(self, url_service: UrlService):
        self.url_service = url_service
    
    def get_statistics(self, limit: int = 20) -> AdminStatsView:
        """
        Get statistics of the most popular URLs
        """
        try:
            url_objects = self.url_service.get_stats(limit)
            
            # Convert URL model objects to UrlStatsView objects
            stats_views = []
            for url_obj in url_objects:
                stats_view = UrlStatsView(
                    id=url_obj.id,
                    target_url=url_obj.target_url,
                    clicks=url_obj.clicks,
                    created_at=url_obj.created_at,
                    short_url=f"/url/{url_obj.id}"
                )
                stats_views.append(stats_view)
            
            return AdminStatsView(
                top_urls=stats_views,
                total=len(stats_views),
                limit=limit
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting statistics: {str(e)}")
    
    def delete_url(self, short_id: str) -> DeleteUrlResponse:
        """
        Delete a shortened URL
        """
        try:
            # Check if the URL exists
            url_data = self.url_service.get_short_url(short_id)
            if not url_data:
                raise HTTPException(status_code=404, detail="URL not found")
            
            # Delete the URL
            success = self.url_service.delete_url(short_id)
            if not success:
                raise HTTPException(status_code=500, detail="Failed to delete URL")
            
            return DeleteUrlResponse(
                message="URL deleted successfully",
                deleted_id=short_id
            )
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error deleting URL: {str(e)}")


# Factory function to create the controller with dependencies
def get_admin_controller(db: Session = Depends(get_db)) -> AdminController:
    """
    Factory function to create AdminController with its dependencies
    """
    url_repository = UrlRepository(db)
    url_service = UrlService(url_repository)
    return AdminController(url_service)
