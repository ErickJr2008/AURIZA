"""
Quick start script for AURIZA Backend
Run this to get started quickly
"""

import subprocess
import sys
import os


def main():
    print(\"🚀 AURIZA Backend - Quick Start\")
    print(\"=\" * 50)
    
    # Check Python version
    if sys.version_info < (3, 10):
        print(\"❌ Python 3.10+ required\")
        sys.exit(1)
    
    print(\"✅ Python version OK\")
    
    # Create virtual environment if it doesn't exist
    if not os.path.exists(\"venv\"):
        print(\"\\n📦 Creating virtual environment...\")
        subprocess.run([sys.executable, \"-m\", \"venv\", \"venv\"], check=True)
        print(\"✅ Virtual environment created\")
    
    # Activate virtual environment and install dependencies
    print(\"\\n📥 Installing dependencies...\")
    
    if sys.platform == \"win32\":
        activate_cmd = \".\\\\venv\\\\Scripts\\\\activate.bat\"
        pip_cmd = \".\\\\venv\\\\Scripts\\\\pip.exe\"
    else:
        activate_cmd = \"source venv/bin/activate\"
        pip_cmd = \"./venv/bin/pip\"
    
    subprocess.run([pip_cmd, \"install\", \"-r\", \"requirements.txt\"], check=True)
    print(\"✅ Dependencies installed\")
    
    # Copy .env file if it doesn't exist
    if not os.path.exists(\".env\"):
        print(\"\\n⚙️  Creating .env file...\")
        if os.path.exists(\".env.example\"):
            with open(\".env.example\", \"r\") as src:
                content = src.read()
            with open(\".env\", \"w\") as dst:
                dst.write(content)
            print(\"✅ .env created from .env.example\")
        else:
            print(\"⚠️  .env.example not found\")
    
    # Run server
    print(\"\\n\" + \"=\" * 50)
    print(\"🎯 Starting AURIZA Backend...\")
    print(\"=\" * 50)
    print(\"📍 Server: http://localhost:8000\")
    print(\"📚 Docs: http://localhost:8000/docs\")
    print(\"\\nPress Ctrl+C to stop\")
    print(\"=\" * 50 + \"\\n\")
    
    if sys.platform == \"win32\":
        subprocess.run([
            \".\\\\venv\\\\Scripts\\\\python.exe\", \"-m\", \"uvicorn\",
            \"app.main:app\", \"--reload\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"
        ])
    else:
        subprocess.run([
            \"./venv/bin/python\", \"-m\", \"uvicorn\",
            \"app.main:app\", \"--reload\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"
        ])


if __name__ == \"__main__\":
    main()
