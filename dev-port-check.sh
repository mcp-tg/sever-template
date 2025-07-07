#!/bin/bash

# Port Check and Kill Script for MCP Development

PORT=${1:-6277}

echo "🔍 Checking port $PORT..."

# Check if port is in use
PID=$(lsof -ti:$PORT)

if [ -z "$PID" ]; then
    echo "✅ Port $PORT is available"
else
    echo "⚠️  Port $PORT is in use by process $PID"
    
    # Show process details
    echo "📋 Process details:"
    ps -p $PID -o pid,ppid,cmd
    
    # Ask if user wants to kill the process
    read -p "❓ Kill process $PID? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        kill $PID
        echo "💀 Killed process $PID"
        
        # Wait a moment and check again
        sleep 1
        NEW_PID=$(lsof -ti:$PORT)
        if [ -z "$NEW_PID" ]; then
            echo "✅ Port $PORT is now available"
        else
            echo "⚠️  Port $PORT is still in use. You may need to force kill:"
            echo "   kill -9 $NEW_PID"
        fi
    else
        echo "🚫 Process not killed. Try using a different port:"
        echo "   MCP_INSPECTOR_PORT=6279 ./dev-inspector.sh"
    fi
fi