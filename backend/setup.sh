#!/bin/bash

# Multi-Channel Customer Query Router Setup Script

echo "======================================"
echo "  FinLink Query Router - Setup"
echo "======================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed"

# Check for .env file
echo ""
if [ ! -f .env ]; then
    echo "⚠️  No .env file found"
    echo "Creating .env from template..."
    
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ Created .env file"
        echo ""
        echo "📝 Please edit .env and add your Google API key:"
        echo "   GOOGLE_API_KEY=your_api_key_here"
        echo ""
        echo "Get your API key at: https://makersuite.google.com/app/apikey"
    else
        echo "Creating basic .env file..."
        echo "GOOGLE_API_KEY=your_gemini_api_key_here" > .env
        echo "✅ Created .env file"
        echo ""
        echo "📝 Please edit .env and add your Google API key"
    fi
else
    echo "✅ .env file exists"
fi

echo ""
echo "======================================"
echo "  Setup Complete!"
echo "======================================"
echo ""
echo "Next steps:"
echo "  1. Edit .env and add your API key (if not done)"
echo "  2. Run: python3 init_system.py"
echo "  3. Run: python3 demo.py"
echo "  4. Run: python3 app.py"
echo ""

