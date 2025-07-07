# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an MCP (Model Context Protocol) server template using FastMCP. The project follows a modular architecture with separate modules for tools, resources, prompts, and middleware.

## Architecture

### Core Components

- **main.py**: Entry point that creates parent and child servers, registers middleware, and mounts components
- **tools/**: Tool definitions that provide executable functions to clients
- **resources/**: Resource definitions that provide data access to clients  
- **prompts/**: Prompt templates for AI interactions
- **middleware/**: Custom middleware for validation, logging, and request processing

### Server Architecture

The template uses a parent-child server pattern:
- Parent server handles global middleware
- Child server contains tools and resources
- Child is mounted on parent with "child" prefix

## Development Commands

### Package Management (uv)
```bash
# Install dependencies
uv sync

# Add new dependency
uv add package-name

# Add development dependency  
uv add --dev package-name

# Run Python with project dependencies
uv run python main.py
```

### Code Quality
```bash
# Format code
uv run black .

# Sort imports
uv run isort .

# Type checking
uv run mypy .

# Run all formatting and checks
uv run black . && uv run isort . && uv run mypy .
```

### Testing
```bash
# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=.

# Run specific test file
uv run pytest tests/test_tools.py
```

### Running the Server
```bash
# Start the MCP server
uv run python my_mcp_server/main.py

# Start with specific host/port (modify main.py)
uv run python my_mcp_server/main.py
```

## Key Patterns

### Adding New Tools
1. Create tool function in `tools/user_tools.py`
2. Use `@mcp.tool` decorator
3. Include proper error handling with `ToolError`
4. Register tool in `register_tools()` function

### Adding New Resources  
1. Create resource function in `resources/user_resources.py`
2. Use `@mcp.resource` decorator
3. Return structured data
4. Register resource in `register_resources()` function

### Adding Middleware
1. Create middleware class in `middleware/custom_middleware.py`
2. Inherit from `Middleware` base class
3. Implement lifecycle methods (e.g., `on_call_tool`)
4. Register middleware in `register_middleware()` function

### Database Operations
- Direct SQLite operations in tools/resources where needed
- All database errors are wrapped in `ToolError`
- Uses SQLite by default with "users.db" file

## File Structure Conventions

- All modules have `__init__.py` files to make them proper Python packages
- Registration functions follow the pattern `register_<component>(mcp: FastMCP)`
- Error handling uses `fastmcp.exceptions.ToolError`
- Keep database operations simple and direct in the relevant modules