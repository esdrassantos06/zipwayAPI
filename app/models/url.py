from sqlalchemy import Column, String, Integer, DateTime, func
from app.database import Base

class URL(Base):
    __tablename__ = "urls"

    id = Column(String, primary_key=True, index=True)
    target_url = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    clicks = Column(Integer, default=0)