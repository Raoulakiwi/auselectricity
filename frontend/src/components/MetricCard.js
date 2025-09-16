import React from 'react';
import { Card } from 'react-bootstrap';

const MetricCard = ({ title, value, unit, trend, color = 'primary' }) => {
  const getTrendIcon = () => {
    if (trend > 0) return '↗️';
    if (trend < 0) return '↘️';
    return '→';
  };

  const getTrendColor = () => {
    if (trend > 0) return 'text-success';
    if (trend < 0) return 'text-danger';
    return 'text-muted';
  };

  return (
    <Card className={`metric-card bg-${color} text-white`}>
      <Card.Body className="text-center">
        <div className="metric-value">{value}</div>
        <div className="metric-label">{title}</div>
        {unit && <div className="metric-unit">{unit}</div>}
        {trend !== undefined && (
          <div className={`trend ${getTrendColor()}`}>
            {getTrendIcon()} {Math.abs(trend).toFixed(1)}%
          </div>
        )}
      </Card.Body>
    </Card>
  );
};

export default MetricCard;
