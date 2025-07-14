"""
API route definitions
"""
from .auth import router as auth_router
from .projects import router as projects_router
from .nodes import router as nodes_router
from .hardware import router as hardware_router
from .io import router as io_router

__all__ = [
    "auth_router",
    "projects_router", 
    "nodes_router",
    "hardware_router",
    "io_router"
]