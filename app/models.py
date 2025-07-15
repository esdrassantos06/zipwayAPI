from pydantic import BaseModel
from typing import Optional

class URLBase(BaseModel):
    """
    Model to receive the URL data to be shortened.
    
    Attributes:
        target_url: Original URL to be shortened
        custom_id: Custom ID
    """        
    
    target_url: str
    custom_id: Optional[str] = None
    
class URLInfo(BaseModel):
    """
    Model to return the shortened url.
    
    Attributes:
        id: Unique identifier for the shortened url
        target_url: Original URL to be shortened
        short_url: Shortened Url
    """
    
    id: str
    target_url: str
    short_url: str