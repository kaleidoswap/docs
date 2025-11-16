#!/bin/bash
# Setup script for KaleidoSwap Mintlify Documentation

set -e

echo "🚀 Setting up KaleidoSwap Mintlify Documentation"
echo "================================================"
echo ""

# Check for Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed"
    echo "Please install Node.js 18.x or higher: https://nodejs.org/"
    exit 1
fi

echo "✓ Node.js found: $(node --version)"

# Check for npm
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed"
    exit 1
fi

echo "✓ npm found: $(npm --version)"
echo ""

# Install Mintlify CLI
echo "📦 Installing Mintlify CLI..."
if command -v mintlify &> /dev/null; then
    echo "✓ Mintlify CLI already installed: $(mintlify --version)"
else
    npm install -g mintlify
    echo "✓ Mintlify CLI installed successfully"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Add your logo files to the assets/ directory"
echo "   - logo-dark.svg"
echo "   - logo-light.svg"
echo "   - favicon.png"
echo ""
echo "2. Update mint.json with your branding"
echo ""
echo "3. Start the development server:"
echo "   $ mintlify dev"
echo ""
echo "4. View your docs at http://localhost:3000"
echo ""
echo "For more information, see README.md"
