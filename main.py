import os
from fastmcp import FastMCP
from src.tools.user_tools import register_tools
from src.resources.user_resources import register_resources
from src.prompts.user_prompts import register_prompts
from src.middleware.custom_middleware import register_middleware

def main():
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    # Create MCP server
    mcp = FastMCP("UserDataServer")
    
    # Register components
    register_middleware(mcp)  # Re-enabled with simplified middleware
    register_tools(mcp)
    register_resources(mcp)
    register_prompts(mcp)
    
    print("🚀 MCP User Data Server")
    print("📊 Version: 1.0.0")
    print("🔧 Environment: development")
    print("📁 Data directory: data")
    print("🌐 Server starting...")
    
    # Start MCP server (automatically handles stdio/http based on environment)
    mcp.run()

if __name__ == "__main__":
    main()