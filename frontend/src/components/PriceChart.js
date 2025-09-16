import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Card } from 'react-bootstrap';

const PriceChart = ({ data, title, height = 400 }) => {
  if (!data || data.length === 0) {
    return (
      <Card className="chart-container">
        <Card.Header>{title}</Card.Header>
        <Card.Body>
          <div className="loading-spinner">
            <div className="spinner-border text-primary" role="status">
              <span className="visually-hidden">Loading...</span>
            </div>
          </div>
        </Card.Body>
      </Card>
    );
  }

  return (
    <Card className="chart-container">
      <Card.Header>{title}</Card.Header>
      <Card.Body>
        <ResponsiveContainer width="100%" height={height}>
          <LineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="timestamp" 
              tickFormatter={(value) => new Date(value).toLocaleDateString()}
            />
            <YAxis />
            <Tooltip 
              labelFormatter={(value) => new Date(value).toLocaleString()}
              formatter={(value, name) => [`$${value.toFixed(2)}`, name]}
            />
            <Legend />
            <Line 
              type="monotone" 
              dataKey="NSW" 
              stroke="#8884d8" 
              strokeWidth={2}
              dot={false}
            />
            <Line 
              type="monotone" 
              dataKey="VIC" 
              stroke="#82ca9d" 
              strokeWidth={2}
              dot={false}
            />
            <Line 
              type="monotone" 
              dataKey="QLD" 
              stroke="#ffc658" 
              strokeWidth={2}
              dot={false}
            />
            <Line 
              type="monotone" 
              dataKey="SA" 
              stroke="#ff7300" 
              strokeWidth={2}
              dot={false}
            />
            <Line 
              type="monotone" 
              dataKey="TAS" 
              stroke="#00ff00" 
              strokeWidth={2}
              dot={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </Card.Body>
    </Card>
  );
};

export default PriceChart;
