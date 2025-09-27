# AgentPilot - Codespace Edition

🚁 **AgentPilot** adapted to run in GitHub Codespace without GUI dependencies.

## Quick Start

### 1. Setup Environment

Run the setup script to prepare the environment:

```bash
python setup_codespace.py
```

This will:
- Check Python compatibility  
- Install essential packages (uvicorn, aiofiles, etc.)
- Create a minimal database
- Set up environment variables

### 2. Launch Options

#### Option A: CLI Mode (Recommended)
```bash
python cli_launcher.py
```

Interactive menu with:
- 🔧 Code Executor - Execute Python/shell commands
- 📊 System Info - View system information  
- 📄 Database Check - Verify database setup
- 🌐 Launch Web Interface - Start web server
- ❌ Exit

#### Option B: Web Interface
```bash
python web_launcher.py
```

Starts a web server at `http://localhost:8000` with a simple HTML interface.

#### Option C: Auto-detect Mode
```bash
python -m src
```

Automatically detects the environment and chooses CLI/web mode instead of GUI.

### 3. Command Line Options

```bash
# Quick system info
python cli_launcher.py --info

# Direct code executor
python cli_launcher.py --execute

# Launch web interface
python cli_launcher.py --web
```

## Features Available in Codespace

✅ **Working Features:**
- Command-line interface
- Simple web interface
- Code execution (Python, Shell)
- Basic database operations
- Environment detection
- Minimal dependency installation

⚠️ **Limited Features:**
- No GUI interface (PySide6 not available)
- Limited AI model integrations (due to dependency constraints)
- Some OpenInterpreter features may be restricted

❌ **Not Available:**
- Full desktop GUI
- Advanced AI workflows requiring specific Python versions
- Features requiring GPU or specialized hardware

## Architecture

```
AgentPilot Codespace Structure:
├── setup_codespace.py     # Environment setup
├── cli_launcher.py        # CLI interface
├── web_launcher.py        # Web interface  
├── src/
│   ├── __main__.py        # Modified entry point
│   └── ...                # Original source code
├── data.db               # SQLite database
└── requirements-codespace.txt # Minimal requirements
```

## Environment Detection

The application automatically detects Codespace environment by checking for:
- `CODESPACES` environment variable
- `GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN`
- `CODESPACE_NAME`
- Absence of `DISPLAY` variable

## Troubleshooting

### Network Issues
If package installation fails due to network timeouts:
```bash
# Try with longer timeout
pip install --timeout 300 package_name

# Or skip package installation and use built-in features
python cli_launcher.py --info
```

### Import Errors
If you see missing module errors:
```bash
# Check what's available
python -c "import sys; print(sys.path)"

# Use the CLI mode which has fewer dependencies
python cli_launcher.py
```

### Database Issues
If database operations fail:
```bash
# Reinitialize database
rm data.db
python setup_codespace.py
```

## Development

### Adding New Features

1. Keep dependencies minimal
2. Use environment detection
3. Provide graceful fallbacks
4. Test in both local and Codespace environments

### Testing

```bash
# Test all components
python setup_codespace.py     # Setup
python cli_launcher.py --info # CLI  
python web_launcher.py        # Web (Ctrl+C to stop)
python -m src                 # Entry point
```

## Limitations

- **Python Version**: Designed for Python 3.8+ but works best with 3.10+
- **Dependencies**: Limited to packages available via pip with network constraints
- **Performance**: May be slower than desktop version due to environment limitations
- **Features**: Some advanced AI/GUI features are not available

## Contributing

When contributing Codespace-compatible features:

1. Test in actual Codespace environment
2. Handle missing dependencies gracefully
3. Provide clear error messages
4. Update this README with new features

## Support

For Codespace-specific issues:
1. Check the troubleshooting section above
2. Verify environment with `python cli_launcher.py --info`
3. Try the minimal CLI mode first
4. Report issues with environment details

---

**Note**: This is a simplified version of AgentPilot for development and testing in Codespace. For full functionality, use the desktop application.