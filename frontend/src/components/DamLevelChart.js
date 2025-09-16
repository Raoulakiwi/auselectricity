import React from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Card } from 'react-bootstrap';

const DamLevelChart = ({ data, title, height = 400 }) => {
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

  // Group data by dam name
  const damNames = [...new Set(data.map(item => item.dam_name))];
  const colors = ['#8884d8', '#82ca9d', '#ffc658', '#ff7300', '#00ff00', '#ff00ff', '#00ffff'];

  return (
    <Card className="chart-container">
      <Card.Header>{title}</Card.Header>
      <Card.Body>
        <ResponsiveContainer width="100%" height={height}>
          <AreaChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="timestamp" 
              tickFormatter={(value) => new Date(value).toLocaleDateString()}
            />
            <YAxis domain={[0, 100]} />
            <Tooltip 
              labelFormatter={(value) => new Date(value).toLocaleString()}
              formatter={(value, name) => [`${value.toFixed(1)}%`, name]}
            />
            <Legend />
            {damNames.map((damName, index) => (
              <Area
                key={damName}
                type="monotone"
                dataKey={damName}
                stackId="1"
                stroke={colors[index % colors.length]}
                fill={colors[index % colors.length]}
                fillOpacity={0.6}
              />
            ))}
          </AreaChart>
        </ResponsiveContainer>
      </Card.Body>
    </Card>
  );
};

export default DamLevelChart;
