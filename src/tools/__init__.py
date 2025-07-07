"""
Tools Module

Contains MCP tool definitions for user data management operations.
Tools provide executable functions that clients can call to perform actions.
"""

from .user_tools import register_tools

__all__ = [
    "register_tools",
]

# Tool names for reference
AVAILABLE_TOOLS = [
    "write_user",
    "get_user_count", 
    "analyze_users",
    "bulk_add_users",
    "process_users_simulation",
]