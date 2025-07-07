"""
Middleware Module

Contains MCP middleware definitions for request/response processing.
Middleware provides cross-cutting concerns like logging, validation, and security.
"""

from .custom_middleware import register_middleware

__all__ = [
    "register_middleware",
]

# Middleware classes for reference
AVAILABLE_MIDDLEWARE = [
    "ValidationMiddleware",
    "LoggingMiddleware", 
    "SecurityMiddleware",
]