import React, { useState } from 'react';
import { Row, Col, Card, Form, Button, Table, Container } from 'react-bootstrap';
import { useQuery } from 'react-query';
import axios from 'axios';
import PriceChart from '../components/PriceChart';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import { getSourceInfo } from '../data/sources';

const ElectricityPrices = () => {
  const [startDate, setStartDate] = useState(new Date(Date.now() - 30 * 24 * 60 * 60 * 1000)); // 30 days ago
  const [endDate, setEndDate] = useState(new Date());
  const [selectedRegion, setSelectedRegion] = useState('');
  const [trendDays, setTrendDays] = useState(30);

  // Fetch electricity prices
  const { data: pricesData, isLoading: pricesLoading } = useQuery(
    ['electricityPrices', startDate, endDate, selectedRegion],
    () => {
      const params = new URLSearchParams();
      if (startDate) params.append('start_date', startDate.toISOString());
      if (endDate) params.append('end_date', endDate.toISOString());
      if (selectedRegion) params.append('region', selectedRegion);
      params.append('size', '1000');
      
      return axios.get(`/api/electricity/prices?${params}`).then(res => res.data);
    }
  );

  // Fetch price trends
  const { data: trendsData, isLoading: trendsLoading } = useQuery(
    ['priceTrends', trendDays, selectedRegion],
    () => {
      const params = new URLSearchParams();
      params.append('days', trendDays);
      if (selectedRegion) params.append('region', selectedRegion);
      
      return axios.get(`/api/electricity/prices/trends?${params}`).then(res => res.data);
    }
  );

  // Fetch available regions
  const { data: regionsData } = useQuery(
    'regions',
    () => axios.get('/api/electricity/prices/regions').then(res => res.data)
  );

  // Prepare chart data
  const prepareChartData = () => {
    if (!pricesData?.prices) return [];
    
    // Group by timestamp and create series for each region
    const grouped = {};
    pricesData.prices.forEach(price => {
      const timestamp = new Date(price.timestamp).toISOString();
      if (!grouped[timestamp]) {
        grouped[timestamp] = { timestamp };
      }
      grouped[timestamp][price.region] = price.price;
    });

    return Object.values(grouped).sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
  };

  const handleFilter = () => {
    // The query will automatically refetch when dependencies change
  };

  if (pricesLoading || trendsLoading) {
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
          <h1>Electricity Prices</h1>
          <p className="text-muted">Historical and current wholesale electricity prices across Australian regions</p>
        </Col>
      </Row>

      {/* Filters */}
      <Card className="filter-section">
        <Card.Header>Filters</Card.Header>
        <Card.Body>
          <Row>
            <Col md={3}>
              <Form.Group>
                <Form.Label>Start Date</Form.Label>
                <DatePicker
                  selected={startDate}
                  onChange={setStartDate}
                  dateFormat="yyyy-MM-dd"
                  className="form-control"
                />
              </Form.Group>
            </Col>
            <Col md={3}>
              <Form.Group>
                <Form.Label>End Date</Form.Label>
                <DatePicker
                  selected={endDate}
                  onChange={setEndDate}
                  dateFormat="yyyy-MM-dd"
                  className="form-control"
                />
              </Form.Group>
            </Col>
            <Col md={3}>
              <Form.Group>
                <Form.Label>Region</Form.Label>
                <Form.Select
                  value={selectedRegion}
                  onChange={(e) => setSelectedRegion(e.target.value)}
                >
                  <option value="">All Regions</option>
                  {regionsData?.regions?.map(region => (
                    <option key={region} value={region}>{region}</option>
                  ))}
                </Form.Select>
              </Form.Group>
            </Col>
            <Col md={3}>
              <Form.Group>
                <Form.Label>Trend Period (Days)</Form.Label>
                <Form.Select
                  value={trendDays}
                  onChange={(e) => setTrendDays(parseInt(e.target.value))}
                >
                  <option value={7}>7 Days</option>
                  <option value={30}>30 Days</option>
                  <option value={90}>90 Days</option>
                  <option value={365}>1 Year</option>
                </Form.Select>
              </Form.Group>
            </Col>
          </Row>
          <Row className="mt-3">
            <Col>
              <Button onClick={handleFilter} variant="primary">
                Apply Filters
              </Button>
            </Col>
          </Row>
        </Card.Body>
      </Card>

      {/* Price Chart */}
      <Row className="mb-4">
        <Col>
          <PriceChart
            data={prepareChartData()}
            title={`Electricity Prices - ${selectedRegion || 'All Regions'}`}
            height={500}
          />
        </Col>
      </Row>

      {/* Market Statistics */}
      {trendsData && (
        <Row className="mb-4">
          <Col md={6}>
            <Card className="dashboard-card">
              <Card.Header>Market Statistics</Card.Header>
              <Card.Body>
                <Row>
                  <Col>
                    <div className="text-center">
                      <div className="h3 text-primary">${trendsData.average_price?.toFixed(2) || 'N/A'}</div>
                      <div className="text-muted">Average Price (AUD/MWh)</div>
                    </div>
                  </Col>
                  <Col>
                    <div className="text-center">
                      <div className="h3 text-success">${trendsData.min_price?.toFixed(2) || 'N/A'}</div>
                      <div className="text-muted">Minimum Price</div>
                    </div>
                  </Col>
                  <Col>
                    <div className="text-center">
                      <div className="h3 text-danger">${trendsData.max_price?.toFixed(2) || 'N/A'}</div>
                      <div className="text-muted">Maximum Price</div>
                    </div>
                  </Col>
                </Row>
                <hr />
                <div className="text-center">
                  <div className="h4 text-info">{trendsData.price_volatility?.toFixed(2) || 'N/A'}</div>
                  <div className="text-muted">Price Volatility (Standard Deviation)</div>
                </div>
              </Card.Body>
            </Card>
          </Col>
          <Col md={6}>
            <Card className="dashboard-card">
              <Card.Header>Analysis Period</Card.Header>
              <Card.Body>
                <ul className="list-unstyled">
                  <li><strong>Period:</strong> {trendsData.period}</li>
                  <li><strong>Start Date:</strong> {new Date(trendsData.start_date).toLocaleDateString()}</li>
                  <li><strong>End Date:</strong> {new Date(trendsData.end_date).toLocaleDateString()}</li>
                  <li><strong>Data Points:</strong> {trendsData.daily_averages?.length || 0}</li>
                </ul>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      )}

      {/* Recent Prices Table */}
      <Row>
        <Col>
          <Card className="dashboard-card">
            <Card.Header>Recent Prices</Card.Header>
            <Card.Body>
              <Table responsive striped hover>
                <thead>
                  <tr>
                    <th>Timestamp</th>
                    <th>Region</th>
                    <th>Price (AUD/MWh)</th>
                    <th>Demand (MW)</th>
                    <th>Supply (MW)</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {pricesData?.prices?.slice(0, 50).map((price, index) => {
                    const sourceInfo = getSourceInfo('electricity');
                    return (
                      <tr key={index}>
                        <td>{new Date(price.timestamp).toLocaleString()}</td>
                        <td>
                          <a 
                            href={sourceInfo?.url} 
                            target="_blank" 
                            rel="noopener noreferrer"
                            className="badge bg-primary region-badge-link"
                            title={`View ${sourceInfo?.name} data`}
                          >
                            {price.region}
                          </a>
                        </td>
                        <td>
                          <span className={`fw-bold ${
                            price.price > 100 ? 'text-danger' : 
                            price.price > 50 ? 'text-warning' : 'text-success'
                          }`}>
                            ${price.price.toFixed(2)}
                          </span>
                        </td>
                        <td>{price.demand.toFixed(0)}</td>
                        <td>{price.supply.toFixed(0)}</td>
                        <td>
                          <span className={`badge ${
                            price.price > 100 ? 'bg-danger' : 
                            price.price > 50 ? 'bg-warning' : 'bg-success'
                          }`}>
                            {price.price > 100 ? 'High' : price.price > 50 ? 'Medium' : 'Low'}
                          </span>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </Table>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default ElectricityPrices;
