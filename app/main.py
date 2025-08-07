from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager

from app.dependencies.limiter import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.routes.admin_routes import admin_router
from app.routes.url_routes import url_router
from app.database import init_db

load_dotenv()

PORT = int(os.getenv("PORT", 8000))
HOST = os.getenv("HOST", "0.0.0.0")
ENV = os.getenv("ENV", "development")  # development, staging, production


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler to initialize resources on startup.
    """
    init_db()
    yield


app = FastAPI(
    title="Zipway - Url Shortener", 
    description="A simple and efficient URL shortening service", 
    version="2.0.0",
    lifespan=lifespan
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

allow_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")

if ENV != "production":
    allow_origins.append("http://localhost:3000")
    allow_origins.append("http://frontend:3000")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
    allow_credentials=True
)

app.include_router(admin_router)
app.include_router(url_router)


@app.get("/", tags=["Information"])
async def root():
    """
    Returns basic information about the API and its endpoints.
    """
    return {
        "app": "URL Shortener",
        "version": "2.0.0",
        "endpoints": {
            "POST /shorten": "Create a Short URL",
            "GET /{short_id}": "Redirect to the original URL",
            "GET admin/stats": "Get use stats",
            "GET /docs": "Redirect to the docs",
            "GET /admin/delete-url": "Delete the URL"
        }
    }


@app.get("/ping", tags=["Health"])
@app.head("/ping", tags=["Health"])
async def ping():
    """
    Health check endpoint.
    """
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=True)
