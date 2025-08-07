from sqlalchemy.orm import Session

from ..models.url import URL


class UrlRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, url: URL) -> URL:
        self.db.add(url)
        self.db.commit()
        self.db.refresh(url)
        return url

    def get(self, short_id: str) -> URL | None:
        return self.db.query(URL).filter(URL.id == short_id).first()

    def increment_clicks(self, short_id: str) -> None:
        short_url = self.get(short_id)
        if short_url:
            short_url.clicks += 1
            self.db.commit()

    def exists(self, short_id: str) -> bool:
        return self.db.query(URL.id).filter(URL.id == short_id).first() is not None

    def stats(self, limit: int = 20):
        return self.db.query(URL).order_by(URL.clicks.desc()).limit(limit).all()

    def delete(self, short_id: str) -> bool:
        short_url = self.get(short_id)
        if short_url:
            self.db.delete(short_url)
            self.db.commit()
            return True
        return False

    def return_target_url(self, short_id: str) -> str | None:
        short_url = self.get(short_id)
        if short_url:
            return short_url.target_url
        return None
