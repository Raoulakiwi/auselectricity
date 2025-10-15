#!/bin/bash

# Australian Electricity Market Dashboard - Production Setup Script
# Sets up nginx reverse proxy and production build

set -e

echo "🚀 Setting up Australian Electricity Market Dashboard for Production..."

# Check if running as root or with sudo
if [[ $EUID -eq 0 ]]; then
   echo "❌ This script should not be run as root. Please run as ubuntu user."
   exit 1
fi

# Get the current directory
PROJECT_DIR=$(pwd)
USER=$(whoami)

echo "📁 Project directory: $PROJECT_DIR"
echo "👤 User: $USER"

# Verify we're in the right directory
if [[ ! -f "start_backend.py" ]]; then
    echo "❌ Error: start_backend.py not found. Please run this script from the project root directory."
    exit 1
fi

# Install nginx
echo "📦 Installing nginx..."
sudo apt update
sudo apt install -y nginx

# Create nginx configuration
echo "🔧 Setting up nginx configuration..."
sudo cp nginx-auselectricity.conf /etc/nginx/sites-available/auselectricity

# Enable the site
sudo ln -sf /etc/nginx/sites-available/auselectricity /etc/nginx/sites-enabled/

# Remove default nginx site
sudo rm -f /etc/nginx/sites-enabled/default

# Test nginx configuration
echo "🧪 Testing nginx configuration..."
sudo nginx -t

# Build the frontend for production
echo "🏗️ Building frontend for production..."
cd frontend

# Check if node_modules exists
if [[ ! -d "node_modules" ]]; then
    echo "📦 Installing frontend dependencies..."
    npm install
fi

# Build the production version
echo "🔨 Building production version..."
REACT_APP_API_URL=http://localhost:8000 npm run build

cd ..

# Set proper permissions
echo "🔐 Setting proper permissions..."
sudo chown -R $USER:$USER $PROJECT_DIR/frontend/build
sudo chmod -R 755 $PROJECT_DIR/frontend/build

# Update service files for production
echo "🔧 Updating service files for production..."

# Update backend service file
sed -i "s|/home/ubuntu/auselectricity|$PROJECT_DIR|g" auselectricity-backend.service
sed -i "s|User=ubuntu|User=$USER|g" auselectricity-backend.service
sed -i "s|Group=ubuntu|Group=$USER|g" auselectricity-backend.service

# Update frontend production service file
sed -i "s|/home/ubuntu/auselectricity|$PROJECT_DIR|g" auselectricity-frontend-production.service
sed -i "s|User=ubuntu|User=$USER|g" auselectricity-frontend-production.service
sed -i "s|Group=ubuntu|Group=$USER|g" auselectricity-frontend-production.service

# Copy service files to systemd directory
echo "📋 Installing systemd service files..."
sudo cp auselectricity-backend.service /etc/systemd/system/
sudo cp auselectricity-frontend-production.service /etc/systemd/system/

# Reload systemd to recognize new services
echo "🔄 Reloading systemd configuration..."
sudo systemctl daemon-reload

# Enable services to start on boot
echo "⚡ Enabling services for auto-startup..."
sudo systemctl enable auselectricity-backend.service
sudo systemctl enable auselectricity-frontend-production.service

# Start services
echo "🚀 Starting services..."
sudo systemctl start auselectricity-backend.service
sudo systemctl start auselectricity-frontend-production.service

# Start and enable nginx
echo "🌐 Starting nginx..."
sudo systemctl enable nginx
sudo systemctl start nginx

# Check service status
echo "📊 Checking service status..."
echo ""
echo "Backend service status:"
sudo systemctl status auselectricity-backend.service --no-pager -l
echo ""
echo "Frontend build service status:"
sudo systemctl status auselectricity-frontend-production.service --no-pager -l
echo ""
echo "Nginx status:"
sudo systemctl status nginx --no-pager -l

echo ""
echo "🎉 Production setup complete!"
echo ""
echo "📋 Useful commands:"
echo "  Check nginx status:    sudo systemctl status nginx"
echo "  Check nginx logs:      sudo journalctl -u nginx -f"
echo "  Restart nginx:         sudo systemctl restart nginx"
echo "  Test nginx config:     sudo nginx -t"
echo "  Reload nginx:          sudo nginx -s reload"
echo ""
echo "🌐 Your application is now available at:"
echo "  Main site:     http://$(curl -s ifconfig.me)"
echo "  API:           http://$(curl -s ifconfig.me)/api/"
echo "  API Docs:      http://$(curl -s ifconfig.me)/api/docs"
echo ""
echo "🔧 To rebuild frontend after changes:"
echo "  cd frontend && npm run build"
echo "  sudo systemctl restart nginx"


