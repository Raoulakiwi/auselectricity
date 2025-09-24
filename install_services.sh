#!/bin/bash

# Australian Electricity Market Dashboard - Service Installation Script
# This script sets up systemd services for auto-startup

set -e  # Exit on any error

echo "🚀 Installing Australian Electricity Market Dashboard Services..."

# Check if running as root or with sudo
if [[ $EUID -eq 0 ]]; then
   echo "❌ This script should not be run as root. Please run as ubuntu user."
   exit 1
fi

# Get the current directory (should be /home/ubuntu/auselectricity)
PROJECT_DIR=$(pwd)
USER=$(whoami)

echo "📁 Project directory: $PROJECT_DIR"
echo "👤 User: $USER"

# Verify we're in the right directory
if [[ ! -f "start_backend.py" ]]; then
    echo "❌ Error: start_backend.py not found. Please run this script from the project root directory."
    exit 1
fi

# Check if virtual environment exists
if [[ ! -d "venv" ]]; then
    echo "❌ Error: Virtual environment not found. Please create it first:"
    echo "   python3 -m venv venv"
    echo "   source venv/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Check if frontend node_modules exists
if [[ ! -d "frontend/node_modules" ]]; then
    echo "❌ Error: Frontend node_modules not found. Please install dependencies first:"
    echo "   cd frontend"
    echo "   npm install"
    exit 1
fi

echo "✅ Prerequisites check passed"

# Update service files with correct paths
echo "🔧 Updating service files with correct paths..."

# Update backend service file
sed -i "s|/home/ubuntu/auselectricity|$PROJECT_DIR|g" auselectricity-backend.service
sed -i "s|User=ubuntu|User=$USER|g" auselectricity-backend.service
sed -i "s|Group=ubuntu|Group=$USER|g" auselectricity-backend.service

# Update frontend service file
sed -i "s|/home/ubuntu/auselectricity|$PROJECT_DIR|g" auselectricity-frontend.service
sed -i "s|User=ubuntu|User=$USER|g" auselectricity-frontend.service
sed -i "s|Group=ubuntu|Group=$USER|g" auselectricity-frontend.service

# Copy service files to systemd directory
echo "📋 Installing systemd service files..."
sudo cp auselectricity-backend.service /etc/systemd/system/
sudo cp auselectricity-frontend.service /etc/systemd/system/

# Reload systemd to recognize new services
echo "🔄 Reloading systemd configuration..."
sudo systemctl daemon-reload

# Enable services to start on boot
echo "⚡ Enabling services for auto-startup..."
sudo systemctl enable auselectricity-backend.service
sudo systemctl enable auselectricity-frontend.service

# Start services
echo "🚀 Starting services..."
sudo systemctl start auselectricity-backend.service
sudo systemctl start auselectricity-frontend.service

# Check service status
echo "📊 Checking service status..."
echo ""
echo "Backend service status:"
sudo systemctl status auselectricity-backend.service --no-pager -l
echo ""
echo "Frontend service status:"
sudo systemctl status auselectricity-frontend.service --no-pager -l

echo ""
echo "🎉 Services installed and started successfully!"
echo ""
echo "📋 Useful commands:"
echo "  Check status:     sudo systemctl status auselectricity-backend.service"
echo "  Check logs:       sudo journalctl -u auselectricity-backend.service -f"
echo "  Restart service:  sudo systemctl restart auselectricity-backend.service"
echo "  Stop service:     sudo systemctl stop auselectricity-backend.service"
echo "  Disable service:  sudo systemctl disable auselectricity-backend.service"
echo ""
echo "🌐 Your application should be available at:"
echo "  Backend API:  http://$(curl -s ifconfig.me):8000"
echo "  Frontend:     http://$(curl -s ifconfig.me):3000"
echo "  API Docs:     http://$(curl -s ifconfig.me):8000/docs"
