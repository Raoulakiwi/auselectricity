# Australian Electricity Market Dashboard - Developer Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [Development Environment Setup](#development-environment-setup)
3. [Project Structure Deep Dive](#project-structure-deep-dive)
4. [Backend Development](#backend-development)
5. [Frontend Development](#frontend-development)
6. [Database Development](#database-development)
7. [Data Collection Development](#data-collection-development)
8. [Testing](#testing)
9. [Code Style and Standards](#code-style-and-standards)
10. [Debugging and Troubleshooting](#debugging-and-troubleshooting)
11. [Contributing Guidelines](#contributing-guidelines)
12. [Performance Optimization](#performance-optimization)

## Getting Started

### Prerequisites for Development
- Python 3.11+ with pip
- Node.js 16+ with npm
- Git
- Code editor (VS Code recommended)
- Database client (optional, for direct DB access)

### Quick Development Setup
```bash
# Clone and setup
git clone <repository-url>
cd auselectricity

# Backend setup
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Frontend setup
cd frontend
npm install
cd ..

# Initialize database
python initialize_data.py

# Start development servers
python start_backend.py  # Terminal 1
cd frontend && npm start  # Terminal 2
```

## Development Environment Setup

### VS Code Configuration

#### Recommended Extensions
```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.pylint",
    "ms-python.black-formatter",
    "bradlc.vscode-tailwindcss",
    "esbenp.prettier-vscode",
    "ms-vscode.vscode-json",
    "ms-vscode.vscode-typescript-next"
  ]
}
```

#### Workspace Settings
Create `.vscode/settings.json`:
```json
{
  "python.defaultInterpreterPath": "./venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "python.formatting.blackArgs": ["--line-length", "88"],
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  },
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true,
    "**/node_modules": true,
    "**/.git": true
  }
}
```

#### Launch Configuration
Create `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/start_backend.py",
      "console": "integratedTerminal",
      "cwd": "${workspaceFolder}"
    },
    {
      "name": "Python: Data Collection",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/collect_comprehensive_data.py",
      "console": "integratedTerminal",
      "cwd": "${workspaceFolder}"
    }
  ]
}
```

### Environment Variables
Create `.env.development`:
```env
# Development Environment Variables
DEBUG=true
LOG_LEVEL=DEBUG
DATABASE_URL=sqlite:///./sql_app.db
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true
REACT_APP_API_URL=http://localhost:8000
REACT_APP_DEBUG=true
```

### Git Configuration
Create `.gitignore`:
```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environment
venv/
env/
ENV/

# Database
*.db
*.sqlite
*.sqlite3

# Environment Variables
.env
.env.local
.env.development
.env.production

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# React
build/
.DS_Store
.env.local
.env.development.local
.env.test.local
.env.production.local

# Logs
logs/
*.log

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

## Project Structure Deep Dive

### Backend Architecture

#### API Layer (`backend/api/`)
```
api/
├── main.py              # FastAPI app initialization
└── routes/
    ├── electricity.py   # Electricity price endpoints
    ├── dams.py         # Dam level endpoints
    └── scraper.py      # Data collection endpoints
```

#### Data Layer (`backend/data/`)
```
data/
├── models/              # Pydantic models for API
│   ├── electricity.py   # Electricity price models
│   └── dams.py         # Dam level models
└── collectors/          # Data collection logic
    ├── aemo_collector.py
    ├── dam_collector.py
    └── robust_data_scrapers.py
```

#### Database Layer (`backend/database/`)
```
database/
├── __init__.py
└── database.py         # SQLAlchemy configuration
```

### Frontend Architecture

#### Component Structure
```
src/
├── components/          # Reusable UI components
│   ├── Navigation.js    # Main navigation
│   ├── PriceChart.js    # Electricity price charts
│   ├── DamLevelChart.js # Dam level charts
│   ├── MetricCard.js    # Metric display cards
│   └── ScraperControl.js # Data collection control
├── pages/              # Page components
│   ├── Dashboard.js     # Main dashboard
│   ├── ElectricityPrices.js
│   ├── DamLevels.js
│   └── Predictions.js
├── App.js              # Main app component
└── index.js            # React entry point
```

## Backend Development

### FastAPI Application Structure

#### Main Application (`backend/api/main.py`)
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes import electricity, dams, scraper

app = FastAPI(
    title="Australian Electricity Market Dashboard API",
    description="API for monitoring Australian wholesale electricity prices and dam levels",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(electricity.router, prefix="/api/electricity", tags=["electricity"])
app.include_router(dams.router, prefix="/api/dams", tags=["dams"])
app.include_router(scraper.router, prefix="/api/scraper", tags=["scraper"])
```

### Creating New API Endpoints

#### 1. Define Pydantic Models
```python
# backend/data/models/new_feature.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List

class NewFeatureResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    value: float
    created_at: datetime

class NewFeatureCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    name: str
    value: float
```

#### 2. Create API Router
```python
# backend/api/routes/new_feature.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.database import get_db
from backend.data.models.new_feature import NewFeatureResponse, NewFeatureCreate

router = APIRouter()

@router.get("/", response_model=List[NewFeatureResponse])
async def get_new_features(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all new features with pagination"""
    features = db.query(NewFeature).offset(skip).limit(limit).all()
    return features

@router.post("/", response_model=NewFeatureResponse)
async def create_new_feature(
    feature: NewFeatureCreate,
    db: Session = Depends(get_db)
):
    """Create a new feature"""
    db_feature = NewFeature(**feature.model_dump())
    db.add(db_feature)
    db.commit()
    db.refresh(db_feature)
    return db_feature
```

#### 3. Register Router
```python
# backend/api/main.py
from backend.api.routes import new_feature

app.include_router(new_feature.router, prefix="/api/new-feature", tags=["new-feature"])
```

### Database Development

#### Creating New Database Models
```python
# backend/database/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from backend.database.database import Base

class NewFeature(Base):
    __tablename__ = "new_features"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    value = Column(Float)
    created_at = Column(DateTime, server_default=func.now())
```

#### Database Migrations
```python
# Create migration script
def create_new_feature_table():
    from backend.database.database import engine
    from backend.database.models import NewFeature
    
    NewFeature.__table__.create(engine, checkfirst=True)
    print("New feature table created successfully")

if __name__ == "__main__":
    create_new_feature_table()
```

### Error Handling

#### Custom Exception Classes
```python
# backend/api/exceptions.py
class DataCollectionError(Exception):
    """Raised when data collection fails"""
    pass

class ValidationError(Exception):
    """Raised when data validation fails"""
    pass

# Usage in routes
@router.post("/scraper/start")
async def start_data_collection():
    try:
        # Data collection logic
        pass
    except DataCollectionError as e:
        raise HTTPException(status_code=500, detail=str(e))
```

#### Global Exception Handler
```python
# backend/api/main.py
from fastapi import HTTPException
from fastapi.responses import JSONResponse

@app.exception_handler(DataCollectionError)
async def data_collection_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Data collection failed: {str(exc)}"}
    )
```

## Frontend Development

### React Component Development

#### Component Template
```javascript
import React, { useState, useEffect } from 'react';
import { Card, Button, Alert } from 'react-bootstrap';

const NewComponent = ({ prop1, prop2 }) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await fetch('/api/endpoint');
        if (!response.ok) {
          throw new Error('Failed to fetch data');
        }
        const result = await response.json();
        setData(result);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <Alert variant="danger">{error}</Alert>;

  return (
    <Card>
      <Card.Header>New Component</Card.Header>
      <Card.Body>
        {/* Component content */}
      </Card.Body>
    </Card>
  );
};

export default NewComponent;
```

### Custom Hooks

#### API Data Hook
```javascript
// src/hooks/useApiData.js
import { useState, useEffect } from 'react';

const useApiData = (endpoint, options = {}) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await fetch(endpoint, options);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const result = await response.json();
      setData(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [endpoint]);

  return { data, loading, error, refetch: fetchData };
};

export default useApiData;
```

#### Usage Example
```javascript
import useApiData from '../hooks/useApiData';

const Dashboard = () => {
  const { data: prices, loading, error, refetch } = useApiData('/api/electricity/prices/current');

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <button onClick={refetch}>Refresh</button>
      {prices?.prices?.map(price => (
        <div key={price.id}>{price.region}: ${price.price}</div>
      ))}
    </div>
  );
};
```

### State Management

#### Context API for Global State
```javascript
// src/context/AppContext.js
import React, { createContext, useContext, useReducer } from 'react';

const AppContext = createContext();

const initialState = {
  user: null,
  theme: 'light',
  notifications: []
};

const appReducer = (state, action) => {
  switch (action.type) {
    case 'SET_USER':
      return { ...state, user: action.payload };
    case 'SET_THEME':
      return { ...state, theme: action.payload };
    case 'ADD_NOTIFICATION':
      return { ...state, notifications: [...state.notifications, action.payload] };
    default:
      return state;
  }
};

export const AppProvider = ({ children }) => {
  const [state, dispatch] = useReducer(appReducer, initialState);

  return (
    <AppContext.Provider value={{ state, dispatch }}>
      {children}
    </AppContext.Provider>
  );
};

export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within AppProvider');
  }
  return context;
};
```

## Data Collection Development

### Adding New Data Sources

#### 1. Create Data Collector
```python
# backend/data/collectors/new_source_collector.py
import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class NewSourceCollector:
    def __init__(self):
        self.base_url = "https://example.com"
        self.timeout = 30

    def collect_data(self):
        """Collect data from new source"""
        try:
            data = []
            
            # Implement data collection logic
            response = requests.get(f"{self.base_url}/api/data", timeout=self.timeout)
            response.raise_for_status()
            
            raw_data = response.json()
            
            # Process and structure data
            for item in raw_data:
                processed_item = {
                    'timestamp': datetime.now(),
                    'source': 'new_source',
                    'value': item['value'],
                    'metadata': item.get('metadata', {})
                }
                data.append(processed_item)
            
            logger.info(f"Collected {len(data)} records from new source")
            return data
            
        except Exception as e:
            logger.error(f"Error collecting data from new source: {e}")
            return []

    def validate_data(self, data):
        """Validate collected data"""
        if not data:
            return False
        
        required_fields = ['timestamp', 'source', 'value']
        for item in data:
            if not all(field in item for field in required_fields):
                return False
        
        return True
```

#### 2. Integrate with Main Collector
```python
# backend/data/collectors/robust_data_scrapers.py
from .new_source_collector import NewSourceCollector

class RobustDataScrapers:
    def __init__(self):
        self.new_source_collector = NewSourceCollector()
        # ... other collectors

    def scrape_all_data(self):
        data = {
            'electricity_prices': [],
            'dam_levels': [],
            'new_data': []  # Add new data type
        }
        
        # Collect new data
        new_data = self.new_source_collector.collect_data()
        if self.new_source_collector.validate_data(new_data):
            data['new_data'] = new_data
        
        return data
```

### Data Validation and Processing

#### Data Validation Schema
```python
# backend/data/validators.py
from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional

class ElectricityPriceValidator(BaseModel):
    timestamp: datetime
    region: str
    price: float
    demand: float
    supply: float

    @validator('region')
    def validate_region(cls, v):
        valid_regions = ['NSW1', 'VIC1', 'QLD1', 'SA1', 'TAS1']
        if v not in valid_regions:
            raise ValueError(f'Invalid region: {v}')
        return v

    @validator('price')
    def validate_price(cls, v):
        if v < 0 or v > 10000:
            raise ValueError(f'Price out of range: {v}')
        return v

    @validator('demand', 'supply')
    def validate_demand_supply(cls, v):
        if v < 0:
            raise ValueError(f'Demand/Supply cannot be negative: {v}')
        return v
```

#### Data Processing Pipeline
```python
# backend/data/processors.py
import pandas as pd
from typing import List, Dict, Any

class DataProcessor:
    def __init__(self):
        self.processors = {
            'electricity_prices': self.process_electricity_prices,
            'dam_levels': self.process_dam_levels
        }

    def process_electricity_prices(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process electricity price data"""
        if not data:
            return []
        
        df = pd.DataFrame(data)
        
        # Remove duplicates
        df = df.drop_duplicates(subset=['timestamp', 'region'])
        
        # Handle missing values
        df['price'] = df['price'].fillna(df['price'].median())
        
        # Add calculated fields
        df['price_per_mw'] = df['price'] / df['demand']
        df['supply_demand_ratio'] = df['supply'] / df['demand']
        
        return df.to_dict('records')

    def process_dam_levels(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process dam level data"""
        if not data:
            return []
        
        df = pd.DataFrame(data)
        
        # Remove duplicates
        df = df.drop_duplicates(subset=['timestamp', 'dam_name'])
        
        # Handle missing values
        df['capacity_percentage'] = df['capacity_percentage'].fillna(0)
        df['volume_ml'] = df['volume_ml'].fillna(0)
        
        # Add calculated fields
        df['volume_change'] = df.groupby('dam_name')['volume_ml'].diff()
        
        return df.to_dict('records')
```

## Testing

### Backend Testing

#### Unit Tests
```python
# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from backend.api.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_electricity_prices_endpoint():
    response = client.get("/api/electricity/prices/current")
    assert response.status_code == 200
    data = response.json()
    assert "prices" in data
    assert "timestamp" in data

def test_scraper_start():
    response = client.post("/api/scraper/start")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["status"] == "running"
```

#### Integration Tests
```python
# tests/test_integration.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database.database import get_db, Base
from backend.database.models import ElectricityPrice

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_database_connection(test_db):
    db = TestingSessionLocal()
    price = ElectricityPrice(
        timestamp="2025-09-11T12:00:00",
        region="NSW1",
        price=85.50,
        demand=8500.0,
        supply=9180.0
    )
    db.add(price)
    db.commit()
    db.refresh(price)
    
    assert price.id is not None
    assert price.region == "NSW1"
    
    db.close()
```

#### Data Collection Tests
```python
# tests/test_data_collection.py
import pytest
from backend.data.collectors.robust_data_scrapers import RobustDataScrapers

def test_data_collection():
    scraper = RobustDataScrapers()
    data = scraper.scrape_all_data()
    
    assert isinstance(data, dict)
    assert 'electricity_prices' in data
    assert 'dam_levels' in data
    assert isinstance(data['electricity_prices'], list)
    assert isinstance(data['dam_levels'], list)

def test_electricity_data_generation():
    scraper = RobustDataScrapers()
    data = scraper.generate_realistic_electricity_data()
    
    assert len(data) > 0
    for item in data:
        assert 'timestamp' in item
        assert 'region' in item
        assert 'price' in item
        assert item['region'] in ['NSW1', 'VIC1', 'QLD1', 'SA1', 'TAS1']
```

### Frontend Testing

#### Component Tests
```javascript
// src/components/__tests__/MetricCard.test.js
import React from 'react';
import { render, screen } from '@testing-library/react';
import MetricCard from '../MetricCard';

describe('MetricCard', () => {
  test('renders metric card with title and value', () => {
    render(
      <MetricCard
        title="Test Metric"
        value="100"
        unit="MW"
        color="primary"
      />
    );
    
    expect(screen.getByText('Test Metric')).toBeInTheDocument();
    expect(screen.getByText('100')).toBeInTheDocument();
    expect(screen.getByText('MW')).toBeInTheDocument();
  });

  test('applies correct color class', () => {
    render(
      <MetricCard
        title="Test"
        value="100"
        color="danger"
      />
    );
    
    const card = screen.getByText('Test').closest('.card');
    expect(card).toHaveClass('border-danger');
  });
});
```

#### API Integration Tests
```javascript
// src/__tests__/api.test.js
import { render, screen, waitFor } from '@testing-library/react';
import Dashboard from '../pages/Dashboard';

// Mock fetch
global.fetch = jest.fn();

describe('Dashboard API Integration', () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  test('loads and displays electricity prices', async () => {
    const mockPrices = {
      timestamp: '2025-09-11T12:00:00',
      prices: [
        { id: 1, region: 'NSW1', price: 85.50 }
      ]
    };

    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockPrices,
    });

    render(<Dashboard />);

    await waitFor(() => {
      expect(screen.getByText('NSW1')).toBeInTheDocument();
      expect(screen.getByText('$85.50')).toBeInTheDocument();
    });
  });
});
```

### Running Tests

#### Backend Tests
```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run all tests
pytest

# Run specific test file
pytest tests/test_api.py

# Run with coverage
pytest --cov=backend tests/
```

#### Frontend Tests
```bash
# Install test dependencies
npm install --save-dev @testing-library/react @testing-library/jest-dom

# Run tests
npm test

# Run tests with coverage
npm test -- --coverage
```

## Code Style and Standards

### Python Code Style

#### Black Configuration
Create `pyproject.toml`:
```toml
[tool.black]
line-length = 88
target-version = ['py311']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | build
  | dist
)/
'''
```

#### Pylint Configuration
Create `.pylintrc`:
```ini
[MASTER]
load-plugins=pylint_django

[MESSAGES CONTROL]
disable=missing-docstring,too-few-public-methods

[FORMAT]
max-line-length=88

[DESIGN]
max-args=10
max-locals=20
max-returns=6
max-branches=15
```

#### Import Organization
```python
# Standard library imports
import os
import sys
from datetime import datetime
from typing import List, Dict, Optional

# Third-party imports
import pandas as pd
import requests
from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session

# Local imports
from backend.database.database import get_db
from backend.data.models.electricity import ElectricityPriceResponse
```

### JavaScript Code Style

#### ESLint Configuration
Create `.eslintrc.js`:
```javascript
module.exports = {
  env: {
    browser: true,
    es2021: true,
    node: true,
  },
  extends: [
    'eslint:recommended',
    'plugin:react/recommended',
    'plugin:react-hooks/recommended',
  ],
  parserOptions: {
    ecmaFeatures: {
      jsx: true,
    },
    ecmaVersion: 12,
    sourceType: 'module',
  },
  plugins: ['react', 'react-hooks'],
  rules: {
    'react/prop-types': 'off',
    'react/react-in-jsx-scope': 'off',
    'no-unused-vars': 'warn',
    'no-console': 'warn',
  },
  settings: {
    react: {
      version: 'detect',
    },
  },
};
```

#### Prettier Configuration
Create `.prettierrc`:
```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 80,
  "tabWidth": 2,
  "useTabs": false
}
```

### Git Hooks

#### Pre-commit Hook
Create `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 22.3.0
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/pycqa/pylint
    rev: v2.15.0
    hooks:
      - id: pylint

  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v8.20.0
    hooks:
      - id: eslint
        files: \.js$
        types: [file]
```

Install pre-commit:
```bash
pip install pre-commit
pre-commit install
```

## Debugging and Troubleshooting

### Backend Debugging

#### Logging Configuration
```python
# backend/utils/logging.py
import logging
import sys
from datetime import datetime

def setup_logging(level=logging.INFO):
    """Setup application logging"""
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # File handler
    file_handler = logging.FileHandler('logs/app.log')
    file_handler.setFormatter(formatter)
    
    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    
    # Specific loggers
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    logging.getLogger('uvicorn').setLevel(logging.INFO)
```

#### Debug Mode
```python
# backend/api/main.py
import logging
from backend.utils.logging import setup_logging

# Enable debug logging
setup_logging(logging.DEBUG)

# Add debug endpoints
@app.get("/debug/database")
async def debug_database(db: Session = Depends(get_db)):
    """Debug database connection and data"""
    try:
        # Test database connection
        result = db.execute("SELECT 1").fetchone()
        
        # Get table counts
        electricity_count = db.query(ElectricityPrice).count()
        dam_count = db.query(DamLevel).count()
        
        return {
            "database_connected": True,
            "electricity_records": electricity_count,
            "dam_records": dam_count,
            "test_query": result[0] if result else None
        }
    except Exception as e:
        logging.error(f"Database debug error: {e}")
        return {"database_connected": False, "error": str(e)}
```

### Frontend Debugging

#### React Developer Tools
```javascript
// Add to package.json
{
  "scripts": {
    "start": "REACT_APP_DEBUG=true react-scripts start"
  }
}

// Debug component
const DebugComponent = ({ data }) => {
  if (process.env.REACT_APP_DEBUG === 'true') {
    console.log('Debug data:', data);
  }
  
  return <div>{/* Component content */}</div>;
};
```

#### Error Boundaries
```javascript
// src/components/ErrorBoundary.js
import React from 'react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="alert alert-danger">
          <h2>Something went wrong.</h2>
          <details>
            <summary>Error details</summary>
            <pre>{this.state.error?.toString()}</pre>
          </details>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
```

### Performance Debugging

#### Backend Performance
```python
# backend/utils/performance.py
import time
import functools
import logging

logger = logging.getLogger(__name__)

def performance_monitor(func):
    """Decorator to monitor function performance"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        execution_time = end_time - start_time
        logger.info(f"{func.__name__} executed in {execution_time:.4f} seconds")
        
        return result
    return wrapper

# Usage
@performance_monitor
def expensive_operation():
    # Some expensive operation
    pass
```

#### Frontend Performance
```javascript
// src/utils/performance.js
export const measurePerformance = (name, fn) => {
  const start = performance.now();
  const result = fn();
  const end = performance.now();
  
  console.log(`${name} took ${end - start} milliseconds`);
  return result;
};

// Usage
const expensiveCalculation = () => {
  return measurePerformance('Expensive Calculation', () => {
    // Some expensive calculation
    return result;
  });
};
```

## Contributing Guidelines

### Development Workflow

#### 1. Feature Development
```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes
# Add tests
# Update documentation

# Commit changes
git add .
git commit -m "feat: add new feature"

# Push branch
git push origin feature/new-feature

# Create pull request
```

#### 2. Bug Fixes
```bash
# Create bugfix branch
git checkout -b bugfix/fix-issue-123

# Fix the issue
# Add tests to prevent regression
# Update documentation if needed

# Commit changes
git add .
git commit -m "fix: resolve issue #123"

# Push branch
git push origin bugfix/fix-issue-123
```

### Code Review Process

#### Pull Request Template
Create `.github/pull_request_template.md`:
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

#### Review Checklist
- [ ] Code follows project style guidelines
- [ ] Tests are included and pass
- [ ] Documentation is updated
- [ ] No security vulnerabilities
- [ ] Performance impact considered
- [ ] Error handling is appropriate

### Documentation Standards

#### Code Documentation
```python
def calculate_price_trend(prices: List[float], days: int) -> Dict[str, float]:
    """
    Calculate price trend statistics for a given period.
    
    Args:
        prices: List of price values
        days: Number of days to analyze
        
    Returns:
        Dictionary containing trend statistics
        
    Raises:
        ValueError: If prices list is empty or days is invalid
        
    Example:
        >>> prices = [85.5, 87.2, 89.1, 86.8]
        >>> trend = calculate_price_trend(prices, 4)
        >>> print(trend['average'])
        87.15
    """
    if not prices:
        raise ValueError("Prices list cannot be empty")
    
    if days <= 0:
        raise ValueError("Days must be positive")
    
    # Implementation here
    pass
```

#### API Documentation
```python
@router.get("/electricity/prices/trends")
async def get_price_trends(
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze"),
    region: Optional[str] = Query(None, description="Filter by region")
):
    """
    Get electricity price trends and statistics.
    
    This endpoint provides comprehensive price trend analysis including:
    - Average, minimum, and maximum prices
    - Price volatility calculations
    - Daily average breakdowns
    
    **Parameters:**
    - **days**: Number of days to analyze (1-365)
    - **region**: Optional region filter (NSW1, VIC1, QLD1, SA1, TAS1)
    
    **Returns:**
    - Trend statistics and daily averages
    
    **Example:**
    ```bash
    curl "http://localhost:8000/api/electricity/prices/trends?days=7&region=NSW1"
    ```
    """
    # Implementation here
    pass
```

## Performance Optimization

### Backend Optimization

#### Database Optimization
```python
# Use database indexes
class ElectricityPrice(Base):
    __tablename__ = "electricity_prices"
    
    # Add indexes for frequently queried columns
    timestamp = Column(DateTime, index=True)
    region = Column(String, index=True)
    price = Column(Float, index=True)

# Use query optimization
def get_recent_prices(db: Session, limit: int = 100):
    """Optimized query for recent prices"""
    return db.query(ElectricityPrice)\
        .order_by(ElectricityPrice.timestamp.desc())\
        .limit(limit)\
        .all()

# Use connection pooling
from sqlalchemy.pool import QueuePool

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)
```

#### Caching
```python
# backend/utils/cache.py
from functools import lru_cache
import redis
import json

# In-memory caching
@lru_cache(maxsize=128)
def get_region_list():
    """Cache region list"""
    return ['NSW1', 'VIC1', 'QLD1', 'SA1', 'TAS1']

# Redis caching
redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cache_data(key: str, data: dict, ttl: int = 300):
    """Cache data in Redis"""
    redis_client.setex(key, ttl, json.dumps(data))

def get_cached_data(key: str):
    """Get cached data from Redis"""
    cached = redis_client.get(key)
    if cached:
        return json.loads(cached)
    return None
```

### Frontend Optimization

#### Component Optimization
```javascript
// Use React.memo for expensive components
const ExpensiveComponent = React.memo(({ data }) => {
  // Component logic
  return <div>{/* Expensive rendering */}</div>;
});

// Use useMemo for expensive calculations
const Dashboard = ({ prices }) => {
  const processedData = useMemo(() => {
    return prices.map(price => ({
      ...price,
      formattedPrice: `$${price.price.toFixed(2)}`
    }));
  }, [prices]);

  return <div>{/* Render processed data */}</div>;
};

// Use useCallback for event handlers
const Dashboard = () => {
  const handleRefresh = useCallback(() => {
    // Refresh logic
  }, []);

  return <button onClick={handleRefresh}>Refresh</button>;
};
```

#### Bundle Optimization
```javascript
// Lazy load components
const LazyComponent = React.lazy(() => import('./LazyComponent'));

const App = () => {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <LazyComponent />
    </Suspense>
  );
};

// Code splitting
const Dashboard = React.lazy(() => import('./pages/Dashboard'));
const ElectricityPrices = React.lazy(() => import('./pages/ElectricityPrices'));
```

---

This developer guide provides comprehensive information for contributing to the Australian Electricity Market Dashboard project. Follow these guidelines to ensure code quality, maintainability, and consistency across the codebase.
