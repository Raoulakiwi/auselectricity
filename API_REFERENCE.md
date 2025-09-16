# Australian Electricity Market Dashboard - API Reference

## Table of Contents
1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Base URL and Endpoints](#base-url-and-endpoints)
4. [Electricity Prices API](#electricity-prices-api)
5. [Dam Levels API](#dam-levels-api)
6. [Data Collection API](#data-collection-api)
7. [System API](#system-api)
8. [Error Handling](#error-handling)
9. [Rate Limiting](#rate-limiting)
10. [Examples](#examples)

## Overview

The Australian Electricity Market Dashboard API provides RESTful endpoints for accessing electricity price data, dam level information, and system controls. The API is built with FastAPI and provides automatic OpenAPI documentation.

### Key Features
- RESTful API design
- Automatic OpenAPI/Swagger documentation
- JSON request/response format
- Comprehensive error handling
- Real-time data access
- Historical data queries
- Data collection controls

## Authentication

Currently, the API does not require authentication for development purposes. For production deployment, implement authentication using:

- API Keys
- JWT Tokens
- OAuth 2.0
- Basic Authentication

## Base URL and Endpoints

### Base URL
```
http://localhost:8000/api
```

### API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Electricity Prices API

### GET /electricity/prices

Retrieve electricity prices with optional filtering and pagination.

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `start_date` | string | No | - | Start date in ISO format (YYYY-MM-DDTHH:MM:SS) |
| `end_date` | string | No | - | End date in ISO format (YYYY-MM-DDTHH:MM:SS) |
| `region` | string | No | - | Filter by region (NSW1, VIC1, QLD1, SA1, TAS1) |
| `page` | integer | No | 1 | Page number (minimum: 1) |
| `size` | integer | No | 100 | Page size (minimum: 1, maximum: 1000) |

#### Example Request
```bash
curl "http://localhost:8000/api/electricity/prices?region=NSW1&page=1&size=10"
```

#### Response
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
  "size": 10
}
```

### GET /electricity/prices/current

Get the most recent electricity prices for all regions.

#### Example Request
```bash
curl "http://localhost:8000/api/electricity/prices/current"
```

#### Response
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
    },
    {
      "id": 2,
      "timestamp": "2025-09-11T12:00:00",
      "region": "VIC1",
      "price": 78.25,
      "demand": 6500.0,
      "supply": 7020.0,
      "created_at": "2025-09-11T12:00:00"
    }
  ]
}
```

### GET /electricity/prices/trends

Get price trends and statistics over a specified period.

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `days` | integer | No | 30 | Number of days to analyze (minimum: 1, maximum: 365) |
| `region` | string | No | - | Filter by region |

#### Example Request
```bash
curl "http://localhost:8000/api/electricity/prices/trends?days=7&region=NSW1"
```

#### Response
```json
{
  "period": "7 days",
  "start_date": "2025-09-04T12:00:00",
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
    },
    {
      "date": "2025-09-10",
      "region": "NSW1",
      "price": 92.75
    }
  ]
}
```

### GET /electricity/prices/regions

Get list of available regions.

#### Example Request
```bash
curl "http://localhost:8000/api/electricity/prices/regions"
```

#### Response
```json
{
  "regions": ["NSW1", "VIC1", "QLD1", "SA1", "TAS1"]
}
```

### POST /electricity/prices

Create a new electricity price record.

#### Request Body
```json
{
  "timestamp": "2025-09-11T12:00:00",
  "region": "NSW1",
  "price": 85.50,
  "demand": 8500.0,
  "supply": 9180.0
}
```

#### Response
```json
{
  "id": 1,
  "timestamp": "2025-09-11T12:00:00",
  "region": "NSW1",
  "price": 85.50,
  "demand": 8500.0,
  "supply": 9180.0,
  "created_at": "2025-09-11T12:00:00"
}
```

## Dam Levels API

### GET /dams/levels

Retrieve dam levels with optional filtering and pagination.

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `start_date` | string | No | - | Start date in ISO format |
| `end_date` | string | No | - | End date in ISO format |
| `state` | string | No | - | Filter by state (NSW, VIC, QLD, SA, TAS) |
| `dam_name` | string | No | - | Filter by dam name |
| `page` | integer | No | 1 | Page number |
| `size` | integer | No | 100 | Page size |

#### Example Request
```bash
curl "http://localhost:8000/api/dams/levels?state=NSW&page=1&size=5"
```

#### Response
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
  "total": 10,
  "page": 1,
  "size": 5
}
```

### GET /dams/levels/current

Get the most recent dam levels for all dams.

#### Example Request
```bash
curl "http://localhost:8000/api/dams/levels/current"
```

#### Response
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

### GET /dams/levels/trends

Get dam level trends over a specified period.

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `days` | integer | No | 30 | Number of days to analyze |
| `state` | string | No | - | Filter by state |
| `dam_name` | string | No | - | Filter by dam name |

#### Example Request
```bash
curl "http://localhost:8000/api/dams/levels/trends?days=14&state=NSW"
```

#### Response
```json
{
  "period": "14 days",
  "start_date": "2025-08-28T12:00:00",
  "end_date": "2025-09-11T12:00:00",
  "average_capacity": 78.5,
  "min_capacity": 65.2,
  "max_capacity": 89.1,
  "capacity_volatility": 5.8,
  "daily_averages": [
    {
      "date": "2025-09-11",
      "dam_name": "Warragamba",
      "capacity_percentage": 85.95
    }
  ]
}
```

### GET /dams/levels/states

Get list of available states.

#### Example Request
```bash
curl "http://localhost:8000/api/dams/levels/states"
```

#### Response
```json
{
  "states": ["NSW", "VIC", "QLD", "SA", "TAS"]
}
```

### GET /dams/levels/dams

Get list of available dams.

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `state` | string | No | - | Filter by state |

#### Example Request
```bash
curl "http://localhost:8000/api/dams/levels/dams?state=NSW"
```

#### Response
```json
{
  "dams": [
    {
      "name": "Warragamba",
      "state": "NSW"
    },
    {
      "name": "Burrinjuck",
      "state": "NSW"
    }
  ]
}
```

### POST /dams/levels

Create a new dam level record.

#### Request Body
```json
{
  "timestamp": "2025-09-11T12:00:00",
  "dam_name": "Warragamba",
  "state": "NSW",
  "capacity_percentage": 85.95,
  "volume_ml": 1745642.94
}
```

#### Response
```json
{
  "id": 1,
  "timestamp": "2025-09-11T12:00:00",
  "dam_name": "Warragamba",
  "state": "NSW",
  "capacity_percentage": 85.95,
  "volume_ml": 1745642.94,
  "created_at": "2025-09-11T12:00:00"
}
```

## Data Collection API

### POST /scraper/start

Start the data collection process.

#### Example Request
```bash
curl -X POST "http://localhost:8000/api/scraper/start"
```

#### Response
```json
{
  "message": "Data collection started",
  "status": "running",
  "timestamp": "2025-09-11T12:00:00"
}
```

#### Error Response (if already running)
```json
{
  "detail": "Data collection is already running. Please wait for it to complete."
}
```

### GET /scraper/status

Get the current status of the data collection process.

#### Example Request
```bash
curl "http://localhost:8000/api/scraper/status"
```

#### Response (when running)
```json
{
  "is_running": true,
  "last_run": null,
  "last_error": null,
  "progress": "Collecting current data...",
  "timestamp": "2025-09-11T12:00:00"
}
```

#### Response (when completed)
```json
{
  "is_running": false,
  "last_run": "2025-09-11T12:00:00",
  "last_error": null,
  "progress": "Data collection completed successfully!",
  "timestamp": "2025-09-11T12:00:00"
}
```

#### Response (when error occurred)
```json
{
  "is_running": false,
  "last_run": null,
  "last_error": "Connection timeout to data source",
  "progress": "Data collection failed: Connection timeout",
  "timestamp": "2025-09-11T12:00:00"
}
```

### GET /scraper/health

Health check for the scraper service.

#### Example Request
```bash
curl "http://localhost:8000/api/scraper/health"
```

#### Response
```json
{
  "status": "healthy",
  "timestamp": "2025-09-11T12:00:00"
}
```

## System API

### GET /health

General health check endpoint.

#### Example Request
```bash
curl "http://localhost:8000/api/health"
```

#### Response
```json
{
  "status": "healthy",
  "timestamp": "2025-09-11T12:00:00"
}
```

### GET /stats

Get basic statistics about the data in the system.

#### Example Request
```bash
curl "http://localhost:8000/api/stats"
```

#### Response
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

## Error Handling

### HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 400 | Bad Request - Invalid request parameters |
| 404 | Not Found - Resource not found |
| 422 | Unprocessable Entity - Validation error |
| 500 | Internal Server Error - Server error |

### Error Response Format

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Error Examples

#### Validation Error (422)
```json
{
  "detail": [
    {
      "loc": ["body", "price"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

#### Not Found Error (404)
```json
{
  "detail": "Resource not found"
}
```

#### Server Error (500)
```json
{
  "detail": "Internal server error occurred"
}
```

## Rate Limiting

Currently, the API does not implement rate limiting. For production deployment, consider implementing:

- Request rate limiting per IP
- API key-based rate limiting
- Endpoint-specific rate limits

Example implementation with FastAPI:
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/api/electricity/prices")
@limiter.limit("100/minute")
async def get_electricity_prices(request: Request, ...):
    # endpoint implementation
```

## Examples

### JavaScript/Node.js

#### Fetch Current Electricity Prices
```javascript
const fetchCurrentPrices = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/electricity/prices/current');
    const data = await response.json();
    console.log('Current prices:', data);
    return data;
  } catch (error) {
    console.error('Error fetching prices:', error);
  }
};
```

#### Start Data Collection
```javascript
const startDataCollection = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/scraper/start', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    const data = await response.json();
    console.log('Data collection started:', data);
    return data;
  } catch (error) {
    console.error('Error starting data collection:', error);
  }
};
```

### Python

#### Using Requests Library
```python
import requests
import json

# Get current electricity prices
def get_current_prices():
    response = requests.get('http://localhost:8000/api/electricity/prices/current')
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

# Get dam levels for a specific state
def get_dam_levels(state='NSW'):
    params = {'state': state, 'size': 10}
    response = requests.get('http://localhost:8000/api/dams/levels', params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

# Start data collection
def start_data_collection():
    response = requests.post('http://localhost:8000/api/scraper/start')
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None
```

#### Using httpx (Async)
```python
import httpx
import asyncio

async def get_price_trends(days=30):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f'http://localhost:8000/api/electricity/prices/trends',
            params={'days': days}
        )
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return None

# Usage
trends = asyncio.run(get_price_trends(7))
```

### cURL Examples

#### Get Electricity Prices with Filters
```bash
curl -X GET "http://localhost:8000/api/electricity/prices" \
  -H "Content-Type: application/json" \
  -G \
  -d "region=NSW1" \
  -d "start_date=2025-09-10T00:00:00" \
  -d "end_date=2025-09-11T23:59:59" \
  -d "page=1" \
  -d "size=50"
```

#### Create New Electricity Price Record
```bash
curl -X POST "http://localhost:8000/api/electricity/prices" \
  -H "Content-Type: application/json" \
  -d '{
    "timestamp": "2025-09-11T12:00:00",
    "region": "NSW1",
    "price": 85.50,
    "demand": 8500.0,
    "supply": 9180.0
  }'
```

#### Monitor Data Collection Status
```bash
# Start collection
curl -X POST "http://localhost:8000/api/scraper/start"

# Check status
curl "http://localhost:8000/api/scraper/status"

# Check health
curl "http://localhost:8000/api/scraper/health"
```

### React/JavaScript Frontend Integration

#### Custom Hook for API Calls
```javascript
import { useState, useEffect } from 'react';

const useApiData = (endpoint) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await fetch(`http://localhost:8000/api${endpoint}`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const result = await response.json();
        setData(result);
        setError(null);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [endpoint]);

  return { data, loading, error };
};

// Usage in component
const Dashboard = () => {
  const { data: prices, loading, error } = useApiData('/electricity/prices/current');
  
  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  
  return (
    <div>
      {prices?.prices?.map(price => (
        <div key={price.id}>
          {price.region}: ${price.price}/MWh
        </div>
      ))}
    </div>
  );
};
```

---

This API reference provides comprehensive documentation for all available endpoints, request/response formats, error handling, and usage examples. The API is designed to be intuitive and follows RESTful principles for easy integration with any client application.
