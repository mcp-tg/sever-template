#!/bin/bash

# MCP Inspector Development Script

echo "🔍 Starting MCP Server with Inspector"

# Create data directory if it doesn't exist
mkdir -p data

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from .env.example"
    cp .env.example .env
fi

# Check if virtual environment exists
if [ ! -d .venv ]; then
    echo "🔧 Creating virtual environment..."
    uv venv
fi

# Install dependencies
echo "📦 Installing dependencies..."
uv sync

# Check if Node.js and npm are available
if ! command -v npm &> /dev/null; then
    echo "❌ npm is required for MCP Inspector"
    echo "💡 Please install Node.js from https://nodejs.org/"
    exit 1
fi

echo "🚀 Starting MCP Inspector..."
echo "💡 This will open a web interface to test your MCP server"
echo "💡 If you see a port conflict, use: ./dev-port-check.sh 6277"

# Run the MCP Inspector with uv run pointing to our main script
npx @modelcontextprotocol/inspector uv run main.py