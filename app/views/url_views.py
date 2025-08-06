from pydantic import BaseModel
from datetime import datetime

class UrlStatsView(BaseModel):
    """
    View to represent the statistics of an individual URL
    """
    id: str
    target_url: str
    clicks: int
    created_at: datetime
    short_url: str

class UrlCreateView(BaseModel):
    """
    View to represent the creation of a short URL
    """
    id: str
    target_url: str
    short_url: str