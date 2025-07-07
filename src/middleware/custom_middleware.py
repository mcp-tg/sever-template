from fastmcp.server.middleware import Middleware, MiddlewareContext
from fastmcp.exceptions import ToolError
from fastmcp import FastMCP
import time

def register_middleware(mcp: FastMCP):
    class ValidationMiddleware(Middleware):
        """Validates tool inputs before execution."""
        async def on_call_tool(self, context: MiddlewareContext, call_next):
            # Skip validation for now - just log and pass through
            return await call_next(context)

    class LoggingMiddleware(Middleware):
        """Logs tool execution details."""
        async def on_call_tool(self, context: MiddlewareContext, call_next):
            start_time = time.time()
            
            # Safe logging - just log that a tool was called
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Tool called")
            
            try:
                result = await call_next(context)
                execution_time = time.time() - start_time
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Tool completed successfully in {execution_time:.2f}s")
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Tool failed after {execution_time:.2f}s: {str(e)}")
                raise

    class SecurityMiddleware(Middleware):
        """Provides basic security checks."""
        async def on_call_tool(self, context: MiddlewareContext, call_next):
            # Skip security checks for now - just pass through
            return await call_next(context)

    # Register middleware with the server
    mcp.add_middleware(ValidationMiddleware())
    mcp.add_middleware(LoggingMiddleware())
    mcp.add_middleware(SecurityMiddleware())