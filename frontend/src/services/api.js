import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
const AUTH_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/auth';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post(`${AUTH_URL}/refresh/`, {
          refresh: refreshToken,
        });
        
        localStorage.setItem('access_token', response.data.access);
        api.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`;
        return api(originalRequest);
      } catch (err) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(err);
      }
    }
    return Promise.reject(error);
  }
);

// Auth services
export const authService = {
  register: (data) => axios.post(`${AUTH_URL}/register/`, data),
  login: (email, password) => axios.post(`${AUTH_URL}/login/`, { email, password }),
  getProfile: () => api.get(`${AUTH_URL}/profile/`),
  updateProfile: (data) => api.patch(`${AUTH_URL}/profile/`, data),
};

// Movie services
export const movieService = {
  getAll: (params) => api.get('/movies/', { params }),
  getById: (id) => api.get(`/movies/${id}/`),
  getNowShowing: () => api.get('/movies/now_showing/'),
  getByGenre: (genreId) => api.get('/movies/by_genre/', { params: { genre_id: genreId } }),
  getSessions: (movieId) => api.get(`/movies/${movieId}/sessions/`),
};

// Genre services
export const genreService = {
  getAll: () => api.get('/genres/'),
  search: (query) => api.get('/genres/', { params: { search: query } }),
};

// Session services
export const sessionService = {
  getAll: (params) => api.get('/sessions/', { params }),
  getById: (id) => api.get(`/sessions/${id}/`),
  getUpcoming: () => api.get('/sessions/upcoming_sessions/'),
};

// Booking services
export const bookingService = {
  create: (data) => api.post('/bookings/', data),
  getAll: (params) => api.get('/bookings/', { params }),
  getById: (id) => api.get(`/bookings/${id}/`),
  getActive: () => api.get('/bookings/active/'),
  getHistory: () => api.get('/bookings/history/'),
  cancel: (id) => api.post(`/bookings/${id}/cancel/`),
  markPaid: (id) => api.post(`/bookings/${id}/mark_paid/`),
};

export default api;
