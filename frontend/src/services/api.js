import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getHospitals = () => api.get('/hospitals');
export const updateHospitalBeds = (id, available_beds) => api.put(`/hospitals/${id}/beds`, { available_beds });

export const getAmbulances = () => api.get('/ambulances');
export const updateAmbulanceStatus = (id, status) => api.put(`/ambulances/${id}/status`, { status });
export const resetAmbulanceStatus = (id) => api.post(`/ambulances/${id}/reset`);

export const getDoctors = () => api.get('/doctors');
export const toggleDoctorAvailability = (id) => api.put(`/doctors/${id}/toggle-availability`);

export const searchPatients = (query) => api.get(`/patients/search?query=${encodeURIComponent(query)}`);

export const dispatchEmergency = (payload) => api.post('/emergency/dispatch', payload);

export const getDashboardStats = () => api.get('/analytics/dashboard');

export const adminLogin = (username, password) => api.post('/auth/login', { username, password });

export default api;
