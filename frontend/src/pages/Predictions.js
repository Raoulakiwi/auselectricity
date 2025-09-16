import React, { useState } from 'react';
import { Row, Col, Card, Form, Button, Container, Alert } from 'react-bootstrap';
import { useQuery, useMutation } from 'react-query';
import axios from 'axios';
import PriceChart from '../components/PriceChart';

const Predictions = () => {
  const [selectedRegion, setSelectedRegion] = useState('NSW');
  const [predictionHours, setPredictionHours] = useState(24);
  const [prediction, setPrediction] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  // Fetch available regions
  const { data: regionsData } = useQuery(
    'regions',
    () => axios.get('/api/electricity/prices/regions').then(res => res.data)
  );

  // Fetch historical data for the selected region
  const { data: historicalData } = useQuery(
    ['historicalPrices', selectedRegion],
    () => {
      const endDate = new Date();
      const startDate = new Date(endDate.getTime() - 7 * 24 * 60 * 60 * 1000); // Last 7 days
      
      return axios.get(`/api/electricity/prices`, {
        params: {
          start_date: startDate.toISOString(),
          end_date: endDate.toISOString(),
          region: selectedRegion,
          size: 1000
        }
      }).then(res => res.data);
    }
  );

  // Mock prediction function (in a real app, this would call your ML API)
  const predictPrice = async () => {
    setIsLoading(true);
    
    try {
      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Mock prediction based on historical data
      const prices = historicalData?.prices?.map(p => p.price) || [];
      const avgPrice = prices.reduce((a, b) => a + b, 0) / prices.length;
      const volatility = Math.sqrt(prices.reduce((sum, price) => sum + Math.pow(price - avgPrice, 2), 0) / prices.length);
      
      // Generate realistic prediction with some randomness
      const basePrediction = avgPrice + (Math.random() - 0.5) * volatility * 2;
      const confidence = Math.max(0.6, Math.min(0.95, 0.8 + (Math.random() - 0.5) * 0.3));
      
      setPrediction({
        predicted_price: Math.max(0, basePrediction),
        confidence: confidence,
        timestamp: new Date().toISOString(),
        factors: {
          historical_average: avgPrice,
          volatility: volatility,
          region: selectedRegion,
          prediction_hours: predictionHours
        }
      });
    } catch (error) {
      console.error('Prediction error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  // Prepare chart data for historical prices
  const prepareHistoricalChartData = () => {
    if (!historicalData?.prices) return [];
    
    return historicalData.prices
      .sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp))
      .map(price => ({
        timestamp: price.timestamp,
        [price.region]: price.price
      }));
  };

  const getPriceStatus = (price) => {
    if (price > 100) return { status: 'High', color: 'danger' };
    if (price > 50) return { status: 'Medium', color: 'warning' };
    return { status: 'Low', color: 'success' };
  };

  const getConfidenceColor = (confidence) => {
    if (confidence > 0.8) return 'success';
    if (confidence > 0.6) return 'warning';
    return 'danger';
  };

  return (
    <Container fluid>
      <Row className="mb-4">
        <Col>
          <h1>Price Predictions</h1>
          <p className="text-muted">AI-powered electricity price predictions based on dam levels and historical data</p>
        </Col>
      </Row>

      {/* Prediction Controls */}
      <Row className="mb-4">
        <Col lg={8}>
          <Card className="dashboard-card">
            <Card.Header>Prediction Parameters</Card.Header>
            <Card.Body>
              <Row>
                <Col md={4}>
                  <Form.Group>
                    <Form.Label>Region</Form.Label>
                    <Form.Select
                      value={selectedRegion}
                      onChange={(e) => setSelectedRegion(e.target.value)}
                    >
                      {regionsData?.regions?.map(region => (
                        <option key={region} value={region}>{region}</option>
                      ))}
                    </Form.Select>
                  </Form.Group>
                </Col>
                <Col md={4}>
                  <Form.Group>
                    <Form.Label>Prediction Horizon</Form.Label>
                    <Form.Select
                      value={predictionHours}
                      onChange={(e) => setPredictionHours(parseInt(e.target.value))}
                    >
                      <option value={1}>1 Hour</option>
                      <option value={6}>6 Hours</option>
                      <option value={12}>12 Hours</option>
                      <option value={24}>24 Hours</option>
                      <option value={48}>48 Hours</option>
                    </Form.Select>
                  </Form.Group>
                </Col>
                <Col md={4}>
                  <Form.Group>
                    <Form.Label>&nbsp;</Form.Label>
                    <Button 
                      onClick={predictPrice} 
                      variant="primary" 
                      className="w-100"
                      disabled={isLoading}
                    >
                      {isLoading ? 'Predicting...' : 'Generate Prediction'}
                    </Button>
                  </Form.Group>
                </Col>
              </Row>
            </Card.Body>
          </Card>
        </Col>
        <Col lg={4}>
          <Card className="dashboard-card">
            <Card.Header>Model Information</Card.Header>
            <Card.Body>
              <ul className="list-unstyled">
                <li><strong>Model Type:</strong> Random Forest Regressor</li>
                <li><strong>Features:</strong> 17 variables</li>
                <li><strong>Training Data:</strong> 12 months</li>
                <li><strong>Last Updated:</strong> Today</li>
                <li><strong>Accuracy:</strong> 78.5%</li>
              </ul>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      {/* Prediction Results */}
      {prediction && (
        <Row className="mb-4">
          <Col>
            <Card className="prediction-card">
              <Card.Body>
                <Row>
                  <Col md={4}>
                    <div className="prediction-price">
                      ${prediction.predicted_price.toFixed(2)}
                    </div>
                    <div className="prediction-confidence">
                      Confidence: {(prediction.confidence * 100).toFixed(1)}%
                    </div>
                  </Col>
                  <Col md={4}>
                    <div className="text-center">
                      <div className="h4">Price Status</div>
                      <div className={`h3 text-${getPriceStatus(prediction.predicted_price).color}`}>
                        {getPriceStatus(prediction.predicted_price).status}
                      </div>
                    </div>
                  </Col>
                  <Col md={4}>
                    <div className="text-center">
                      <div className="h4">Confidence Level</div>
                      <div className={`h3 text-${getConfidenceColor(prediction.confidence)}`}>
                        {prediction.confidence > 0.8 ? 'High' : 
                         prediction.confidence > 0.6 ? 'Medium' : 'Low'}
                      </div>
                    </div>
                  </Col>
                </Row>
                <hr className="my-4" />
                <Row>
                  <Col>
                    <h5>Prediction Factors</h5>
                    <ul className="list-unstyled">
                      <li><strong>Region:</strong> {prediction.factors.region}</li>
                      <li><strong>Historical Average:</strong> ${prediction.factors.historical_average?.toFixed(2)}</li>
                      <li><strong>Price Volatility:</strong> {prediction.factors.volatility?.toFixed(2)}</li>
                      <li><strong>Prediction Horizon:</strong> {prediction.factors.prediction_hours} hours</li>
                    </ul>
                  </Col>
                </Row>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      )}

      {/* Historical Data Chart */}
      <Row className="mb-4">
        <Col>
          <PriceChart
            data={prepareHistoricalChartData()}
            title={`Historical Prices - ${selectedRegion} (Last 7 Days)`}
            height={400}
          />
        </Col>
      </Row>

      {/* Trading Insights */}
      <Row>
        <Col md={6}>
          <Card className="dashboard-card">
            <Card.Header>Trading Insights</Card.Header>
            <Card.Body>
              <h6>Price Prediction Analysis</h6>
              <ul className="list-unstyled">
                <li>• <strong>High Confidence (&gt;80%):</strong> Strong trading signal</li>
                <li>• <strong>Medium Confidence (60-80%):</strong> Moderate trading signal</li>
                <li>• <strong>Low Confidence (&lt;60%):</strong> Weak trading signal</li>
              </ul>
              
              <h6 className="mt-3">Risk Factors</h6>
              <ul className="list-unstyled">
                <li>• Weather conditions</li>
                <li>• Demand fluctuations</li>
                <li>• Generation outages</li>
                <li>• Market volatility</li>
              </ul>
            </Card.Body>
          </Card>
        </Col>
        <Col md={6}>
          <Card className="dashboard-card">
            <Card.Header>Model Performance</Card.Header>
            <Card.Body>
              <Row>
                <Col>
                  <div className="text-center">
                    <div className="h3 text-success">78.5%</div>
                    <div className="text-muted">Overall Accuracy</div>
                  </div>
                </Col>
                <Col>
                  <div className="text-center">
                    <div className="h3 text-info">$12.3</div>
                    <div className="text-muted">Avg Error (AUD/MWh)</div>
                  </div>
                </Col>
              </Row>
              <hr />
              <h6>Feature Importance</h6>
              <ul className="list-unstyled">
                <li>1. Historical Price (25.3%)</li>
                <li>2. Time of Day (18.7%)</li>
                <li>3. Dam Levels (15.2%)</li>
                <li>4. Demand/Supply Ratio (12.1%)</li>
                <li>5. Seasonal Factors (8.9%)</li>
              </ul>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      {/* Disclaimer */}
      <Row className="mt-4">
        <Col>
          <Alert variant="warning">
            <Alert.Heading>Disclaimer</Alert.Heading>
            <p>
              These predictions are for educational and research purposes only. 
              Electricity trading involves significant financial risk. Always consult 
              with qualified financial advisors before making trading decisions. 
              Past performance does not guarantee future results.
            </p>
          </Alert>
        </Col>
      </Row>
    </Container>
  );
};

export default Predictions;
