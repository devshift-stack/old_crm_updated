#!/bin/bash
# Mac Remote Assistant - Quick Install from GitHub
# Run this on your Mac: curl -s https://raw.githubusercontent.com/devshift-stack/old_crm_updated/claude/mac-remote-access-app-qiKTl/quick-install.sh | bash

set -e

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║   🚀 MAC REMOTE ASSISTANT - GitHub Quick Install             ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check if git is installed
echo "🔍 Checking git installation..."
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git is not installed!${NC}"
    echo "Install: xcode-select --install"
    exit 1
fi
echo -e "${GREEN}✓ Git found${NC}"
echo ""

# Clone repository
echo "📥 Cloning repository from GitHub..."
cd ~
if [ -d "old_crm_updated" ]; then
    echo -e "${YELLOW}⚠️  Directory 'old_crm_updated' already exists${NC}"
    read -p "   Remove and re-clone? (y/N): " remake
    if [[ $remake =~ ^[Yy]$ ]]; then
        rm -rf old_crm_updated
        git clone https://github.com/devshift-stack/old_crm_updated.git
    else
        echo "   Using existing directory..."
    fi
else
    git clone https://github.com/devshift-stack/old_crm_updated.git
fi

cd old_crm_updated
echo -e "${GREEN}✓ Repository cloned${NC}"
echo ""

# Checkout branch
echo "🔀 Checking out branch..."
git checkout claude/mac-remote-access-app-qiKTl
echo -e "${GREEN}✓ Branch checked out${NC}"
echo ""

# Run installer
echo "⚡ Running auto-installer..."
echo ""
cd mac_assistant
chmod +x install.sh
./install.sh
