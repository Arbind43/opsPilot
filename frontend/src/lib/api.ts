import axios from 'axios';
import { useAuthStore } from '../store/authStore';

// In production (Vercel), VITE_API_URL must be set to the Render backend URL,
// e.g. https://opspilot-backend.onrender.com/api/v1
// In development, the Vite proxy handles /api/v1 → http://localhost:8000
const API_BASE = import.meta.env.VITE_API_URL || '/api/v1';

if (import.meta.env.PROD && !import.meta.env.VITE_API_URL) {
  console.error(
    '[OpsPilot] VITE_API_URL is not set! ' +
    'Set it in your Vercel project environment variables to your Render backend URL, ' +
    'e.g. https://opspilot-backend.onrender.com/api/v1'
  );
}

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().accessToken;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  // When sending FormData, let the browser set Content-Type automatically
  // so it includes the correct multipart boundary. The global default
  // 'application/json' header would break file uploads if left in place.
  if (config.data instanceof FormData) {
    delete config.headers['Content-Type'];
  }

  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    // Handle 401 Unauthorized globally
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const refreshToken = useAuthStore.getState().refreshToken;
        if (!refreshToken) throw new Error('No refresh token');
        
        // Attempt to refresh
        const res = await axios.post('/api/v1/auth/refresh', { refresh_token: refreshToken });
        const { access_token, refresh_token } = res.data;
        
        useAuthStore.getState().setTokens(access_token, refresh_token);
        
        // Retry original request with new token
        originalRequest.headers.Authorization = `Bearer ${access_token}`;
        return api(originalRequest);
      } catch (refreshError) {
        // Refresh failed, logout
        useAuthStore.getState().logout();
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);

export default api;
