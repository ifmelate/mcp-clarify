#!/bin/bash
# Setup script for MCP HITL Server

set -e

echo "🚀 Setting up MCP HITL Server..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python found: $(python3 --version)"

# Check if uv is installed
if command -v uv &> /dev/null; then
    echo "✓ uv found: $(uv --version)"
    echo "📦 Creating virtual environment with uv..."
    uv venv
    echo "📥 Installing dependencies with uv..."
    uv pip install -r requirements.txt
else
    echo "⚠️  uv not found, using pip instead"
    echo "📦 Creating virtual environment with venv..."
    python3 -m venv .venv
    echo "📥 Installing dependencies with pip..."
    source .venv/bin/activate
    pip install -r requirements.txt
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To activate the virtual environment, run:"
echo "  source .venv/bin/activate"
echo ""
echo "To run the server, use:"
echo "  python hitl_server.py"
echo ""
echo "Don't forget to configure your MCP client to use this server!"

