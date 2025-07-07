# FastMCP Server Template - Agent Reference

This document provides a comprehensive guide for AI agents to understand the structure, patterns, and implementation details of this FastMCP server template.

## 🏗️ Codebase Architecture

### Directory Structure
```
server-template/
├── __init__.py              # Main package exports and metadata
├── main.py                  # Server entry point and configuration
├── src/                     # Source modules directory
│   ├── __init__.py         # Source package initialization
│   ├── tools/
│   │   ├── __init__.py     # Tool exports and available tools list
│   │   └── user_tools.py   # Tool implementations
│   ├── resources/
│   │   ├── __init__.py     # Resource exports and available resources list
│   │   └── user_resources.py # Resource implementations
│   ├── prompts/
│   │   ├── __init__.py     # Prompt exports and available prompts list
│   │   └── user_prompts.py # Prompt implementations
│   └── middleware/
│       ├── __init__.py     # Middleware exports and available middleware list
│       └── custom_middleware.py # Middleware implementations
├── data/                    # Data storage directory
├── pyproject.toml          # Project configuration
└── dev-*.sh               # Development scripts
```

## 🔧 Core Implementation Patterns

### 1. Main Server Setup (`main.py`)

**Key Pattern**: Simple, environment-adaptive server initialization
```python
def main():
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    # Create MCP server
    mcp = FastMCP("UserDataServer")
    
    # Register components in order
    register_middleware(mcp)
    register_tools(mcp)
    register_resources(mcp)
    register_prompts(mcp)
    
    # Auto-detecting server mode (stdio for inspector, http for local)
    mcp.run()
```

**Important Notes**:
- Uses `mcp.run()` without parameters for automatic environment detection
- Creates data directory automatically
- Simple, clean startup without complex configuration

### 2. Tool Implementation Pattern (`tools/user_tools.py`)

**Standard Tool Structure**:
```python
@mcp.tool(
    name="tool_name",
    description="Brief description for discovery",
    tags={"category", "type"}
)
async def tool_function(param1: Type, param2: Type, ctx: Context) -> ReturnType:
    """Comprehensive docstring for agents.
    
    Detailed explanation of what the tool does, when to use it,
    parameters, return values, and usage examples.
    
    Args:
        param1: Description of parameter
        param2: Description of parameter
        
    Returns:
        Description of return value structure
        
    Example usage:
        - When to use this tool
        - How it fits into workflows
    """
    # Implementation with context usage
    await ctx.info("Starting operation")
    await ctx.report_progress(progress=0, total=100)
    
    try:
        # Main logic here
        result = do_work()
        await ctx.info("Operation completed")
        return result
    except Exception as e:
        await ctx.error(f"Operation failed: {str(e)}")
        raise ToolError(f"Error: {str(e)}")
```

**Available Tools**:
1. `write_user` - Individual user creation with validation
2. `get_user_count` - Quick count utility 
3. `analyze_users` - Hybrid statistical + AI analysis
4. `bulk_add_users` - Batch operations with progress tracking
5. `process_users_simulation` - Demo tool for testing

### 3. Resource Implementation Pattern (`resources/user_resources.py`)

**Static Resource**:
```python
@mcp.resource(
    uri="scheme://path",
    name="ResourceName", 
    description="Description for discovery",
    mime_type="application/json"
)
async def resource_function(ctx: Context) -> dict:
    """Detailed docstring explaining resource purpose and usage."""
    await ctx.debug("Accessing resource")
    # Logic to generate/fetch data
    return {"data": "resource_content"}
```

**Resource Template (Parameterized)**:
```python
@mcp.resource("scheme://path/{parameter}")
async def template_function(parameter: str, ctx: Context) -> dict:
    """Handles parameterized resource access."""
    # URL decode parameter
    import urllib.parse
    decoded_param = urllib.parse.unquote(parameter)
    
    # Logic using parameter
    return {"result": f"data_for_{decoded_param}"}
```

**Available Resources**:
1. `data://users` - All user data
2. `data://users/{user_name}` - Find by name (URL-encoded)
3. `data://users/stats` - Statistical overview
4. `data://users/report` - Comprehensive report

### 4. Prompt Implementation Pattern (`prompts/user_prompts.py`)

**Basic Prompt**:
```python
@mcp.prompt(
    name="prompt_name",
    description="Prompt purpose"
)
async def prompt_function(ctx: Context) -> str:
    """Docstring explaining prompt usage."""
    # Optional: Get current data for context
    current_data = await ctx.read_resource("data://users")
    
    return f"""
    Prompt template with dynamic content: {current_data}
    """
```

**Parameterized Prompt**:
```python
@mcp.prompt()
async def param_prompt(param: str = "default", ctx: Context = None) -> str:
    """Prompt with parameters."""
    return f"Customized prompt for {param}"
```

**Interactive Prompt with Elicitation**:
```python
@mcp.prompt()
async def interactive_prompt(ctx: Context) -> str:
    """Uses ctx.elicit for user interaction."""
    user_input = await ctx.elicit("Question?", response_type=str)
    return f"Personalized prompt for {user_input}"
```

## 📊 Data Storage Pattern

### File Structure
```json
// data/users.json
{
  "users": [
    {
      "name": "John Doe",
      "email": "john@example.com"
    },
    {
      "name": "Jane Smith", 
      "email": "jane@example.com"
    }
  ]
}
```

### Data Access Pattern
```python
def read_users():
    users_file = "data/users.json"
    if os.path.exists(users_file):
        with open(users_file, 'r') as f:
            data = json.load(f)
        return data.get("users", [])
    return []

def write_users(users):
    users_file = "data/users.json"
    with open(users_file, 'w') as f:
        json.dump({"users": users}, f, indent=2)
```

## 🔄 Context Usage Patterns

### Progress Reporting
```python
# For operations with known steps
await ctx.report_progress(progress=current_step, total=total_steps)

# For percentage-based progress  
await ctx.report_progress(progress=50, total=100)
```

### Logging Levels
```python
await ctx.debug("Detailed debugging information")
await ctx.info("General information for users")
await ctx.warning("Warning about potential issues")
await ctx.error("Error conditions")
```

### Resource Reading
```python
# Read from another resource
data = await ctx.read_resource("data://users")
```

### LLM Sampling (Agent-Only)
```python
try:
    response = await ctx.sample("Analysis prompt", temperature=0.3)
    # Use AI response
except Exception as e:
    # Fallback for non-AI environments
    response = "AI not available"
```

### Client Elicitation (Interactive Clients)
```python
try:
    user_input = await ctx.elicit("Question?", response_type=str)
    # Use input
except Exception as e:
    # Fallback for non-interactive environments
    user_input = "default"
```

## 🛡️ Middleware Pattern

### Middleware Structure
```python
class CustomMiddleware(Middleware):
    """Middleware description."""
    
    async def on_call_tool(self, context: MiddlewareContext, call_next):
        # Pre-processing
        start_time = time.time()
        
        try:
            # Call next middleware/tool
            result = await call_next(context)
            # Post-processing on success
            return result
        except Exception as e:
            # Error handling
            raise

# Registration
mcp.add_middleware(CustomMiddleware())
```

## 🧪 Testing Patterns

### Unit Testing Structure
```python
import pytest
from my_mcp_server.tools.user_tools import register_tools

@pytest.mark.asyncio
async def test_tool():
    mcp = FastMCP("TestServer")
    register_tools(mcp)
    
    # Test tool functionality
    result = await mcp.call_tool("write_user", {"name": "Test", "email": "test@example.com"})
    assert result["status"] == "success"
```

### Development Scripts
- `dev-start.sh` - Local development server
- `dev-inspector.sh` - MCP Inspector testing
- `dev-port-check.sh` - Port conflict resolution

## 📦 Package Structure Best Practices

### `__init__.py` Files
Each package includes:
- Module docstrings explaining purpose
- Import statements for main functions
- `__all__` lists for clean API exports
- Reference lists (AVAILABLE_TOOLS, AVAILABLE_RESOURCES, etc.)

### Error Handling
- Use `ToolError` for tool failures
- Provide descriptive error messages
- Log errors with context
- Include fallback behavior where appropriate

### Documentation Standards
- Comprehensive docstrings for all public functions
- Include Args, Returns, and Example usage sections
- Explain when and how to use each component
- Document parameter formats and constraints

## 🔄 Extension Patterns

### Adding New Tools
1. Create function in `tools/user_tools.py`
2. Use `@mcp.tool()` decorator with metadata
3. Add comprehensive docstring
4. Update `tools/__init__.py` AVAILABLE_TOOLS list
5. Test with inspector

### Adding New Resources
1. Create function in `resources/user_resources.py`
2. Use `@mcp.resource()` decorator with URI
3. Handle both static and parameterized resources
4. Update `resources/__init__.py` lists
5. Test resource access

### Adding New Middleware
1. Create class inheriting from `Middleware`
2. Implement lifecycle methods (`on_call_tool`, etc.)
3. Register with `mcp.add_middleware()`
4. Test middleware functionality

This template demonstrates production-ready patterns for building FastMCP servers with comprehensive functionality, proper error handling, and agent-friendly documentation.