# Australian Electricity Market Dashboard - Setup Instructions

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Installation Steps](#installation-steps)
3. [Configuration](#configuration)
4. [Running the Application](#running-the-application)
5. [Verification](#verification)
6. [Troubleshooting](#troubleshooting)
7. [Next Steps](#next-steps)

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10, macOS 10.15, or Ubuntu 18.04+
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space
- **CPU**: Dual-core processor
- **Network**: Internet connection for package downloads and data collection

### Software Requirements
- **Python**: 3.11 or higher
- **Node.js**: 16 or higher
- **npm**: 8 or higher (comes with Node.js)
- **Git**: Latest version

### Check Your System
Before starting, verify you have the required software:

```bash
# Check Python version
python --version
# Should show Python 3.11.x or higher

# Check Node.js version
node --version
# Should show v16.x.x or higher

# Check npm version
npm --version
# Should show 8.x.x or higher

# Check Git
git --version
# Should show git version 2.x.x or higher
```

## Installation Steps

### Step 1: Download and Install Prerequisites

#### If you don't have Python 3.11+:
- **Windows**: Download from [python.org](https://www.python.org/downloads/)
- **macOS**: Use Homebrew: `brew install python@3.11`
- **Linux**: `sudo apt install python3.11 python3.11-venv python3.11-pip`

#### If you don't have Node.js 16+:
- **All platforms**: Download from [nodejs.org](https://nodejs.org/)
- **macOS**: Use Homebrew: `brew install node`
- **Linux**: `curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash - && sudo apt-get install -y nodejs`

### Step 2: Clone the Repository

```bash
# Clone the repository
git clone <repository-url>
cd auselectricity
```

### Step 3: Set Up Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install Python dependencies
pip install -r requirements.txt
```

### Step 4: Set Up Frontend Dependencies

```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Return to root directory
cd ..
```

### Step 5: Initialize the Database

```bash
# Make sure you're in the root directory and virtual environment is activated
python initialize_data.py
```

This will:
- Create the SQLite database file
- Set up all required tables
- Populate with sample data
- Verify the database is working correctly

## Configuration

### Environment Variables (Optional)
Create a `.env` file in the root directory for custom configuration:

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
```

### CORS Configuration (If Needed)
If you need to access the API from a different domain, edit `backend/api/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://yourdomain.com"  # Add your domain here
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Running the Application

### Method 1: Using Startup Scripts (Recommended)

#### Start Backend Server
```bash
# Make sure you're in the root directory with virtual environment activated
python start_backend.py
```

You should see output like:
```
🚀 Starting Australian Electricity Market Dashboard API...
📊 Dashboard will be available at: http://localhost:8000
📖 API documentation at: http://localhost:8000/docs
🔄 Press Ctrl+C to stop the server
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

#### Start Frontend Server (New Terminal)
```bash
# Open a new terminal/command prompt
cd auselectricity/frontend

# Start the React development server
npm start
```

You should see output like:
```
Compiled successfully!

You can now view auselectricity in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.1.100:3000

Note that the development build is not optimized.
To create a production build, use npm run build.
```

### Method 2: Using Batch/Shell Scripts

#### Windows
```batch
# Start backend (Terminal 1)
python start_backend.py

# Start frontend (Terminal 2)
start_frontend.bat
```

#### macOS/Linux
```bash
# Start backend (Terminal 1)
python start_backend.py

# Start frontend (Terminal 2)
./start_frontend.sh
```

### Method 3: Manual Commands

#### Backend
```bash
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Start backend
uvicorn backend.api.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Frontend
```bash
# Navigate to frontend directory
cd frontend

# Start development server
npm start
```

## Verification

### 1. Check Backend API
Open your browser and visit:
- **API Health Check**: http://localhost:8000/api/health
- **API Documentation**: http://localhost:8000/docs

You should see:
- Health check returns: `{"status": "healthy", "timestamp": "..."}`
- Swagger UI documentation page loads

### 2. Check Frontend Dashboard
Open your browser and visit:
- **Main Dashboard**: http://localhost:3000

You should see:
- Australian Electricity Market Dashboard loads
- Navigation menu with Dashboard, Electricity Prices, Dam Levels, Predictions
- Data collection control panel at the top
- Charts and metrics displaying data

### 3. Test Data Collection
1. Click the "Start Data Collection" button on the dashboard
2. Watch the status update in real-time
3. Verify new data appears in the charts

### 4. Test API Endpoints
```bash
# Test electricity prices endpoint
curl http://localhost:8000/api/electricity/prices/current

# Test dam levels endpoint
curl http://localhost:8000/api/dams/levels/current

# Test scraper status
curl http://localhost:8000/api/scraper/status
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Python Not Found
**Error**: `python: command not found` or `Python was not found`

**Solution**:
- Install Python from [python.org](https://www.python.org/downloads/)
- Make sure to check "Add Python to PATH" during installation
- Restart your terminal/command prompt after installation

#### 2. Node.js Not Found
**Error**: `node: command not found` or `npm: command not found`

**Solution**:
- Install Node.js from [nodejs.org](https://nodejs.org/)
- Restart your terminal/command prompt after installation

#### 3. Port Already in Use
**Error**: `Address already in use` or `Port 8000 is already in use`

**Solution**:
```bash
# Find process using port 8000
netstat -an | findstr :8000  # Windows
lsof -i :8000                # macOS/Linux

# Kill the process
taskkill /F /PID <process_id>  # Windows
kill -9 <process_id>           # macOS/Linux
```

#### 4. Database Connection Error
**Error**: `sqlite3.OperationalError: database is locked`

**Solution**:
```bash
# Stop all Python processes
pkill -f python  # macOS/Linux
taskkill /F /IM python.exe  # Windows

# Recreate database
rm sql_app.db  # macOS/Linux
del sql_app.db  # Windows
python initialize_data.py
```

#### 5. Frontend Compilation Errors
**Error**: `Module not found: Error: Can't resolve 'react-bootstrap-icons'`

**Solution**:
```bash
cd frontend
npm install react-bootstrap-icons
npm start
```

#### 6. Permission Denied (macOS/Linux)
**Error**: `Permission denied` when running scripts

**Solution**:
```bash
# Make scripts executable
chmod +x start_frontend.sh

# Fix file permissions
sudo chown -R $USER:$USER /path/to/auselectricity
```

#### 7. Virtual Environment Issues
**Error**: `No module named 'fastapi'` or similar import errors

**Solution**:
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### 8. Frontend Build Errors
**Error**: Various compilation errors in React

**Solution**:
```bash
cd frontend

# Clear cache and reinstall
npm cache clean --force
rm -rf node_modules
rm package-lock.json
npm install
npm start
```

### Getting Help

If you encounter issues not covered here:

1. **Check the logs**: Look at the terminal output for error messages
2. **Verify requirements**: Make sure all software versions meet requirements
3. **Check documentation**: Review the technical documentation
4. **Create an issue**: Report the problem with detailed error messages

## Next Steps

### 1. Explore the Dashboard
- Navigate through different pages (Electricity Prices, Dam Levels, Predictions)
- Try the data collection button
- Explore the interactive charts

### 2. Review the API
- Visit http://localhost:8000/docs to see the interactive API documentation
- Try the API endpoints directly
- Test different query parameters

### 3. Customize the Application
- Modify the data collection sources
- Add new chart types
- Customize the dashboard layout

### 4. Learn More
- Read the [Technical Documentation](TECHNICAL_DOCUMENTATION.md)
- Review the [API Reference](API_REFERENCE.md)
- Check the [Developer Guide](DEVELOPER_GUIDE.md)

### 5. Deploy to Production
- Follow the [Deployment Guide](DEPLOYMENT_GUIDE.md)
- Set up a production database
- Configure proper security settings

## Success!

If you've reached this point, congratulations! You have successfully set up the Australian Electricity Market Dashboard. The application should be running with:

- ✅ Backend API at http://localhost:8000
- ✅ Frontend Dashboard at http://localhost:3000
- ✅ Database populated with sample data
- ✅ Data collection system working
- ✅ All features functional

You can now start monitoring Australian electricity prices and dam levels, and begin developing your trading strategies based on the data insights provided by the dashboard.

---

**Need help?** Check the troubleshooting section above or refer to the comprehensive documentation in the project repository.
