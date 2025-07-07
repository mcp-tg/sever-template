#!/bin/bash

# Local Development Startup Script

echo "🚀 Starting MCP Server Template in Development Mode"

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

# Start the server
echo "🎯 Starting server..."
uv run main.py