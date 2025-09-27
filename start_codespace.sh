#!/bin/bash
# AgentPilot Codespace Startup Script

echo "🚁 AgentPilot - Codespace Startup"
echo "=================================="

# Check if we're in a codespace
if [ -n "$CODESPACES" ]; then
    echo "✅ GitHub Codespace detected"
else
    echo "⚠️  Not in Codespace, but continuing..."
fi

# Check Python version
echo "🐍 Python version: $(python --version)"

# Run setup if data.db doesn't exist
if [ ! -f "data.db" ]; then
    echo "📦 Running initial setup..."
    python setup_codespace.py
else
    echo "✅ Database found, skipping setup"
fi

# Check command line arguments
case "$1" in
    "web")
        echo "🌐 Starting web interface..."
        python web_launcher.py
        ;;
    "cli")
        echo "🖥️  Starting CLI interface..."
        python cli_launcher.py
        ;;
    "info")
        echo "📊 Showing system info..."
        python cli_launcher.py --info
        ;;
    "setup")
        echo "⚙️  Running setup..."
        python setup_codespace.py
        ;;
    *)
        echo ""
        echo "🚀 Usage: $0 [option]"
        echo ""
        echo "Options:"
        echo "  web    - Start web interface (http://localhost:8000)"
        echo "  cli    - Start CLI interface"
        echo "  info   - Show system information"
        echo "  setup  - Run setup process"
        echo ""
        echo "No option = Auto-detect mode"
        echo ""
        
        if [ -z "$1" ]; then
            echo "🔄 Starting auto-detect mode..."
            python -m src
        fi
        ;;
esac