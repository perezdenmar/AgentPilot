#!/usr/bin/env python3
"""
CLI launcher for AgentPilot - provides command-line access without GUI
"""

import os
import sys
import sqlite3
import json
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def check_database():
    """Check if the database exists and create basic structure if needed"""
    db_path = Path("data.db")
    
    if not db_path.exists():
        print("📄 Creating basic database structure...")
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Create basic tables (simplified version)
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
                kind TEXT DEFAULT 'CHAT'
            )
        ''')
        
        # Insert default settings
        cursor.execute("INSERT OR IGNORE INTO settings (field, value) VALUES ('accepted_tos', '1')")
        cursor.execute("INSERT OR IGNORE INTO settings (field, value) VALUES ('my_uuid', 'codespace-user')")
        
        conn.commit()
        conn.close()
        print("✅ Database initialized")
    else:
        print("✅ Database found")

def simple_code_executor():
    """Simple code execution interface"""
    print("\n🔧 AgentPilot Code Executor")
    print("Enter code to execute, or 'quit' to exit")
    print("Supported: python, shell commands")
    print("-" * 40)
    
    while True:
        try:
            code_input = input("\n📝 Enter code (or 'quit'): ").strip()
            
            if code_input.lower() in ['quit', 'exit', 'q']:
                break
            
            if not code_input:
                continue
                
            # Detect language
            if code_input.startswith('python:') or code_input.startswith('py:'):
                code = code_input.split(':', 1)[1].strip()
                print(f"🐍 Executing Python: {code}")
                try:
                    exec(code)
                except Exception as e:
                    print(f"❌ Error: {e}")
            
            elif code_input.startswith('shell:') or code_input.startswith('sh:'):
                code = code_input.split(':', 1)[1].strip()
                print(f"🖥️  Executing Shell: {code}")
                try:
                    import subprocess
                    result = subprocess.run(code, shell=True, capture_output=True, text=True)
                    if result.stdout:
                        print(f"📤 Output: {result.stdout}")
                    if result.stderr:
                        print(f"⚠️  Error: {result.stderr}")
                except Exception as e:
                    print(f"❌ Error: {e}")
            
            else:
                # Default to Python
                print(f"🐍 Executing Python: {code_input}")
                try:
                    result = eval(code_input)
                    if result is not None:
                        print(f"📤 Result: {result}")
                except:
                    try:
                        exec(code_input)
                    except Exception as e:
                        print(f"❌ Error: {e}")
                        
        except KeyboardInterrupt:
            print("\n🛑 Interrupted by user")
            break
        except EOFError:
            print("\n🛑 EOF detected")
            break

def show_system_info():
    """Display system information"""
    print("\n📊 System Information")
    print("-" * 30)
    print(f"🐍 Python: {sys.version}")
    print(f"📁 Working Dir: {os.getcwd()}")
    print(f"🌐 Platform: {sys.platform}")
    
    # Check for Codespace
    if os.getenv('CODESPACES'):
        print("✅ Running in GitHub Codespace")
        print(f"📦 Codespace Name: {os.getenv('CODESPACE_NAME', 'Unknown')}")
    
    # Check database
    db_path = Path("data.db")
    if db_path.exists():
        print(f"💾 Database: {db_path.stat().st_size} bytes")
    else:
        print("💾 Database: Not found")

def interactive_menu():
    """Show interactive menu"""
    while True:
        print("\n🚁 AgentPilot - CLI Mode")
        print("=" * 40)
        print("1. 🔧 Code Executor")
        print("2. 📊 System Info")
        print("3. 📄 Database Check")
        print("4. 🌐 Launch Web Interface")
        print("5. ❌ Exit")
        
        try:
            choice = input("\nSelect option (1-5): ").strip()
            
            if choice == '1':
                simple_code_executor()
            elif choice == '2':
                show_system_info()
            elif choice == '3':
                check_database()
            elif choice == '4':
                print("🌐 Launching web interface...")
                os.system("python web_launcher.py")
            elif choice == '5':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice, please try again")
                
        except KeyboardInterrupt:
            print("\n🛑 Interrupted by user")
            break
        except EOFError:
            print("\n🛑 EOF detected")
            break

def main():
    """Main entry point"""
    print("🚁 AgentPilot - Command Line Interface")
    print("=" * 50)
    
    # Check environment
    if os.getenv('CODESPACES'):
        print("✅ GitHub Codespace detected")
    
    # Initialize database
    check_database()
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == '--info':
            show_system_info()
        elif sys.argv[1] == '--execute':
            simple_code_executor()
        elif sys.argv[1] == '--web':
            os.system("python web_launcher.py")
        else:
            print(f"❌ Unknown argument: {sys.argv[1]}")
            print("Available: --info, --execute, --web")
    else:
        # Interactive mode
        interactive_menu()

if __name__ == "__main__":
    main()