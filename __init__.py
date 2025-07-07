"""
MCP User Data Server

A comprehensive MCP server template using FastMCP with file-based storage.
Provides tools, resources, and prompts for managing user data with context support,
progress reporting, and middleware capabilities.
"""

__version__ = "1.0.0"
__author__ = "MCP Server Template"
__description__ = "FastMCP server template for user data management"

# Main server entry point
from .main import main

# Component registration functions
from .src.tools.user_tools import register_tools
from .src.resources.user_resources import register_resources
from .src.prompts.user_prompts import register_prompts
from .src.middleware.custom_middleware import register_middleware

__all__ = [
    "main",
    "register_tools",
    "register_resources", 
    "register_prompts",
    "register_middleware",
]