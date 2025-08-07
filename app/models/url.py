from sqlalchemy import Column, String, Integer, DateTime, func
from app.database import Base
from pydantic import BaseModel, Field
from typing import Optional

# Pydantic

class URLBase(BaseModel):
    target_url: str
    custom_id: Optional[str] = Field(None, alias="short_id")

    class Config:
        validate_by_name = True


class URLInfo(BaseModel):
    id: str
    target_url: str
    short_url: str



# SQLAlchemy

class URL(Base):
    __tablename__ = "urls"

    id = Column(String, primary_key=True, index=True)
    target_url = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    clicks = Column(Integer, default=0)