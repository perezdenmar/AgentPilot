#!/usr/bin/env python3
"""
Web launcher for AgentPilot - runs the app in web mode for Codespace
This bypasses the GUI and provides a simple web interface
"""

import os
import sys
import asyncio
import json
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def create_simple_web_interface():
    """Create a simple HTML interface for AgentPilot"""
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AgentPilot - Codespace</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #1e1e1e;
            color: #ffffff;
        }
        .container {
            background-color: #2d2d2d;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        h1 {
            text-align: center;
            color: #00d4ff;
            margin-bottom: 30px;
        }
        .status {
            background-color: #404040;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .feature-list {
            list-style-type: none;
            padding: 0;
        }
        .feature-list li {
            background-color: #404040;
            margin: 10px 0;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #00d4ff;
        }
        .instructions {
            background-color: #1a472a;
            border: 1px solid #28a745;
            border-radius: 5px;
            padding: 20px;
            margin-top: 20px;
        }
        .instructions h3 {
            color: #28a745;
            margin-top: 0;
        }
        code {
            background-color: #404040;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }
        .warning {
            background-color: #4a3728;
            border: 1px solid #fd7e14;
            border-radius: 5px;
            padding: 15px;
            margin: 20px 0;
            color: #fd7e14;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚁 AgentPilot - Codespace Edition</h1>
        
        <div class="status">
            <h2>Status: Ready for Codespace</h2>
            <p>AgentPilot has been adapted to run in GitHub Codespace environment without GUI dependencies.</p>
        </div>

        <h2>🎯 Available Features</h2>
        <ul class="feature-list">
            <li><strong>Web Interface:</strong> This simple web interface for basic interaction</li>
            <li><strong>CLI Mode:</strong> Command-line interface through OpenInterpreter</li>
            <li><strong>API Mode:</strong> FastAPI server for programmatic access</li>
            <li><strong>Code Execution:</strong> Execute code in multiple languages (Python, Shell, JavaScript, etc.)</li>
            <li><strong>No GUI Dependencies:</strong> Bypasses PySide6 and other GUI requirements</li>
        </ul>

        <div class="instructions">
            <h3>🚀 How to Use in Codespace</h3>
            <p><strong>1. Install minimal dependencies:</strong></p>
            <code>pip install fastapi uvicorn requests</code>
            
            <p><strong>2. Run the web launcher:</strong></p>
            <code>python web_launcher.py</code>
            
            <p><strong>3. Access the application:</strong></p>
            <p>The application will be available at the Codespace's forwarded port</p>
            
            <p><strong>4. Alternative: Use CLI mode:</strong></p>
            <code>python -c "from src.plugins.openinterpreter.src.terminal_interface.terminal_interface import terminal_interface; terminal_interface(None, 'Hello')"</code>
        </div>

        <div class="warning">
            <strong>⚠️ Note:</strong> This is a simplified version of AgentPilot adapted for Codespace. 
            Some advanced features requiring GUI or specific Python versions may not be available.
            For full functionality, use the desktop application.
        </div>

        <h2>📊 System Information</h2>
        <div class="status">
            <p><strong>Environment:</strong> GitHub Codespace</p>
            <p><strong>Python Version:</strong> """ + str(sys.version) + """</p>
            <p><strong>Working Directory:</strong> """ + str(os.getcwd()) + """</p>
        </div>
    </div>
</body>
</html>"""
    
    return html_content

def launch_simple_server():
    """Launch a simple HTTP server for the web interface"""
    try:
        import http.server
        import socketserver
        import webbrowser
        from threading import Thread
        
        # Create the HTML file
        html_file = Path("agentpilot_web.html")
        html_file.write_text(create_simple_web_interface())
        
        PORT = 8000
        
        class Handler(http.server.SimpleHTTPRequestHandler):
            def do_GET(self):
                if self.path == '/' or self.path == '':
                    self.path = '/agentpilot_web.html'
                return super().do_GET()
        
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"🚁 AgentPilot Web Interface starting...")
            print(f"📡 Server running at http://localhost:{PORT}")
            print(f"🌐 In Codespace, use the forwarded port to access the interface")
            print(f"🛑 Press Ctrl+C to stop the server")
            
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print(f"\n🛑 Server stopped.")
                
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        print("Falling back to CLI mode...")
        return False
    
    return True

def check_codespace_environment():
    """Check if we're running in a Codespace environment"""
    codespace_indicators = [
        'CODESPACES',
        'GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN',
        'CODESPACE_NAME'
    ]
    
    return any(os.getenv(indicator) for indicator in codespace_indicators)

def main():
    """Main entry point for the web launcher"""
    print("🚁 AgentPilot - Codespace Launcher")
    print("=" * 50)
    
    if check_codespace_environment():
        print("✅ Codespace environment detected")
    else:
        print("⚠️  Codespace environment not detected, but continuing...")
    
    print(f"🐍 Python version: {sys.version}")
    print(f"📁 Working directory: {os.getcwd()}")
    
    # Try to launch the web server
    if not launch_simple_server():
        print("\n📋 Alternative: Manual CLI usage")
        print("You can interact with AgentPilot components manually:")
        print("1. Import the required modules")
        print("2. Use the OpenInterpreter CLI components")
        print("3. Access the core functionality through Python API")

if __name__ == "__main__":
    main()