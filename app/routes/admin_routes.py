from fastapi import APIRouter, Depends, Request, Query

from ..controllers.admin_controller import get_admin_controller, AdminController
from ..dependencies.auth import AdminToken
from ..dependencies.limiter import limiter, DEFAULT_LIMITS
from ..views.admin_views import AdminStatsView, DeleteUrlResponse

admin_router = APIRouter(prefix="/admin", tags=["Admin"])

admin_auth = AdminToken()

@admin_router.get("/stats", response_model=AdminStatsView)
@limiter.limit(DEFAULT_LIMITS["admin"])
async def get_statistics(
    request: Request,
    limit: int = 20,
    token: str = Depends(admin_auth.__call__),
    controller: AdminController = Depends(get_admin_controller)
):
    """
    Return user statistics of the most popular URLs.
    Requires admin token.
    """
    return controller.get_statistics(limit)


@admin_router.delete("/delete_url", response_model=DeleteUrlResponse)
@limiter.limit(DEFAULT_LIMITS["admin"])
async def delete_short_url(
    request: Request,
    short_id: str = Query(..., description="The short ID of the URL to delete"),
    token: str = Depends(admin_auth.__call__),
    controller: AdminController = Depends(get_admin_controller)
):
    """
    Delete a shortened URL.
    Requires admin token.
    """
    return controller.delete_url(short_id)
