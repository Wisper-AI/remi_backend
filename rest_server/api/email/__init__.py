from fastapi import APIRouter

from .add_connection import router as add_connection_router
from .list_connections import router as list_connections_router
from .remove_connection import router as remove_connection_router

router = APIRouter(prefix="/api/v1/email", tags=["email"])
router.include_router(add_connection_router)
router.include_router(list_connections_router)
router.include_router(remove_connection_router)

__all__ = ["router"]
