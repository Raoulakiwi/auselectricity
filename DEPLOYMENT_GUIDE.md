# Australian Electricity Market Dashboard - Deployment Guide

## Table of Contents
1. [Quick Start](#quick-start)
2. [System Requirements](#system-requirements)
3. [Installation Steps](#installation-steps)
4. [Configuration](#configuration)
5. [Running the Application](#running-the-application)
6. [Production Deployment](#production-deployment)
7. [Docker Deployment](#docker-deployment)
8. [Cloud Deployment](#cloud-deployment)
9. [Monitoring and Maintenance](#monitoring-and-maintenance)
10. [Troubleshooting](#troubleshooting)

## Quick Start

### Prerequisites Check
Before starting, ensure you have:
- Python 3.11+ installed
- Node.js 16+ installed
- Git installed
- Internet connection for package downloads

### 5-Minute Setup
```bash
# 1. Clone the repository
git clone <repository-url>
cd auselectricity

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Initialize the database
python initialize_data.py

# 4. Start the backend (in one terminal)
python start_backend.py

# 5. Start the frontend (in another terminal)
cd frontend
npm install
npm start
```

**Access the application:**
- Dashboard: http://localhost:3000
- API Documentation: http://localhost:8000/docs

## System Requirements

### Minimum Requirements
- **OS**: Windows 10, macOS 10.15, or Ubuntu 18.04+
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space
- **CPU**: Dual-core processor
- **Network**: Internet connection for data collection

### Recommended Requirements
- **OS**: Windows 11, macOS 12+, or Ubuntu 20.04+
- **RAM**: 8GB or more
- **Storage**: 10GB free space (for data storage)
- **CPU**: Quad-core processor
- **Network**: Stable broadband connection

### Software Dependencies
- **Python**: 3.11 or higher
- **Node.js**: 16 or higher
- **npm**: 8 or higher
- **Git**: Latest version

## Installation Steps

### Step 1: Environment Setup

#### Windows
```powershell
# Check Python version
python --version

# Check Node.js version
node --version
npm --version

# If not installed, download from:
# Python: https://www.python.org/downloads/
# Node.js: https://nodejs.org/
```

#### macOS
```bash
# Install using Homebrew
brew install python@3.11 node

# Or download from official websites
# Python: https://www.python.org/downloads/
# Node.js: https://nodejs.org/
```

#### Linux (Ubuntu/Debian)
```bash
# Update package list
sudo apt update

# Install Python 3.11
sudo apt install python3.11 python3.11-venv python3.11-pip

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### Step 2: Project Setup

#### Clone Repository
```bash
git clone <repository-url>
cd auselectricity
```

#### Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

#### Install Backend Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Install Frontend Dependencies
```bash
cd frontend
npm install
cd ..
```

### Step 3: Database Initialization

#### Initialize Database
```bash
python initialize_data.py
```

This will:
- Create SQLite database file
- Set up database tables
- Populate with sample data
- Verify database integrity

#### Verify Database
```bash
# Check if database was created
ls -la sql_app.db

# Test database connection
python -c "from backend.database.database import SessionLocal; db = SessionLocal(); print('Database connected successfully'); db.close()"
```

### Step 4: Configuration

#### Create Environment File
Create `.env` file in the root directory:

```env
# Database Configuration
DATABASE_URL=sqlite:///./sql_app.db

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true

# Frontend Configuration
REACT_APP_API_URL=http://localhost:8000

# Data Collection Configuration
SCRAPER_TIMEOUT=300
SCRAPER_RETRY_COUNT=3
SCRAPER_DELAY=5

# Logging Configuration
LOG_LEVEL=INFO
```

#### Configure CORS (if needed)
Edit `backend/api/main.py` to add additional origins:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://yourdomain.com"  # Add your domain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Running the Application

### Development Mode

#### Start Backend Server
```bash
# From project root directory
python start_backend.py
```

Expected output:
```
🚀 Starting Australian Electricity Market Dashboard API...
📊 Dashboard will be available at: http://localhost:8000
📖 API documentation at: http://localhost:8000/docs
🔄 Press Ctrl+C to stop the server
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

#### Start Frontend Server
```bash
# In a new terminal
cd frontend
npm start
```

Expected output:
```
Compiled successfully!

You can now view auselectricity in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.1.100:3000

Note that the development build is not optimized.
To create a production build, use npm run build.
```

### Using Startup Scripts

#### Windows
```batch
# Start backend
python start_backend.py

# Start frontend (in another terminal)
start_frontend.bat
```

#### Linux/macOS
```bash
# Start backend
python start_backend.py

# Start frontend (in another terminal)
./start_frontend.sh
```

### Verification

#### Test Backend
```bash
# Health check
curl http://localhost:8000/api/health

# API documentation
# Open http://localhost:8000/docs in browser
```

#### Test Frontend
```bash
# Open http://localhost:3000 in browser
# Verify dashboard loads correctly
# Test data collection button
```

## Production Deployment

### Database Upgrade

#### PostgreSQL Setup
```bash
# Install PostgreSQL
# Windows: Download from https://www.postgresql.org/download/windows/
# macOS: brew install postgresql
# Linux: sudo apt install postgresql postgresql-contrib

# Create database
sudo -u postgres createdb auselectricity

# Install Python PostgreSQL adapter
pip install psycopg2-binary
```

#### Update Database Configuration
```python
# In backend/database/database.py
SQLALCHEMY_DATABASE_URL = "postgresql://username:password@localhost/auselectricity"
```

### Backend Production Setup

#### Install Production Server
```bash
pip install gunicorn
```

#### Create Production Configuration
Create `gunicorn.conf.py`:

```python
bind = "0.0.0.0:8000"
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
preload_app = True
```

#### Start Production Server
```bash
gunicorn -c gunicorn.conf.py backend.api.main:app
```

### Frontend Production Build

#### Build Production Bundle
```bash
cd frontend
npm run build
```

#### Serve with Nginx
Create Nginx configuration:

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        root /path/to/auselectricity/frontend/build;
        index index.html;
        try_files $uri $uri/ /index.html;
    }
    
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### SSL Configuration

#### Using Let's Encrypt
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d yourdomain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

## Docker Deployment

### Create Dockerfile

#### Backend Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app
RUN chown -R app:app /app
USER app

# Expose port
EXPOSE 8000

# Start command
CMD ["python", "start_backend.py"]
```

#### Frontend Dockerfile
```dockerfile
FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY . .

# Build application
RUN npm run build

# Install serve to run the app
RUN npm install -g serve

# Expose port
EXPOSE 3000

# Start command
CMD ["serve", "-s", "build", "-l", "3000"]
```

### Docker Compose
Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/auselectricity
    depends_on:
      - db
    volumes:
      - ./data:/app/data

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:8000
    depends_on:
      - backend

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=auselectricity
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

### Docker Commands
```bash
# Build and start services
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Cloud Deployment

### AWS Deployment

#### EC2 Setup
```bash
# Launch EC2 instance (Ubuntu 20.04)
# Install dependencies
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-pip nodejs npm nginx

# Clone repository
git clone <repository-url>
cd auselectricity

# Set up application
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python initialize_data.py

# Set up systemd service
sudo nano /etc/systemd/system/auselectricity.service
```

#### Systemd Service
```ini
[Unit]
Description=Australian Electricity Market Dashboard
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/auselectricity
Environment=PATH=/home/ubuntu/auselectricity/venv/bin
ExecStart=/home/ubuntu/auselectricity/venv/bin/python start_backend.py
Restart=always

[Install]
WantedBy=multi-user.target
```

#### Start Service
```bash
sudo systemctl enable auselectricity
sudo systemctl start auselectricity
sudo systemctl status auselectricity
```

### Azure Deployment

#### App Service Setup
```bash
# Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Login to Azure
az login

# Create resource group
az group create --name auselectricity-rg --location eastus

# Create App Service plan
az appservice plan create --name auselectricity-plan --resource-group auselectricity-rg --sku B1

# Create web app
az webapp create --resource-group auselectricity-rg --plan auselectricity-plan --name auselectricity-app --runtime "PYTHON|3.11"
```

### Google Cloud Deployment

#### App Engine Setup
Create `app.yaml`:

```yaml
runtime: python311

env_variables:
  DATABASE_URL: "sqlite:///./sql_app.db"

handlers:
- url: /.*
  script: auto
```

Deploy:
```bash
# Install Google Cloud SDK
# Deploy to App Engine
gcloud app deploy
```

## Monitoring and Maintenance

### Logging Setup

#### Backend Logging
```python
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
```

#### Log Rotation
```bash
# Install logrotate
sudo apt install logrotate

# Create logrotate configuration
sudo nano /etc/logrotate.d/auselectricity
```

```bash
/path/to/auselectricity/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 ubuntu ubuntu
}
```

### Health Monitoring

#### Health Check Script
Create `health_check.py`:

```python
import requests
import sys

def check_backend():
    try:
        response = requests.get('http://localhost:8000/api/health', timeout=5)
        if response.status_code == 200:
            print("Backend: OK")
            return True
        else:
            print("Backend: FAILED")
            return False
    except Exception as e:
        print(f"Backend: ERROR - {e}")
        return False

def check_frontend():
    try:
        response = requests.get('http://localhost:3000', timeout=5)
        if response.status_code == 200:
            print("Frontend: OK")
            return True
        else:
            print("Frontend: FAILED")
            return False
    except Exception as e:
        print(f"Frontend: ERROR - {e}")
        return False

if __name__ == "__main__":
    backend_ok = check_backend()
    frontend_ok = check_frontend()
    
    if not (backend_ok and frontend_ok):
        sys.exit(1)
```

#### Cron Job for Health Checks
```bash
# Add to crontab
crontab -e

# Check every 5 minutes
*/5 * * * * /path/to/auselectricity/health_check.py
```

### Data Backup

#### Database Backup Script
Create `backup_database.py`:

```python
import shutil
import datetime
import os

def backup_database():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"backup_{timestamp}.db"
    backup_path = f"backups/{backup_filename}"
    
    # Create backups directory if it doesn't exist
    os.makedirs("backups", exist_ok=True)
    
    # Copy database file
    shutil.copy2("sql_app.db", backup_path)
    
    print(f"Database backed up to: {backup_path}")
    
    # Keep only last 30 backups
    backup_files = sorted([f for f in os.listdir("backups") if f.startswith("backup_")])
    if len(backup_files) > 30:
        for old_backup in backup_files[:-30]:
            os.remove(f"backups/{old_backup}")

if __name__ == "__main__":
    backup_database()
```

#### Automated Backups
```bash
# Add to crontab for daily backups
0 2 * * * /path/to/auselectricity/backup_database.py
```

### Performance Monitoring

#### System Metrics
```bash
# Install monitoring tools
sudo apt install htop iotop nethogs

# Monitor system resources
htop
iotop
nethogs
```

#### Application Metrics
```python
# Add to backend for metrics collection
import psutil
import time

def get_system_metrics():
    return {
        'cpu_percent': psutil.cpu_percent(),
        'memory_percent': psutil.virtual_memory().percent,
        'disk_percent': psutil.disk_usage('/').percent,
        'timestamp': time.time()
    }
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Port Already in Use
**Error**: `Address already in use`
**Solution**:
```bash
# Find process using port
netstat -tulpn | grep :8000
# Kill process
kill -9 <PID>
```

#### 2. Database Locked
**Error**: `database is locked`
**Solution**:
```bash
# Check for running processes
ps aux | grep python
# Kill all Python processes
pkill -f python
# Restart application
```

#### 3. Memory Issues
**Error**: `Out of memory`
**Solution**:
```bash
# Check memory usage
free -h
# Increase swap space
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

#### 4. Network Connectivity
**Error**: `Connection refused`
**Solution**:
```bash
# Check firewall
sudo ufw status
# Allow ports
sudo ufw allow 8000
sudo ufw allow 3000
```

#### 5. Permission Issues
**Error**: `Permission denied`
**Solution**:
```bash
# Fix file permissions
chmod +x start_frontend.sh
chmod 644 sql_app.db
# Fix ownership
sudo chown -R $USER:$USER /path/to/auselectricity
```

### Debug Mode

#### Enable Debug Logging
```python
# In backend/api/main.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

#### Frontend Debug Mode
```bash
# Set environment variable
export REACT_APP_DEBUG=true
npm start
```

### Recovery Procedures

#### Database Recovery
```bash
# Restore from backup
cp backups/backup_20250911_120000.db sql_app.db
# Reinitialize if needed
python initialize_data.py
```

#### Application Recovery
```bash
# Stop all services
pkill -f python
pkill -f node

# Clean up
rm -rf node_modules
rm -rf venv

# Reinstall
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd frontend && npm install && cd ..

# Restart
python start_backend.py
```

---

This deployment guide provides comprehensive instructions for setting up, configuring, and maintaining the Australian Electricity Market Dashboard in various environments. Follow the steps carefully and refer to the troubleshooting section if you encounter any issues.
