import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import { Container } from 'react-bootstrap';
import Navigation from './components/Navigation';
import Dashboard from './pages/Dashboard';
import ElectricityPrices from './pages/ElectricityPrices';
import DamLevels from './pages/DamLevels';
import Predictions from './pages/Predictions';
import './App.css';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div className="App">
          <Navigation />
          <Container fluid className="mt-4">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/electricity" element={<ElectricityPrices />} />
              <Route path="/dams" element={<DamLevels />} />
              <Route path="/predictions" element={<Predictions />} />
            </Routes>
          </Container>
        </div>
      </Router>
    </QueryClientProvider>
  );
}

export default App;
