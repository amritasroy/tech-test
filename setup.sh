#!/bin/bash
# Setup script for Git Commit Tracker

echo "🔧 Setting up Git Commit Tracker..."
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✓ Found Python $PYTHON_VERSION"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Setup complete!"
    echo ""
    echo "🚀 Quick Start:"
    echo "   python git_tracker.py                    # Analyze current directory"
    echo "   python git_tracker.py /path/to/repo      # Analyze specific repo"
    echo "   python git_tracker.py --help             # See all options"
    echo ""
    echo "📖 See README.md and QUICKSTART.md for more information"
else
    echo ""
    echo "❌ Installation failed. Please check the error messages above."
    exit 1
fi
