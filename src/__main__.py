import os
import sys

# Set environment variables
os.environ['LITELLM_LOG'] = 'ERROR'

def is_codespace_environment():
    """Check if we're running in a Codespace or headless environment"""
    codespace_indicators = [
        'CODESPACES',
        'GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN',
        'CODESPACE_NAME',
        'CI',  # Continuous Integration
        'DISPLAY' not in os.environ,  # No display available
    ]
    return any(os.getenv(indicator) if isinstance(indicator, str) else indicator for indicator in codespace_indicators)

def launch_codespace_mode():
    """Launch AgentPilot in Codespace-friendly mode"""
    print("🚁 AgentPilot - Codespace Mode")
    print("=" * 40)
    print("🌐 GUI mode not available in this environment")
    print("🔄 Switching to CLI/Web mode...")
    
    # Try to import and run the CLI launcher
    try:
        import subprocess
        subprocess.run([sys.executable, 'cli_launcher.py'], cwd=os.path.dirname(os.path.dirname(__file__)))
    except Exception as e:
        print(f"❌ Error launching CLI mode: {e}")
        print("💡 Try running: python cli_launcher.py")

if __name__ == '__main__':
    if is_codespace_environment():
        launch_codespace_mode()
    else:
        # Try to import GUI mode
        try:
            from src.gui.main import launch
            launch()
        except ImportError as e:
            print(f"❌ GUI dependencies not available: {e}")
            print("🔄 Falling back to Codespace mode...")
            launch_codespace_mode()
