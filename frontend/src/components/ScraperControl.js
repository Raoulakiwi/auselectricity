import React, { useState, useEffect } from 'react';
import { Card, Button, Alert, Spinner, Badge } from 'react-bootstrap';
import { Play, ArrowRepeat, CheckCircle, XCircle, Clock } from 'react-bootstrap-icons';

const ScraperControl = () => {
  const [status, setStatus] = useState({
    is_running: false,
    last_run: null,
    last_error: null,
    progress: "Ready to collect data"
  });
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState('');

  // Fetch scraper status on component mount
  useEffect(() => {
    fetchStatus();
    // Poll for status updates every 5 seconds when running
    const interval = setInterval(() => {
      if (status.is_running) {
        fetchStatus();
      }
    }, 5000);

    return () => clearInterval(interval);
  }, [status.is_running]);

  const fetchStatus = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/scraper/status');
      const data = await response.json();
      setStatus(data);
    } catch (error) {
      console.error('Error fetching scraper status:', error);
    }
  };

  const startDataCollection = async () => {
    setIsLoading(true);
    setMessage('');
    
    try {
      const response = await fetch('http://localhost:8000/api/scraper/start', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const data = await response.json();
        setMessage('Data collection started successfully!');
        setStatus(prev => ({ ...prev, is_running: true }));
      } else {
        const errorData = await response.json();
        setMessage(`Error: ${errorData.detail}`);
      }
    } catch (error) {
      setMessage(`Error starting data collection: ${error.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const getStatusIcon = () => {
    if (status.is_running) {
      return <Spinner animation="border" size="sm" className="me-2" />;
    } else if (status.last_error) {
      return <XCircle className="text-danger me-2" />;
    } else if (status.last_run) {
      return <CheckCircle className="text-success me-2" />;
    } else {
      return <Clock className="text-muted me-2" />;
    }
  };

  const getStatusBadge = () => {
    if (status.is_running) {
      return <Badge bg="primary">Running</Badge>;
    } else if (status.last_error) {
      return <Badge bg="danger">Error</Badge>;
    } else if (status.last_run) {
      return <Badge bg="success">Ready</Badge>;
    } else {
      return <Badge bg="secondary">Idle</Badge>;
    }
  };

  const formatLastRun = (timestamp) => {
    if (!timestamp) return 'Never';
    const date = new Date(timestamp);
    return date.toLocaleString();
  };

  return (
    <Card className="dashboard-card">
      <Card.Header className="d-flex justify-content-between align-items-center">
        <h5 className="mb-0">
          <ArrowRepeat className="me-2" />
          Data Collection Control
        </h5>
        {getStatusBadge()}
      </Card.Header>
      <Card.Body>
        <div className="mb-3">
          <div className="d-flex align-items-center mb-2">
            {getStatusIcon()}
            <strong>Status:</strong>
            <span className="ms-2">{status.progress}</span>
          </div>
          
          {status.last_run && (
            <div className="text-muted small">
              <strong>Last Run:</strong> {formatLastRun(status.last_run)}
            </div>
          )}
          
          {status.last_error && (
            <div className="text-danger small mt-1">
              <strong>Last Error:</strong> {status.last_error}
            </div>
          )}
        </div>

        {message && (
          <Alert variant={message.includes('Error') ? 'danger' : 'success'} className="mb-3">
            {message}
          </Alert>
        )}

        <div className="d-grid">
          <Button
            variant={status.is_running ? "secondary" : "primary"}
            size="lg"
            onClick={startDataCollection}
            disabled={status.is_running || isLoading}
            className="d-flex align-items-center justify-content-center"
          >
            {isLoading ? (
              <>
                <Spinner animation="border" size="sm" className="me-2" />
                Starting...
              </>
            ) : status.is_running ? (
              <>
                <Spinner animation="border" size="sm" className="me-2" />
                Collection in Progress...
              </>
            ) : (
              <>
                <Play className="me-2" />
                Start Data Collection
              </>
            )}
          </Button>
        </div>

        <div className="mt-3">
          <small className="text-muted">
            <strong>What this does:</strong> Collects the latest electricity prices and dam levels 
            from various Australian sources. This process may take a few minutes to complete.
          </small>
        </div>
      </Card.Body>
    </Card>
  );
};

export default ScraperControl;
