# Australian Electricity Market Dashboard - Setup Guide

## Overview

This dashboard monitors Australian wholesale electricity market prices and dam levels to help predict price fluctuations for profitable trading opportunities.

## Features

- **Real-time Electricity Price Monitoring**: Track wholesale electricity prices from AEMO
- **Dam Level Tracking**: Monitor water storage levels across major Australian dams
- **Historical Data Analysis**: View 12+ months of historical data with interactive charts
- **Price Prediction**: Machine learning models to predict price fluctuations
- **Interactive Dashboard**: Modern web interface with real-time updates

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

## Installation

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd auselectricity
```

### 2. Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Initialize the database with sample data
python initialize_data.py

# Start the backend server
python start_backend.py
```

The backend API will be available at:
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

### 3. Frontend Setup

Open a new terminal and run:

```bash
# Install Node.js dependencies
cd frontend
npm install

# Start the React development server
npm start
```

The dashboard will be available at: **http://localhost:3000**

## Usage

### Dashboard Overview

1. **Main Dashboard**: Overview of current prices and dam levels
2. **Electricity Prices**: Detailed price analysis with historical trends
3. **Dam Levels**: Water storage monitoring across all states
4. **Predictions**: AI-powered price predictions for trading insights

### Key Features

#### Real-time Monitoring
- Current electricity prices for all regions (NSW, VIC, QLD, SA, TAS)
- Live dam level updates
- Market statistics and trends

#### Historical Analysis
- 12+ months of historical data
- Interactive charts and visualizations
- Price volatility analysis
- Dam level trends

#### Price Predictions
- Machine learning models trained on historical data
- Confidence scoring for predictions
- Trading insights and risk factors
- Feature importance analysis

### Data Sources

#### Electricity Prices
- **AEMO (Australian Energy Market Operator)**: Wholesale electricity market data
- **AER (Australian Energy Regulator)**: Market performance reports
- **Regions**: NSW, VIC, QLD, SA, TAS

#### Dam Levels
- **WaterNSW**: New South Wales dam levels
- **Melbourne Water**: Victoria water storage levels
- **Seqwater**: Queensland dam levels
- **Bureau of Meteorology**: National water storage data

## API Endpoints

### Electricity Prices
- `GET /api/electricity/prices` - Get electricity prices with filtering
- `GET /api/electricity/prices/current` - Get current prices for all regions
- `GET /api/electricity/prices/trends` - Get price trends and statistics
- `GET /api/electricity/prices/regions` - Get available regions

### Dam Levels
- `GET /api/dams/levels` - Get dam levels with filtering
- `GET /api/dams/levels/current` - Get current dam levels
- `GET /api/dams/levels/trends` - Get dam level trends and statistics
- `GET /api/dams/levels/states` - Get available states
- `GET /api/dams/levels/dams` - Get available dams

### System
- `GET /api/health` - Health check
- `GET /api/stats` - Database statistics

## Configuration

### Environment Variables

```bash
# Database URL (default: sqlite:///./electricity_data.db)
DATABASE_URL=sqlite:///./electricity_data.db

# API Settings
API_HOST=0.0.0.0
API_PORT=8000
```

### Database

The system uses SQLite by default, but can be configured to use PostgreSQL or MySQL by changing the `DATABASE_URL` environment variable.

## Development

### Project Structure

```
auselectricity/
├── backend/
│   ├── api/                 # FastAPI application
│   ├── data/               # Data models and collectors
│   ├── database/           # Database configuration
│   └── ml/                 # Machine learning models
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   └── pages/          # Page components
│   └── public/             # Static assets
├── data/                   # Data storage
└── docs/                   # Documentation
```

### Adding New Data Sources

1. Create a new collector in `backend/data/collectors/`
2. Add data models in `backend/data/models/`
3. Create API routes in `backend/api/routes/`
4. Update the frontend components

### Machine Learning Models

The prediction models are located in `backend/ml/price_predictor.py`. To retrain models:

1. Update the training data
2. Modify feature engineering
3. Adjust model parameters
4. Test and validate results

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Check if the database file exists
   - Verify SQLite installation
   - Run `python initialize_data.py` to recreate the database

2. **API Connection Issues**
   - Ensure the backend is running on port 8000
   - Check CORS settings in `backend/api/main.py`
   - Verify the proxy setting in `frontend/package.json`

3. **Frontend Build Issues**
   - Clear npm cache: `npm cache clean --force`
   - Delete node_modules and reinstall: `rm -rf node_modules && npm install`
   - Check Node.js version compatibility

4. **Data Loading Issues**
   - Verify sample data generation
   - Check database initialization
   - Review API endpoint responses

### Logs and Debugging

- Backend logs are displayed in the terminal running `start_backend.py`
- Frontend logs are available in the browser console
- API documentation at http://localhost:8000/docs

## Production Deployment

### Backend Deployment

1. Use a production WSGI server like Gunicorn
2. Set up a reverse proxy with Nginx
3. Configure environment variables
4. Set up database backups

### Frontend Deployment

1. Build the production bundle: `npm run build`
2. Serve static files with a web server
3. Configure API endpoints for production
4. Set up SSL certificates

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is for educational and research purposes. Please ensure compliance with data usage policies when accessing real market data.

## Disclaimer

This tool is for educational and research purposes only. Always consult with financial advisors before making trading decisions in the electricity market. Past performance does not guarantee future results.
