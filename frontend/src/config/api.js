// API configuration for different environments
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export { API_BASE_URL };

// Default axios configuration
import axios from 'axios';

axios.defaults.baseURL = API_BASE_URL;

export default axios;
