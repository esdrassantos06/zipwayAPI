from pydantic import BaseModel, Field
from typing import Optional

class URLBase(BaseModel):
    target_url: str
    custom_id: Optional[str] = Field(None, alias="short_id")
    
    class Config:
        allow_population_by_field_name = True

class URLInfo(BaseModel):
    id: str
    target_url: str
    short_url: str