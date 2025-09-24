#!/bin/bash

# Australian Electricity Market Dashboard - Server Setup Script
# For Ubuntu servers with Python 3.12

echo "🚀 Setting up Australian Electricity Market Dashboard on Ubuntu server..."

# Update system packages
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install system dependencies for Python packages
echo "🔧 Installing system build dependencies..."
sudo apt install -y \
    python3-dev \
    python3-venv \
    python3-pip \
    build-essential \
    libssl-dev \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libjpeg-dev \
    libpng-dev \
    pkg-config \
    postgresql-client \
    curl \
    git

# Install Node.js and npm for frontend (if needed)
echo "📦 Installing Node.js and npm..."
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Verify installations
echo "✅ Verifying installations..."
python3 --version
node --version
npm --version

echo "🎉 System setup complete!"
echo ""
echo "Next steps:"
echo "1. Create virtual environment: python3 -m venv venv"
echo "2. Activate virtual environment: source venv/bin/activate"
echo "3. Upgrade pip: python3 -m pip install --upgrade pip"
echo "4. Install requirements: pip install -r requirements.txt"
echo "5. Start the application: python start_backend.py"
