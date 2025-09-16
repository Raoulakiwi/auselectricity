# Australian Electricity Market Dashboard - Technical Documentation

## Table of Contents
1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Technology Stack](#technology-stack)
4. [Project Structure](#project-structure)
5. [Database Schema](#database-schema)
6. [API Documentation](#api-documentation)
7. [Data Collection System](#data-collection-system)
8. [Frontend Components](#frontend-components)
9. [Installation Guide](#installation-guide)
10. [Configuration](#configuration)
11. [Deployment](#deployment)
12. [Troubleshooting](#troubleshooting)
13. [Development Guidelines](#development-guidelines)

## System Overview

The Australian Electricity Market Dashboard is a full-stack web application designed to monitor and analyze Australian wholesale electricity prices and dam levels across all states. The platform provides real-time data visualization, historical trend analysis, and predictive insights for energy trading.

### Key Features
- Real-time electricity price monitoring across 5 regions (NSW, VIC, QLD, SA, TAS)
- Dam level tracking for major water storage facilities
- Historical data analysis with 30-day trends
- Interactive charts and visualizations
- Data collection automation via web scraping
- RESTful API for data access
- Responsive web interface

## Architecture

### High-Level Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   Database      │
│   (React.js)    │◄──►│   (FastAPI)     │◄──►│   (SQLite)      │
│   Port: 3000    │    │   Port: 8000    │    │   File-based    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Browser   │    │  Data Scrapers  │    │  Data Storage   │
│   Dashboard UI  │    │  Background     │    │  Historical     │
│                 │    │  Collection     │    │  Records        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Component Architecture
- **Frontend**: React.js SPA with Bootstrap styling
- **Backend**: FastAPI REST API with SQLAlchemy ORM
- **Database**: SQLite for development, easily upgradeable to PostgreSQL
- **Data Collection**: Python-based web scrapers with background processing
- **Real-time Updates**: Polling-based data refresh

## Technology Stack

### Backend Technologies
- **Python 3.11+**: Core programming language
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM)
- **SQLite**: Lightweight database engine
- **Uvicorn**: ASGI server for FastAPI
- **Pydantic**: Data validation using Python type annotations
- **Requests**: HTTP library for web scraping
- **BeautifulSoup4**: HTML parsing library
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Scikit-learn**: Machine learning library for predictions

### Frontend Technologies
- **React.js 18**: JavaScript library for building user interfaces
- **React Router**: Declarative routing for React
- **React Bootstrap**: Bootstrap components built with React
- **React Bootstrap Icons**: Icon library
- **Axios**: HTTP client for API requests
- **Recharts**: Composable charting library
- **React Query**: Data fetching and caching library

### Development Tools
- **Node.js & npm**: Package management for frontend
- **pip**: Package management for Python
- **Git**: Version control
- **PowerShell/Bash**: Command line interface

## Project Structure

```
auselectricity/
├── backend/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI application entry point
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── electricity.py      # Electricity price API endpoints
│   │       ├── dams.py            # Dam level API endpoints
│   │       └── scraper.py         # Data collection API endpoints
│   ├── data/
│   │   ├── collectors/
│   │   │   ├── __init__.py
│   │   │   ├── aemo_collector.py   # AEMO data collection (placeholder)
│   │   │   ├── dam_collector.py    # Dam data collection (placeholder)
│   │   │   └── robust_data_scrapers.py  # Main data collection logic
│   │   └── models/
│   │       ├── __init__.py
│   │       ├── electricity.py      # Electricity price Pydantic models
│   │       └── dams.py            # Dam level Pydantic models
│   ├── database/
│   │   ├── __init__.py
│   │   └── database.py            # Database configuration and models
│   └── ml/
│       ├── __init__.py
│       └── price_predictor.py     # Machine learning price prediction
├── frontend/
│   ├── public/
│   │   ├── index.html
│   │   └── manifest.json
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navigation.js       # Main navigation component
│   │   │   ├── PriceChart.js       # Electricity price chart
│   │   │   ├── DamLevelChart.js    # Dam level chart
│   │   │   ├── MetricCard.js       # Metric display card
│   │   │   └── ScraperControl.js   # Data collection control
│   │   ├── pages/
│   │   │   ├── Dashboard.js        # Main dashboard page
│   │   │   ├── ElectricityPrices.js # Electricity prices page
│   │   │   ├── DamLevels.js        # Dam levels page
│   │   │   └── Predictions.js      # Predictions page
│   │   ├── App.js                  # Main React application
│   │   ├── App.css                 # Global styles
│   │   ├── index.js                # React entry point
│   │   └── index.css               # Additional global styles
│   ├── package.json                # Node.js dependencies
│   └── package-lock.json
├── data/
│   └── sample_data/                # Sample data files
├── requirements.txt                # Python dependencies
├── start_backend.py               # Backend startup script
├── start_frontend.bat             # Windows frontend startup
├── start_frontend.sh              # Linux/macOS frontend startup
├── initialize_data.py             # Database initialization
├── collect_comprehensive_data.py  # Main data collection script
└── README.md                      # Project overview
```

## Database Schema

### Electricity Prices Table
```sql
CREATE TABLE electricity_prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME NOT NULL,
    region VARCHAR(10) NOT NULL,        -- NSW1, VIC1, QLD1, SA1, TAS1
    price FLOAT NOT NULL,               -- Price in AUD/MWh
    demand FLOAT NOT NULL,              -- Demand in MW
    supply FLOAT NOT NULL,              -- Supply in MW
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_electricity_timestamp ON electricity_prices(timestamp);
CREATE INDEX idx_electricity_region ON electricity_prices(region);
```

### Dam Levels Table
```sql
CREATE TABLE dam_levels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME NOT NULL,
    dam_name VARCHAR(100) NOT NULL,     -- Name of the dam
    state VARCHAR(10) NOT NULL,         -- NSW, VIC, QLD, SA, TAS
    capacity_percentage FLOAT NOT NULL, -- Capacity as percentage
    volume_ml FLOAT NOT NULL,           -- Volume in megalitres
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_dam_timestamp ON dam_levels(timestamp);
CREATE INDEX idx_dam_name ON dam_levels(dam_name);
CREATE INDEX idx_dam_state ON dam_levels(state);
```

### Price Predictions Table (Future Enhancement)
```sql
CREATE TABLE price_predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME NOT NULL,
    region VARCHAR(10) NOT NULL,
    predicted_price FLOAT NOT NULL,
    confidence FLOAT NOT NULL,          -- Prediction confidence (0-1)
    model_version VARCHAR(50),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## API Documentation

### Base URL
```
http://localhost:8000/api
```

### Electricity Prices Endpoints

#### GET /electricity/prices
Get electricity prices with optional filtering and pagination.

**Query Parameters:**
- `start_date` (optional): Start date for data (ISO format)
- `end_date` (optional): End date for data (ISO format)
- `region` (optional): Filter by region (NSW1, VIC1, QLD1, SA1, TAS1)
- `page` (optional): Page number (default: 1)
- `size` (optional): Page size (default: 100, max: 1000)

**Response:**
```json
{
  "prices": [
    {
      "id": 1,
      "timestamp": "2025-09-11T12:00:00",
      "region": "NSW1",
      "price": 85.50,
      "demand": 8500.0,
      "supply": 9180.0,
      "created_at": "2025-09-11T12:00:00"
    }
  ],
  "total": 1000,
  "page": 1,
  "size": 100
}
```

#### GET /electricity/prices/current
Get the most recent electricity prices for all regions.

**Response:**
```json
{
  "timestamp": "2025-09-11T12:00:00",
  "prices": [
    {
      "id": 1,
      "timestamp": "2025-09-11T12:00:00",
      "region": "NSW1",
      "price": 85.50,
      "demand": 8500.0,
      "supply": 9180.0,
      "created_at": "2025-09-11T12:00:00"
    }
  ]
}
```

#### GET /electricity/prices/trends
Get price trends over a specified period.

**Query Parameters:**
- `days` (optional): Number of days to analyze (default: 30, max: 365)
- `region` (optional): Filter by region

**Response:**
```json
{
  "period": "30 days",
  "start_date": "2025-08-12T12:00:00",
  "end_date": "2025-09-11T12:00:00",
  "average_price": 89.25,
  "min_price": 45.00,
  "max_price": 150.75,
  "price_volatility": 12.34,
  "daily_averages": [
    {
      "date": "2025-09-11",
      "region": "NSW1",
      "price": 85.50
    }
  ]
}
```

### Dam Levels Endpoints

#### GET /dams/levels
Get dam levels with optional filtering and pagination.

**Query Parameters:**
- `start_date` (optional): Start date for data
- `end_date` (optional): End date for data
- `state` (optional): Filter by state (NSW, VIC, QLD, SA, TAS)
- `dam_name` (optional): Filter by dam name
- `page` (optional): Page number
- `size` (optional): Page size

**Response:**
```json
{
  "dam_levels": [
    {
      "id": 1,
      "timestamp": "2025-09-11T12:00:00",
      "dam_name": "Warragamba",
      "state": "NSW",
      "capacity_percentage": 85.95,
      "volume_ml": 1745642.94,
      "created_at": "2025-09-11T12:00:00"
    }
  ],
  "total": 50,
  "page": 1,
  "size": 100
}
```

#### GET /dams/levels/current
Get the most recent dam levels for all dams.

**Response:**
```json
{
  "timestamp": "2025-09-11T12:00:00",
  "dam_levels": [
    {
      "id": 1,
      "timestamp": "2025-09-11T12:00:00",
      "dam_name": "Warragamba",
      "state": "NSW",
      "capacity_percentage": 85.95,
      "volume_ml": 1745642.94,
      "created_at": "2025-09-11T12:00:00"
    }
  ]
}
```

### Data Collection Endpoints

#### POST /scraper/start
Start the data collection process.

**Response:**
```json
{
  "message": "Data collection started",
  "status": "running",
  "timestamp": "2025-09-11T12:00:00"
}
```

#### GET /scraper/status
Get the current status of the data collection process.

**Response:**
```json
{
  "is_running": false,
  "last_run": "2025-09-11T12:00:00",
  "last_error": null,
  "progress": "Data collection completed successfully!",
  "timestamp": "2025-09-11T12:00:00"
}
```

### System Endpoints

#### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-09-11T12:00:00"
}
```

#### GET /stats
Get basic statistics about the data.

**Response:**
```json
{
  "electricity_records": 23605,
  "dam_records": 42,
  "electricity_date_range": {
    "earliest": "2025-08-12T00:00:00",
    "latest": "2025-09-11T23:00:00"
  },
  "dam_date_range": {
    "earliest": "2025-09-11T12:00:00",
    "latest": "2025-09-11T12:00:00"
  }
}
```

## Data Collection System

### Overview
The data collection system uses a combination of web scraping and realistic data generation to populate the database with Australian electricity market and dam level data.

### Data Sources

#### Electricity Prices
- **Primary Source**: Realistic market-based data generation
- **Fallback**: AEMO (Australian Energy Market Operator) - requires API access
- **Alternative**: NEMOSIS library - for historical data access
- **Coverage**: All 5 NEM regions (NSW1, VIC1, QLD1, SA1, TAS1)

#### Dam Levels
- **Queensland**: Seqwater - Real data via web scraping
- **Other States**: Realistic data generation based on seasonal patterns
- **Coverage**: Major dams across all states

### Data Collection Process

#### 1. Current Data Collection
```python
# Main collection function
def scrape_all_data():
    data = {
        'electricity_prices': [],
        'dam_levels': []
    }
    
    # Collect electricity prices
    data['electricity_prices'] = generate_realistic_electricity_data()
    
    # Collect dam levels
    data['dam_levels'] = scrape_dam_levels()
    
    return data
```

#### 2. Historical Data Generation
- Generates 30 days of historical data
- Uses realistic market patterns and seasonal variations
- Includes price volatility and demand fluctuations

#### 3. Data Storage
- Stores data in SQLite database
- Handles duplicate prevention
- Maintains data integrity with foreign key constraints

### Web Scraping Implementation

#### Seqwater Dam Levels
```python
def scrape_seqwater_levels():
    """Scrape real dam level data from Seqwater"""
    try:
        url = "https://www.seqwater.com.au/water-supply/dam-levels"
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        # Parse dam level data from HTML
        # Return structured data
    except Exception as e:
        logger.error(f"Error scraping Seqwater: {e}")
        return []
```

#### Error Handling
- Comprehensive error logging
- Graceful fallback to realistic data generation
- Retry mechanisms for network failures
- Timeout handling for slow responses

## Frontend Components

### Component Architecture

#### 1. Navigation Component
- **File**: `frontend/src/components/Navigation.js`
- **Purpose**: Main navigation bar with routing
- **Features**: Active link highlighting, responsive design

#### 2. Price Chart Component
- **File**: `frontend/src/components/PriceChart.js`
- **Purpose**: Interactive electricity price visualization
- **Features**: Multi-region comparison, time series display

#### 3. Dam Level Chart Component
- **File**: `frontend/src/components/DamLevelChart.js`
- **Purpose**: Dam level visualization
- **Features**: Capacity percentage display, state grouping

#### 4. Metric Card Component
- **File**: `frontend/src/components/MetricCard.js`
- **Purpose**: Key metrics display
- **Features**: Color-coded values, responsive layout

#### 5. Scraper Control Component
- **File**: `frontend/src/components/ScraperControl.js`
- **Purpose**: Data collection control interface
- **Features**: Real-time status, progress tracking, error handling

### Page Components

#### 1. Dashboard Page
- **File**: `frontend/src/pages/Dashboard.js`
- **Purpose**: Main dashboard with overview metrics
- **Features**: Real-time data, interactive charts, quick stats

#### 2. Electricity Prices Page
- **File**: `frontend/src/pages/ElectricityPrices.js`
- **Purpose**: Detailed electricity price analysis
- **Features**: Historical trends, regional comparison

#### 3. Dam Levels Page
- **File**: `frontend/src/pages/DamLevels.js`
- **Purpose**: Dam level monitoring
- **Features**: State-wise grouping, capacity tracking

#### 4. Predictions Page
- **File**: `frontend/src/pages/Predictions.js`
- **Purpose**: Price prediction and trading insights
- **Features**: ML predictions, confidence levels, risk factors

### State Management
- **React Query**: Data fetching and caching
- **Local State**: Component-level state management
- **API Integration**: Axios for HTTP requests

### Styling
- **Bootstrap**: Responsive design framework
- **Custom CSS**: Additional styling for charts and components
- **Icons**: React Bootstrap Icons for UI elements

## Installation Guide

### Prerequisites
- Python 3.11 or higher
- Node.js 16 or higher
- npm or yarn package manager
- Git

### Backend Installation

#### 1. Clone Repository
```bash
git clone <repository-url>
cd auselectricity
```

#### 2. Create Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

#### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Initialize Database
```bash
python initialize_data.py
```

#### 5. Start Backend Server
```bash
python start_backend.py
```

### Frontend Installation

#### 1. Navigate to Frontend Directory
```bash
cd frontend
```

#### 2. Install Dependencies
```bash
npm install
```

#### 3. Start Development Server
```bash
# Windows
npm start
# Or use the batch file
start_frontend.bat

# Linux/macOS
npm start
# Or use the shell script
./start_frontend.sh
```

### Verification
- Backend: http://localhost:8000/docs (API documentation)
- Frontend: http://localhost:3000 (Dashboard)
- Health Check: http://localhost:8000/api/health

## Configuration

### Environment Variables
Create a `.env` file in the root directory:

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
LOG_FILE=logs/app.log
```

### Database Configuration
The system uses SQLite by default. To upgrade to PostgreSQL:

1. Install PostgreSQL dependencies:
```bash
pip install psycopg2-binary
```

2. Update database URL:
```python
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/auselectricity"
```

### API Configuration
Modify `backend/api/main.py` for CORS settings:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Deployment

### Development Deployment
The current setup is optimized for development with:
- SQLite database
- Local file storage
- Development servers

### Production Deployment

#### 1. Database Migration
- Upgrade to PostgreSQL or MySQL
- Set up database connection pooling
- Configure backup strategies

#### 2. Backend Deployment
- Use production ASGI server (Gunicorn with Uvicorn workers)
- Set up reverse proxy (Nginx)
- Configure SSL certificates
- Set up monitoring and logging

#### 3. Frontend Deployment
- Build production bundle: `npm run build`
- Serve static files with Nginx
- Configure CDN for assets

#### 4. Data Collection
- Set up cron jobs for scheduled data collection
- Implement queue system for background processing
- Set up monitoring for data collection failures

### Docker Deployment (Optional)
Create `Dockerfile` for containerized deployment:

```dockerfile
# Backend Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "start_backend.py"]
```

## Troubleshooting

### Common Issues

#### 1. Backend Not Starting
**Symptoms**: Port 8000 not accessible
**Solutions**:
- Check if port is already in use: `netstat -an | findstr :8000`
- Kill existing processes: `taskkill /F /IM python.exe`
- Restart backend: `python start_backend.py`

#### 2. Frontend Compilation Errors
**Symptoms**: Module not found errors
**Solutions**:
- Install missing packages: `npm install <package-name>`
- Clear npm cache: `npm cache clean --force`
- Delete node_modules and reinstall: `rm -rf node_modules && npm install`

#### 3. Database Connection Issues
**Symptoms**: SQLAlchemy errors
**Solutions**:
- Check database file permissions
- Recreate database: `rm sql_app.db && python initialize_data.py`
- Verify SQLite installation

#### 4. Data Collection Failures
**Symptoms**: Scraper status shows errors
**Solutions**:
- Check network connectivity
- Verify target websites are accessible
- Review error logs in scraper status
- Test individual scraper functions

#### 5. API CORS Errors
**Symptoms**: Frontend can't access API
**Solutions**:
- Check CORS configuration in `main.py`
- Verify API URL in frontend configuration
- Ensure both servers are running

### Logging and Debugging

#### Backend Logging
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

#### Frontend Debugging
- Use browser developer tools
- Check network tab for API calls
- Review console for JavaScript errors

#### Database Debugging
```python
# Enable SQLAlchemy logging
import logging
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
```

## Development Guidelines

### Code Style
- **Python**: Follow PEP 8 guidelines
- **JavaScript**: Use ESLint configuration
- **Comments**: Document complex logic and API endpoints
- **Naming**: Use descriptive variable and function names

### Git Workflow
1. Create feature branches for new development
2. Use descriptive commit messages
3. Test changes before merging
4. Keep main branch stable

### Testing
- **Backend**: Use pytest for API testing
- **Frontend**: Use Jest and React Testing Library
- **Integration**: Test API endpoints with real data

### Performance Optimization
- **Database**: Use indexes for frequently queried columns
- **API**: Implement pagination for large datasets
- **Frontend**: Use React Query for caching
- **Data Collection**: Implement rate limiting and retry logic

### Security Considerations
- **API**: Implement authentication for production
- **Data**: Validate all input data
- **CORS**: Configure appropriate origins
- **Dependencies**: Keep packages updated

### Monitoring and Maintenance
- **Logs**: Implement structured logging
- **Metrics**: Track API performance and data collection success
- **Alerts**: Set up notifications for system failures
- **Backups**: Regular database backups
- **Updates**: Keep dependencies updated

---

This documentation provides a comprehensive guide for understanding, installing, and maintaining the Australian Electricity Market Dashboard. For additional support or questions, refer to the project's issue tracker or contact the development team.
