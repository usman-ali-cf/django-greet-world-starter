"""
Pydantic schemas (DTOs)
"""
from .auth import LoginRequest, UserResponse, Token
from .project import ProjectBase, ProjectCreate, ProjectResponse, NodeBase, NodeCreate, NodeResponse
from .hardware import HardwareResponse, HardwareNodeCreate, HardwareNodeResponse
from .io import IOBase, IOResponse, IOAssignRequest, IORemoveRequest

__all__ = [
    "LoginRequest", "UserResponse", "Token",
    "ProjectBase", "ProjectCreate", "ProjectResponse", 
    "NodeBase", "NodeCreate", "NodeResponse",
    "HardwareResponse", "HardwareNodeCreate", "HardwareNodeResponse",
    "IOBase", "IOResponse", "IOAssignRequest", "IORemoveRequest"
]