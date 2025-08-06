from pydantic import BaseModel
from typing import List, Optional
from app.views.url_views import UrlStatsView


class AdminStatsView(BaseModel):
    """
    View to represent the statistics of an individual URL
    """
    top_urls: List[UrlStatsView]
    total: int
    limit: int
    message: Optional[str] = "Statistics obtained successfully"


class DeleteUrlResponse(BaseModel):
    """
    View to represent the response of the URL deletion
    """
    message: str
    deleted_id: str
    success: bool = True
