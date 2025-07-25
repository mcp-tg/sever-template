# FastMCP Server Template

A comprehensive MCP (Model Context Protocol) server template built with FastMCP, featuring file-based user data management with advanced context support, progress reporting, and middleware capabilities.

## ✨ Features

- **Complete MCP Implementation**: Tools, Resources, Prompts, and Middleware
- **File-Based Storage**: JSON-based data storage (no database required)
- **Context Support**: Full FastMCP context capabilities including logging, progress reporting, and LLM sampling
- **Progress Reporting**: Real-time progress updates for long-running operations
- **Middleware Pipeline**: Validation, logging, and security middleware
- **Agent-Friendly**: Comprehensive docstrings and clear API structure
- **Inspector Ready**: Full support for MCP Inspector testing

## 📦 What's Included

### Tools (5 total)
- `write_user` - Add individual users with validation
- `get_user_count` - Quick user count utility
- `analyze_users` - Comprehensive data analysis with AI insights
- `bulk_add_users` - Batch user import with progress tracking
- `process_users_simulation` - Demo tool for testing workflows

### Resources (4 total)
- `data://users` - Access all user data
- `data://users/{user_name}` - Find specific users by name
- `data://users/stats` - Quick statistical overview
- `data://users/report` - Comprehensive data report

### Prompts (3 total)
- `user_management_assistant` - Setup prompt for user data management
- `data_analysis_prompt` - Customizable analysis guidance
- `interactive_user_prompt` - Interactive user onboarding

## 🚀 Quick Start

### Option 1: Test with MCP Inspector

Perfect for exploring the server capabilities through a web interface:

```bash
# Clone the repository
git clone <your-repo-url>
cd server-template

# Make scripts executable
chmod +x dev-inspector.sh dev-start.sh

# Launch MCP Inspector
./dev-inspector.sh
```

This will:
- Install dependencies automatically
- Launch the MCP Inspector web interface
- Allow you to test all tools, resources, and prompts interactively

### Option 2: Run Locally for Development

For local development and testing:

```bash
# Install dependencies
uv sync

# Start the server
./dev-start.sh

# Or run directly
uv run python my_mcp_server/main.py
```

### Option 3: Use with an Agent

Connect this server to Claude Desktop or other MCP-compatible clients:

1. **Add to Claude Desktop configuration** (`claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "user-data-server": {
      "command": "uv",
      "args": ["run", "python", "/path/to/server-template/my_mcp_server/main.py"]
    }
  }
}
```

2. **Restart Claude Desktop** and the server will be available

## 🔧 Building Your Own Server

### Method 1: Fork and Customize

1. **Fork this repository** to your GitHub account
2. **Clone your fork**:
   ```bash
   git clone https://github.com/yourusername/your-server-name.git
   cd your-server-name
   ```

3. **Customize the server**:
   - Update `pyproject.toml` with your server name and details
   - Modify tools in `my_mcp_server/tools/`
   - Update resources in `my_mcp_server/resources/`
   - Customize prompts in `my_mcp_server/prompts/`

4. **Test your changes**:
   ```bash
   ./dev-inspector.sh
   ```

### Method 2: Use as Reference with Your Agent

1. **Clone this repository** to your local machine
2. **Reference in your agent prompts**:

```
I want to build an MCP server using FastMCP. I have a reference template at /path/to/server-template that shows best practices. Please help me:

1. Analyze the structure of the reference template
2. Understand the patterns used for tools, resources, and prompts
3. Create a new server based on these patterns for [your use case]

The reference template includes:
- Complete FastMCP implementation examples
- Context usage patterns
- Progress reporting
- Middleware implementation
- Agent-friendly documentation

Please examine the AGENT_README.md file first to understand the codebase structure.
```

3. **Your agent will**:
   - Read the codebase structure from `AGENT_README.md`
   - Understand the patterns and best practices
   - Help you build a customized server for your needs

## 📁 Project Structure

```
server-template/
├── my_mcp_server/           # Main server package
│   ├── main.py             # Server entry point
│   ├── tools/              # Tool definitions
│   ├── resources/          # Resource definitions
│   ├── prompts/            # Prompt templates
│   └── middleware/         # Middleware components
├── data/                   # Data storage directory
├── dev-inspector.sh        # Inspector testing script
├── dev-start.sh           # Local development script
└── README.md              # This file
```

## 🧪 Testing Your Server

### Using MCP Inspector
The easiest way to test all functionality:

```bash
./dev-inspector.sh
```

- **Tools Tab**: Test all server tools with parameter inputs
- **Resources Tab**: Browse available data resources
- **Prompts Tab**: Test prompt templates
- **Progress**: View real-time progress reporting

### Manual Testing Workflow

1. **Add some users**:
   ```
   Tool: write_user
   Parameters: {"name": "John Doe", "email": "john@example.com"}
   ```

2. **Check user count**:
   ```
   Tool: get_user_count
   ```

3. **View all users**:
   ```
   Resource: data://users
   ```

4. **Find specific user**:
   ```
   Resource: data://users/John%20Doe
   ```

5. **Run analysis**:
   ```
   Tool: analyze_users
   ```

## 📚 Learn More

- **FastMCP Documentation**: [FastMCP Docs](https://gofastmcp.com/getting-started/welcome)
- **MCP Protocol**: [Model Context Protocol](https://modelcontextprotocol.io)
- **Agent README**: See `AGENT_README.md` for detailed codebase structure

## 🤝 Contributing

This template is designed to be educational and reusable. Feel free to:
- Fork and customize for your needs
- Submit improvements via pull requests
- Share your own server implementations
- Report issues or suggestions

## 📄 License

MIT License - feel free to use this template for any purpose.