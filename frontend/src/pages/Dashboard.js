import React from 'react';
import { Row, Col, Card, Container } from 'react-bootstrap';
import { useQuery } from 'react-query';
import axios from 'axios';
import PriceChart from '../components/PriceChart';
import DamLevelChart from '../components/DamLevelChart';
import MetricCard from '../components/MetricCard';
import ScraperControl from '../components/ScraperControl';
import { getSourceInfo, getDamUrl } from '../data/sources';

const Dashboard = () => {
  // Fetch current electricity prices
  const { data: currentPrices, isLoading: pricesLoading } = useQuery(
    'currentPrices',
    () => axios.get('/api/electricity/prices/current').then(res => res.data),
    { refetchInterval: 30000 } // Refresh every 30 seconds
  );

  // Fetch current dam levels
  const { data: currentDamLevels, isLoading: damsLoading } = useQuery(
    'currentDamLevels',
    () => axios.get('/api/dams/levels/current').then(res => res.data),
    { refetchInterval: 60000 } // Refresh every minute
  );

  // Fetch price trends for the last 30 days
  const { data: priceTrends } = useQuery(
    'priceTrends',
    () => axios.get('/api/electricity/prices/trends?days=30').then(res => res.data)
  );

  // Fetch dam level trends for the last 30 days
  const { data: damTrends } = useQuery(
    'damTrends',
    () => axios.get('/api/dams/levels/trends?days=30').then(res => res.data)
  );

  // Calculate metrics
  const calculateMetrics = () => {
    if (!currentPrices?.prices || !currentDamLevels?.dam_levels) {
      return {
        avgPrice: 0,
        maxPrice: 0,
        minPrice: 0,
        avgDamLevel: 0,
        totalDams: 0
      };
    }

    const prices = currentPrices.prices.map(p => p.price);
    const damLevels = currentDamLevels.dam_levels.map(d => d.capacity_percentage);

    return {
      avgPrice: prices.reduce((a, b) => a + b, 0) / prices.length,
      maxPrice: Math.max(...prices),
      minPrice: Math.min(...prices),
      avgDamLevel: damLevels.reduce((a, b) => a + b, 0) / damLevels.length,
      totalDams: currentDamLevels.dam_levels.length
    };
  };

  const metrics = calculateMetrics();

  // Prepare chart data
  const preparePriceChartData = () => {
    if (!priceTrends?.daily_averages) return [];
    
    // Group by date and create series for each region
    const grouped = {};
    priceTrends.daily_averages.forEach(item => {
      if (!grouped[item.date]) {
        grouped[item.date] = { timestamp: item.date };
      }
      grouped[item.date][item.region] = item.price;
    });

    return Object.values(grouped).sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
  };

  const prepareDamChartData = () => {
    if (!damTrends?.daily_averages) return [];
    
    // Group by date and create series for each dam
    const grouped = {};
    damTrends.daily_averages.forEach(item => {
      if (!grouped[item.date]) {
        grouped[item.date] = { timestamp: item.date };
      }
      grouped[item.date][item.dam_name] = item.capacity_percentage;
    });

    return Object.values(grouped).sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
  };

  if (pricesLoading || damsLoading) {
    return (
      <Container>
        <div className="loading-spinner">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
        </div>
      </Container>
    );
  }

  return (
    <Container fluid>
      <Row className="mb-4">
        <Col>
          <h1>Australian Electricity Market Dashboard</h1>
          <p className="text-muted">Real-time monitoring of wholesale electricity prices and dam levels</p>
        </Col>
      </Row>

      {/* Data Collection Control */}
      <Row className="mb-4">
        <Col lg={6}>
          <ScraperControl />
        </Col>
        <Col lg={6}>
          <Card className="dashboard-card">
            <Card.Header>Quick Stats</Card.Header>
            <Card.Body>
              <div className="row text-center">
                <div className="col-6">
                  <div className="h4 text-primary">{currentPrices?.prices?.length || 0}</div>
                  <small className="text-muted">Regions</small>
                </div>
                <div className="col-6">
                  <div className="h4 text-info">{currentDamLevels?.dam_levels?.length || 0}</div>
                  <small className="text-muted">Dams</small>
                </div>
              </div>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      {/* Key Metrics */}
      <Row className="mb-4">
        <Col md={3}>
          <MetricCard
            title="Average Price"
            value={`$${metrics.avgPrice.toFixed(2)}`}
            unit="AUD/MWh"
            color="primary"
          />
        </Col>
        <Col md={3}>
          <MetricCard
            title="Max Price"
            value={`$${metrics.maxPrice.toFixed(2)}`}
            unit="AUD/MWh"
            color="danger"
          />
        </Col>
        <Col md={3}>
          <MetricCard
            title="Min Price"
            value={`$${metrics.minPrice.toFixed(2)}`}
            unit="AUD/MWh"
            color="success"
          />
        </Col>
        <Col md={3}>
          <MetricCard
            title="Avg Dam Level"
            value={`${metrics.avgDamLevel.toFixed(1)}%`}
            unit={`${metrics.totalDams} dams monitored`}
            color="info"
          />
        </Col>
      </Row>

      {/* Charts */}
      <Row>
        <Col lg={8}>
          <PriceChart
            data={preparePriceChartData()}
            title="Electricity Prices - Last 30 Days"
            height={400}
          />
        </Col>
        <Col lg={4}>
          <Card className="dashboard-card">
            <Card.Header>
              Current Regional Prices
              <small className="text-muted ms-2">
                <a 
                  href={getSourceInfo('electricity')?.url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="source-link text-light"
                >
                  Source: {getSourceInfo('electricity')?.name}
                </a>
              </small>
            </Card.Header>
            <Card.Body>
              {currentPrices?.prices?.map(price => (
                <div key={price.region} className="d-flex justify-content-between align-items-center mb-2">
                  <span className="fw-bold">{price.region}</span>
                  <span className={`price-indicator ${
                    price.price > 100 ? 'price-high' : 
                    price.price > 50 ? 'price-medium' : 'price-low'
                  }`}>
                    ${price.price.toFixed(2)}
                  </span>
                </div>
              ))}
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <Row className="mt-4">
        <Col lg={6}>
          <DamLevelChart
            data={prepareDamChartData()}
            title="Dam Levels - Last 30 Days"
            height={400}
          />
        </Col>
        <Col lg={6}>
          <Card className="dashboard-card">
            <Card.Header>
              Current Dam Levels
              <small className="text-muted ms-2">
                ({currentDamLevels?.dam_levels?.length || 0} sites)
              </small>
            </Card.Header>
            <Card.Body>
              <Row>
                {currentDamLevels?.dam_levels?.map(dam => {
                  const specificUrl = getDamUrl(dam.dam_name);
                  const sourceInfo = getSourceInfo('dams', dam.state);
                  const damUrl = specificUrl || sourceInfo?.url;
                  
                  return (
                    <Col md={6} key={`${dam.dam_name}-${dam.state}`} className="mb-2">
                      <div className="d-flex justify-content-between align-items-center p-2 border rounded">
                        <div>
                          <div className="fw-bold">
                            <a 
                              href={damUrl} 
                              target="_blank" 
                              rel="noopener noreferrer"
                              className="dam-name-link"
                              title={specificUrl ? `View ${dam.dam_name} specific information` : `View ${sourceInfo?.name} data`}
                            >
                              {dam.dam_name}
                            </a>
                          </div>
                          <small className="text-muted">{dam.state}</small>
                        </div>
                        <span className={`dam-level-indicator ${
                          dam.capacity_percentage > 80 ? 'level-high' : 
                          dam.capacity_percentage > 50 ? 'level-medium' : 'level-low'
                        }`}>
                          {dam.capacity_percentage.toFixed(1)}%
                        </span>
                      </div>
                    </Col>
                  );
                })}
              </Row>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      {/* Market Summary */}
      <Row className="mt-4">
        <Col>
          <Card className="dashboard-card">
            <Card.Header>Market Summary</Card.Header>
            <Card.Body>
              <Row>
                <Col md={6}>
                  <h5>Electricity Market</h5>
                  <ul className="list-unstyled">
                    <li><strong>Average Price:</strong> ${metrics.avgPrice.toFixed(2)}/MWh</li>
                    <li><strong>Price Range:</strong> ${metrics.minPrice.toFixed(2)} - ${metrics.maxPrice.toFixed(2)}</li>
                    <li><strong>Regions Monitored:</strong> 5 (NSW, VIC, QLD, SA, TAS)</li>
                    <li><strong>Last Updated:</strong> {currentPrices?.timestamp ? new Date(currentPrices.timestamp).toLocaleString() : 'N/A'}</li>
                  </ul>
                </Col>
                <Col md={6}>
                  <h5>Water Storage</h5>
                  <ul className="list-unstyled">
                    <li><strong>Average Capacity:</strong> {metrics.avgDamLevel.toFixed(1)}%</li>
                    <li><strong>Dams Monitored:</strong> {metrics.totalDams}</li>
                    <li><strong>States Covered:</strong> 5 (NSW, VIC, QLD, SA, TAS)</li>
                    <li><strong>Last Updated:</strong> {currentDamLevels?.timestamp ? new Date(currentDamLevels.timestamp).toLocaleString() : 'N/A'}</li>
                  </ul>
                </Col>
              </Row>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default Dashboard;
