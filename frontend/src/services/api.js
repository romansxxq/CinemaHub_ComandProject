import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
const AUTH_URL = `${API_BASE_URL}/auth`;

export const authService = {
  register: (data) => axios.post(`${AUTH_URL}/register/`, data),
  login: (email, password) => axios.post(`${AUTH_URL}/login/`, { email, password }),
  getProfile: (token) =>
    axios.get(`${AUTH_URL}/profile/`, {
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    }),
};

export default axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});