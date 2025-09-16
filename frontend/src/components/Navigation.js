import React from 'react';
import { Navbar, Nav, Container } from 'react-bootstrap';
import { Link, useLocation } from 'react-router-dom';

const Navigation = () => {
  const location = useLocation();
  
  return (
    <Navbar expand="lg" variant="dark">
      <Container>
        <Navbar.Brand as={Link} to="/">
          ⚡ Australian Electricity Market Dashboard
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="ms-auto">
            <Nav.Link as={Link} to="/" active={location.pathname === '/'}>
              Dashboard
            </Nav.Link>
            <Nav.Link as={Link} to="/electricity" active={location.pathname === '/electricity'}>
              Electricity Prices
            </Nav.Link>
            <Nav.Link as={Link} to="/dams" active={location.pathname === '/dams'}>
              Dam Levels
            </Nav.Link>
            <Nav.Link as={Link} to="/predictions" active={location.pathname === '/predictions'}>
              Predictions
            </Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default Navigation;
