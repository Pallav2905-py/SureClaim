import axios from "axios";


const api = axios.create({
  baseURL: 'http://127.0.0.1:5000/'
});

export const apiService = {
    detectFraud: (policies) => api.post('/detect_fraud', { policies }),
    explainPolicy: (policyName) => api.get(`/explain_policy?policy_name=${encodeURIComponent(policyName)}`),
    recommendPolicy: (userData) => api.post('/recommend_policy', userData)
  };