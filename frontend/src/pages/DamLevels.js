import React, { useState } from 'react';
import { Row, Col, Card, Form, Button, Table, Container } from 'react-bootstrap';
import { useQuery } from 'react-query';
import axios from 'axios';
import DamLevelChart from '../components/DamLevelChart';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import { getSourceInfo, getDamUrl } from '../data/sources';

const DamLevels = () => {
  const [startDate, setStartDate] = useState(new Date(Date.now() - 30 * 24 * 60 * 60 * 1000)); // 30 days ago
  const [endDate, setEndDate] = useState(new Date());
  const [selectedState, setSelectedState] = useState('');
  const [selectedDam, setSelectedDam] = useState('');
  const [trendDays, setTrendDays] = useState(30);

  // Fetch dam levels
  const { data: damData, isLoading: damLoading } = useQuery(
    ['damLevels', startDate, endDate, selectedState, selectedDam],
    () => {
      const params = new URLSearchParams();
      if (startDate) params.append('start_date', startDate.toISOString());
      if (endDate) params.append('end_date', endDate.toISOString());
      if (selectedState) params.append('state', selectedState);
      if (selectedDam) params.append('dam_name', selectedDam);
      params.append('size', '1000');
      
      return axios.get(`/api/dams/levels?${params}`).then(res => res.data);
    }
  );

  // Fetch dam level trends
  const { data: trendsData, isLoading: trendsLoading } = useQuery(
    ['damTrends', trendDays, selectedState, selectedDam],
    () => {
      const params = new URLSearchParams();
      params.append('days', trendDays);
      if (selectedState) params.append('state', selectedState);
      if (selectedDam) params.append('dam_name', selectedDam);
      
      return axios.get(`/api/dams/levels/trends?${params}`).then(res => res.data);
    }
  );

  // Fetch available states
  const { data: statesData } = useQuery(
    'states',
    () => axios.get('/api/dams/levels/states').then(res => res.data)
  );

  // Fetch available dams
  const { data: damsData } = useQuery(
    ['dams', selectedState],
    () => {
      const params = new URLSearchParams();
      if (selectedState) params.append('state', selectedState);
      
      return axios.get(`/api/dams/levels/dams?${params}`).then(res => res.data);
    }
  );

  // Fetch current dam levels
  const { data: currentDamLevels } = useQuery(
    'currentDamLevels',
    () => axios.get('/api/dams/levels/current').then(res => res.data)
  );

  // Prepare chart data
  const prepareChartData = () => {
    if (!damData?.dam_levels) return [];
    
    // Group by timestamp and create series for each dam
    const grouped = {};
    damData.dam_levels.forEach(level => {
      const timestamp = new Date(level.timestamp).toISOString();
      if (!grouped[timestamp]) {
        grouped[timestamp] = { timestamp };
      }
      grouped[timestamp][level.dam_name] = level.capacity_percentage;
    });

    return Object.values(grouped).sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
  };

  const handleFilter = () => {
    // The query will automatically refetch when dependencies change
  };

  if (damLoading || trendsLoading) {
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
          <h1>Dam Levels</h1>
          <p className="text-muted">Water storage levels across major Australian dams</p>
        </Col>
      </Row>

      {/* Filters */}
      <Card className="filter-section">
        <Card.Header>Filters</Card.Header>
        <Card.Body>
          <Row>
            <Col md={2}>
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
            <Col md={2}>
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
            <Col md={2}>
              <Form.Group>
                <Form.Label>State</Form.Label>
                <Form.Select
                  value={selectedState}
                  onChange={(e) => {
                    setSelectedState(e.target.value);
                    setSelectedDam(''); // Reset dam selection when state changes
                  }}
                >
                  <option value="">All States</option>
                  {statesData?.states?.map(state => (
                    <option key={state} value={state}>{state}</option>
                  ))}
                </Form.Select>
              </Form.Group>
            </Col>
            <Col md={3}>
              <Form.Group>
                <Form.Label>Dam</Form.Label>
                <Form.Select
                  value={selectedDam}
                  onChange={(e) => setSelectedDam(e.target.value)}
                  disabled={!selectedState}
                >
                  <option value="">All Dams</option>
                  {damsData?.dams?.map(dam => (
                    <option key={dam.name} value={dam.name}>{dam.name}</option>
                  ))}
                </Form.Select>
              </Form.Group>
            </Col>
            <Col md={2}>
              <Form.Group>
                <Form.Label>Trend Period</Form.Label>
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
            <Col md={1}>
              <Form.Group>
                <Form.Label>&nbsp;</Form.Label>
                <Button onClick={handleFilter} variant="primary" className="w-100">
                  Apply
                </Button>
              </Form.Group>
            </Col>
          </Row>
        </Card.Body>
      </Card>

      {/* Current Dam Levels Overview */}
      {currentDamLevels && (
        <Row className="mb-4">
          <Col>
            <Card className="dashboard-card">
              <Card.Header>
                Current Dam Levels Overview
                <small className="text-muted ms-2">
                  ({currentDamLevels.dam_levels?.length || 0} sites monitored)
                </small>
              </Card.Header>
              <Card.Body>
                <Row>
                  {['NSW', 'VIC', 'QLD', 'SA', 'TAS'].map(state => {
                    const stateDams = currentDamLevels.dam_levels?.filter(dam => dam.state === state) || [];
                    const avgCapacity = stateDams.length > 0 
                      ? stateDams.reduce((sum, dam) => sum + dam.capacity_percentage, 0) / stateDams.length 
                      : 0;
                    
                    return (
                      <Col md={2} key={state} className="mb-3">
                        <div className="text-center">
                          <h6 className="fw-bold">{state}</h6>
                          <div className={`h4 ${
                            avgCapacity > 80 ? 'text-success' : 
                            avgCapacity > 50 ? 'text-warning' : 'text-danger'
                          }`}>
                            {avgCapacity.toFixed(1)}%
                          </div>
                          <small className="text-muted">
                            {stateDams.length} dam{stateDams.length !== 1 ? 's' : ''}
                          </small>
                        </div>
                      </Col>
                    );
                  })}
                  <Col md={2}>
                    <div className="text-center">
                      <h6 className="fw-bold">Total</h6>
                      <div className="h4 text-primary">
                        {currentDamLevels.dam_levels?.length || 0}
                      </div>
                      <small className="text-muted">sites</small>
                    </div>
                  </Col>
                </Row>
                
                <hr />
                
                <Row>
                  {currentDamLevels.dam_levels?.map(dam => {
                    const specificUrl = getDamUrl(dam.dam_name);
                    const sourceInfo = getSourceInfo('dams', dam.state);
                    const damUrl = specificUrl || sourceInfo?.url;
                    
                    return (
                      <Col md={4} key={`${dam.dam_name}-${dam.state}`} className="mb-2">
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
                          <div className="text-end">
                            <div className={`fw-bold ${
                              dam.capacity_percentage > 80 ? 'text-success' : 
                              dam.capacity_percentage > 50 ? 'text-warning' : 'text-danger'
                            }`}>
                              {dam.capacity_percentage.toFixed(1)}%
                            </div>
                            <small className="text-muted">
                              {dam.volume_ml.toLocaleString()} ML
                            </small>
                          </div>
                        </div>
                      </Col>
                    );
                  })}
                </Row>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      )}

      {/* Dam Level Chart */}
      <Row className="mb-4">
        <Col>
          <DamLevelChart
            data={prepareChartData()}
            title={`Dam Levels - ${selectedState || 'All States'}`}
            height={500}
          />
        </Col>
      </Row>

      {/* Dam Statistics */}
      {trendsData && (
        <Row className="mb-4">
          <Col md={6}>
            <Card className="dashboard-card">
              <Card.Header>Storage Statistics</Card.Header>
              <Card.Body>
                <Row>
                  <Col>
                    <div className="text-center">
                      <div className="h3 text-primary">{trendsData.average_capacity?.toFixed(1) || 'N/A'}%</div>
                      <div className="text-muted">Average Capacity</div>
                    </div>
                  </Col>
                  <Col>
                    <div className="text-center">
                      <div className="h3 text-success">{trendsData.max_capacity?.toFixed(1) || 'N/A'}%</div>
                      <div className="text-muted">Maximum Capacity</div>
                    </div>
                  </Col>
                  <Col>
                    <div className="text-center">
                      <div className="h3 text-warning">{trendsData.min_capacity?.toFixed(1) || 'N/A'}%</div>
                      <div className="text-muted">Minimum Capacity</div>
                    </div>
                  </Col>
                </Row>
                <hr />
                <div className="text-center">
                  <div className="h4 text-info">{trendsData.capacity_volatility?.toFixed(2) || 'N/A'}</div>
                  <div className="text-muted">Capacity Volatility (Standard Deviation)</div>
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

      {/* Recent Dam Levels Table */}
      <Row>
        <Col>
          <Card className="dashboard-card">
            <Card.Header>Recent Dam Levels</Card.Header>
            <Card.Body>
              <Table responsive striped hover>
                <thead>
                  <tr>
                    <th>Timestamp</th>
                    <th>Dam Name</th>
                    <th>State</th>
                    <th>Capacity %</th>
                    <th>Volume (ML)</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {damData?.dam_levels?.map((level, index) => {
                    const specificUrl = getDamUrl(level.dam_name);
                    const sourceInfo = getSourceInfo('dams', level.state);
                    const damUrl = specificUrl || sourceInfo?.url;
                    
                    return (
                      <tr key={index}>
                        <td>{new Date(level.timestamp).toLocaleString()}</td>
                        <td>
                          <a 
                            href={damUrl} 
                            target="_blank" 
                            rel="noopener noreferrer"
                            className="fw-bold dam-name-link"
                            title={specificUrl ? `View ${level.dam_name} specific information` : `View ${sourceInfo?.name} data`}
                          >
                            {level.dam_name}
                          </a>
                        </td>
                        <td>
                          <span className="badge bg-secondary">{level.state}</span>
                        </td>
                        <td>
                          <span className={`fw-bold ${
                            level.capacity_percentage > 80 ? 'text-success' : 
                            level.capacity_percentage > 50 ? 'text-warning' : 'text-danger'
                          }`}>
                            {level.capacity_percentage.toFixed(1)}%
                          </span>
                        </td>
                        <td>{level.volume_ml.toLocaleString()}</td>
                        <td>
                          <span className={`badge ${
                            level.capacity_percentage > 80 ? 'bg-success' : 
                            level.capacity_percentage > 50 ? 'bg-warning' : 'bg-danger'
                          }`}>
                            {level.capacity_percentage > 80 ? 'High' : 
                             level.capacity_percentage > 50 ? 'Medium' : 'Low'}
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

export default DamLevels;
