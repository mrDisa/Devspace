import axios from 'axios';

const client = axios.create({ baseURL: '/api/v1/', headers: { 'Content-Type': 'application/json' } });
client.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});
let refreshing;
client.interceptors.response.use((response) => response, async (error) => {
  const request = error.config;
  if (error.response?.status !== 401 || request?._retry || !localStorage.getItem('refresh_token')) return Promise.reject(error);
  request._retry = true;
  try {
    refreshing ||= axios.post('/api/v1/token/refresh/', { refresh: localStorage.getItem('refresh_token') }).then(({ data }) => {
      localStorage.setItem('access_token', data.access); return data.access;
    }).finally(() => { refreshing = null; });
    request.headers.Authorization = `Bearer ${await refreshing}`;
    return client(request);
  } catch (refreshError) { localStorage.removeItem('access_token'); localStorage.removeItem('refresh_token'); return Promise.reject(refreshError); }
});
export default client;
