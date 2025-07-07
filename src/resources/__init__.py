"""
Resources Module

Contains MCP resource definitions for data access and retrieval.
Resources provide read-only access to data that clients can consume.
"""

from .user_resources import register_resources

__all__ = [
    "register_resources",
]

# Resource URIs for reference
AVAILABLE_RESOURCES = [
    "data://users",
    "data://users/stats", 
    "data://users/report",
]

# Resource templates (parameterized resources)
AVAILABLE_RESOURCE_TEMPLATES = [
    "data://users/{user_name}",
    "test://user/{id}",
]