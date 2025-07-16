"""
Legacy API routes for backward compatibility
"""
from fastapi import APIRouter

# Create a basic router for legacy API endpoints
legacy_router = APIRouter(
    prefix="",
    tags=["legacy"],
    responses={404: {"description": "Not found"}},
)

@legacy_router.get("/legacy/health")
async def legacy_health_check():
    """Legacy health check endpoint"""
    return {"status": "ok", "message": "Legacy API is running"}
