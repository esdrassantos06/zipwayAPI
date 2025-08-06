from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import RedirectResponse

from ..controllers.url_controller import get_url_controller, UrlController
from ..dependencies.limiter import limiter, DEFAULT_LIMITS
from ..models._init_ import URLBase
from ..views.url_views import UrlCreateView

url_router = APIRouter(prefix="/url", tags=["URLs"])

@url_router.get("/{short_id}")
@limiter.limit(DEFAULT_LIMITS["redirect"])
async def redirect_target_url(short_id: str, request: Request, controller: UrlController = Depends(get_url_controller)):
    """
    Redirect to the target URL of a short URL
    """
    try:
        target_url = controller.redirect_target_url(short_id)
        return RedirectResponse(url=target_url, status_code=307)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@url_router.post("/shorten", response_model=UrlCreateView)
@limiter.limit(DEFAULT_LIMITS["shorten"])
async def create_short_url(url: URLBase, request: Request, controller: UrlController = Depends(get_url_controller)):
    """
    Create a short URL
    """
    return controller.create_short_url(url)