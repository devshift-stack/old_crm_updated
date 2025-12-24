#!/bin/bash
# Mac Remote Assistant - Auto Installer
# Easy one-command installation

set -e  # Exit on error

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                                                               ║"
echo "║     🎉 MAC REMOTE ASSISTANT v5.0 - AUTO INSTALLER           ║"
echo "║                                                               ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Python 3 is installed
echo "🔍 Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed!${NC}"
    echo "Please install Python 3 first: https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo -e "${GREEN}✓ Found: $PYTHON_VERSION${NC}"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
if [ -d "venv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment already exists, skipping...${NC}"
else
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi
echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"
echo ""

# Install dependencies
echo "📚 Installing dependencies..."
echo "   This may take a minute..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Dependencies installed successfully${NC}"
else
    echo -e "${RED}❌ Failed to install dependencies${NC}"
    exit 1
fi
echo ""

# Create .env file
echo "⚙️  Setting up configuration..."
if [ -f ".env" ]; then
    echo -e "${YELLOW}⚠️  .env file already exists${NC}"
    read -p "   Overwrite? (y/N): " overwrite
    if [[ ! $overwrite =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}   Keeping existing .env${NC}"
    else
        cp .env.optimized .env
        echo -e "${GREEN}✓ .env created from .env.optimized${NC}"
    fi
else
    cp .env.optimized .env
    echo -e "${GREEN}✓ .env created from .env.optimized${NC}"
fi
echo ""

# Ask for API key
echo "🔑 API Key Setup"
echo "────────────────────────────────────────────────────────────────"
echo ""
echo "Du brauchst einen Claude API Key von Anthropic:"
echo "👉 https://console.anthropic.com/"
echo ""
read -p "Hast du bereits einen API Key? (y/N): " has_key

if [[ $has_key =~ ^[Yy]$ ]]; then
    echo ""
    read -p "Gib deinen Claude API Key ein (sk-ant-...): " api_key

    if [[ $api_key == sk-ant-* ]]; then
        # Update .env with API key
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            sed -i '' "s/ANTHROPIC_API_KEY=.*/ANTHROPIC_API_KEY=$api_key/" .env
        else
            # Linux
            sed -i "s/ANTHROPIC_API_KEY=.*/ANTHROPIC_API_KEY=$api_key/" .env
        fi
        echo -e "${GREEN}✓ API Key configured${NC}"
    else
        echo -e "${YELLOW}⚠️  Invalid API Key format (should start with sk-ant-)${NC}"
        echo -e "${YELLOW}   Please edit .env manually and add your key${NC}"
    fi
else
    echo ""
    echo -e "${YELLOW}📝 Please get an API key and add it to .env:${NC}"
    echo "   1. Visit: https://console.anthropic.com/"
    echo "   2. Create account / Login"
    echo "   3. Settings → API Keys → Create Key"
    echo "   4. Edit .env and set: ANTHROPIC_API_KEY=sk-ant-your-key"
fi
echo ""

# Create Dropbox folder if needed
echo "📂 Setting up Cloud Sync folder..."
DROPBOX_PATH="$HOME/Dropbox/MacAssistant"
if [ ! -d "$DROPBOX_PATH" ]; then
    echo "   Creating: $DROPBOX_PATH"
    mkdir -p "$DROPBOX_PATH"
    echo -e "${GREEN}✓ Cloud Sync folder created${NC}"
else
    echo -e "${GREEN}✓ Cloud Sync folder exists${NC}"
fi
echo ""

# Installation complete
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                                                               ║"
echo "║                  ✅ INSTALLATION COMPLETE!                    ║"
echo "║                                                               ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Show what's configured
echo "📊 Deine Konfiguration:"
echo "────────────────────────────────────────────────────────────────"
echo "✅ Web Server:   http://localhost:5000"
echo "✅ Cloud Sync:   $DROPBOX_PATH"
echo "❌ Slack Bot:    Disabled (du nutzt Linear)"
echo "❌ Telegram Bot: Disabled (optional)"
echo ""

# Ask to start
echo "🚀 Möchtest du die App jetzt starten?"
read -p "Start? (Y/n): " start_now

if [[ ! $start_now =~ ^[Nn]$ ]]; then
    echo ""
    echo "Starting Mac Remote Assistant..."
    echo "────────────────────────────────────────────────────────────────"
    echo ""
    python3 main.py
else
    echo ""
    echo "────────────────────────────────────────────────────────────────"
    echo "📝 Um die App später zu starten:"
    echo ""
    echo "   cd $(pwd)"
    echo "   source venv/bin/activate"
    echo "   python3 main.py"
    echo ""
    echo "📖 Dann öffne im Browser: http://localhost:5000"
    echo "────────────────────────────────────────────────────────────────"
    echo ""
fi
