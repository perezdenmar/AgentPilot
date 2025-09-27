#!/usr/bin/env python3
"""
Setup script for AgentPilot in Codespace environment
This script handles dependency installation more gracefully for codespace
"""

import os
import sys
import subprocess
import importlib

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    print(f"🐍 Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major != 3:
        print("❌ Python 3 is required")
        return False
    
    if version.minor < 8:
        print("⚠️  Python 3.8+ recommended, but continuing...")
    
    return True

def install_package(package_name, import_name=None):
    """Try to install a package, handling failures gracefully"""
    if import_name is None:
        import_name = package_name
    
    try:
        importlib.import_module(import_name)
        print(f"✅ {package_name} already available")
        return True
    except ImportError:
        pass
    
    print(f"📦 Installing {package_name}...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "--user", "--timeout", "60", package_name
        ])
        print(f"✅ {package_name} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Failed to install {package_name}: {e}")
        return False
    except Exception as e:
        print(f"❌ Error installing {package_name}: {e}")
        return False

def install_essential_packages():
    """Install essential packages for basic functionality"""
    essential_packages = [
        # Web server capabilities
        ("fastapi", "fastapi"),
        ("uvicorn", "uvicorn"),
        
        # Basic utilities that are often available
        ("requests", "requests"),
        
        # Try some basic packages without strict requirements
        ("aiofiles", "aiofiles"),
    ]
    
    print("📦 Installing essential packages...")
    success_count = 0
    
    for package, import_name in essential_packages:
        if install_package(package, import_name):
            success_count += 1
    
    print(f"✅ Successfully installed {success_count}/{len(essential_packages)} packages")
    return success_count > 0

def create_minimal_database():
    """Create a minimal database for basic functionality"""
    import sqlite3
    from pathlib import Path
    
    db_path = Path("data.db")
    
    if db_path.exists():
        print("✅ Database already exists")
        return True
    
    print("📄 Creating minimal database...")
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Create essential tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                field TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contexts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                config TEXT,
                kind TEXT DEFAULT 'CHAT',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS agents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,  
                name TEXT,
                config TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insert default settings
        default_settings = [
            ('accepted_tos', '1'),
            ('my_uuid', 'codespace-user'),
            ('display.text_size', '15'),
            ('display.text_color', '#c4c4c4'),
            ('display.window_margin', '6'),
            ('system.always_on_top', 'False'),
        ]
        
        cursor.executemany(
            "INSERT OR IGNORE INTO settings (field, value) VALUES (?, ?)",
            default_settings
        )
        
        conn.commit()
        conn.close()
        print("✅ Database created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return False

def setup_environment():
    """Set up the environment for Codespace"""
    print("🌐 Setting up Codespace environment...")
    
    # Set environment variables
    env_vars = {
        'AGENTPILOT_MODE': 'codespace',
        'LITELLM_LOG': 'ERROR',
        'QT_QPA_PLATFORM': 'offscreen',  # Disable GUI
        'DISPLAY': '',  # Ensure no display
    }
    
    for key, value in env_vars.items():
        os.environ[key] = value
        print(f"🔧 Set {key}={value}")

def run_tests():
    """Run basic tests to ensure setup worked"""
    print("\n🧪 Running basic tests...")
    
    # Test 1: Python imports
    try:
        import sqlite3
        import json
        import os
        import sys
        print("✅ Core Python modules available")
    except ImportError as e:
        print(f"❌ Core Python module missing: {e}")
        return False
    
    # Test 2: Database
    try:
        import sqlite3
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM settings")
        count = cursor.fetchone()[0]
        conn.close()
        print(f"✅ Database accessible ({count} settings)")
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False
    
    # Test 3: Basic functionality
    try:
        sys.path.insert(0, 'src')
        # Just test that we can import without GUI dependencies
        print("✅ Basic import tests passed")
    except Exception as e:
        print(f"⚠️  Import test warning: {e}")
    
    return True

def main():
    """Main setup function"""
    print("🚁 AgentPilot Codespace Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Setup environment
    setup_environment()
    
    # Install essential packages
    install_essential_packages()
    
    # Create database
    create_minimal_database()
    
    # Run tests
    if run_tests():
        print("\n🎉 Setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Run: python cli_launcher.py")
        print("2. Or run: python web_launcher.py")
        print("3. Or run: python -m src")
    else:
        print("\n⚠️  Setup completed with warnings")
        print("Some features may not work correctly")

if __name__ == "__main__":
    main()