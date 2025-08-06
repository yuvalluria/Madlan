
#!/usr/bin/env python3
"""
Automated setup script for Madlan MCP Server
Run this script to automatically configure everything
"""

import os
import sys
import json
import platform
from pathlib import Path

def get_claude_config_path():
    """Get the Claude Desktop config file path for current OS"""
    system = platform.system()
    if system == "Darwin":  # macOS
        return Path.home() / "Library/Application Support/Claude/claude_desktop_config.json"
    elif system == "Windows":
        return Path(os.environ["APPDATA"]) / "Claude/claude_desktop_config.json"
    else:  # Linux
        return Path.home() / ".config/claude/claude_desktop_config.json"

def create_requirements_txt():
    """Create requirements.txt file"""
    requirements = """mcp>=1.0.0
pandas>=1.3.0
openpyxl>=3.0.0
requests>=2.25.0
geopy>=2.2.0"""
    
    with open("requirements.txt", "w") as f:
        f.write(requirements)
    print("✅ Created requirements.txt")

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing dependencies...")
    os.system(f"{sys.executable} -m pip install -r requirements.txt")
    print("✅ Dependencies installed")

def setup_claude_config():
    """Setup Claude Desktop configuration"""
    config_path = get_claude_config_path()
    current_dir = Path.cwd().absolute()
    
    # MCP server configuration
    mcp_config = {
        "mcpServers": {
            "madlan-property-finder": {
                "command": sys.executable,
                "args": [str(current_dir / "mcp_server.py")],
                "env": {
                    "PYTHONPATH": str(current_dir)
                }
            }
        }
    }
    
    # Create config directory if it doesn't exist
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Load existing config or create new one
    if config_path.exists():
        with open(config_path, 'r') as f:
            existing_config = json.load(f)
        
        # Merge MCP servers
        if "mcpServers" in existing_config:
            existing_config["mcpServers"].update(mcp_config["mcpServers"])
        else:
            existing_config["mcpServers"] = mcp_config["mcpServers"]
        
        final_config = existing_config
    else:
        final_config = mcp_config
    
    # Write config
    with open(config_path, 'w') as f:
        json.dump(final_config, f, indent=2)
    
    print(f"✅ Claude Desktop config updated: {config_path}")

def check_files():
    """Check if required files exist"""
    required_files = [
        "utils/file_loader.py",
        "services/geocoding_service.py", 
        "services/distance_calculator.py",
        "models/property.py",
        "100 listings haifa.xlsx"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ All required files found")
    return True

def create_mcp_server():
    """Create the MCP server file"""
    # The MCP server code would be inserted here
    # For now, just check if it exists
    if Path("mcp_server.py").exists():
        print("✅ mcp_server.py already exists")
        return True
    else:
        print("❌ Please save the MCP server code as 'mcp_server.py' first")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up Madlan MCP Server...")
    print(f"📍 Working directory: {Path.cwd()}")
    print(f"🐍 Python executable: {sys.executable}")
    print()
    
    # Check if we're in the right directory
    if not Path("Madlan.py").exists():
        print("❌ Error: Madlan.py not found!")
        print("   Please run this script from your project directory")
        return
    
    # Step 1: Check files
    if not check_files():
        print("\n❌ Setup cannot continue with missing files")
        return
    
    # Step 2: Check MCP server
    if not create_mcp_server():
        print("\n❌ Setup cannot continue without mcp_server.py")
        return
    
    # Step 3: Create requirements
    create_requirements_txt()
    
    # Step 4: Install dependencies
    try:
        install_dependencies()
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return
    
    # Step 5: Setup Claude config
    try:
        setup_claude_config()
    except Exception as e:
        print(f"❌ Error setting up Claude config: {e}")
        return
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Restart Claude Desktop")
    print("2. Test by asking Claude: 'Find properties closest to clinic'")
    print("3. Check Claude Desktop logs if there are issues")
    
    print(f"\n🔧 Config file location: {get_claude_config_path()}")

if __name__ == "__main__":

    main()
