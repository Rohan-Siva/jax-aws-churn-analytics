import axios from 'axios';
import type { AnalyticsData, UserAnalytics, Prediction, PredictionTimeline } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const api = {
    
    getAnalytics: async (): Promise<AnalyticsData> => {
        const response = await apiClient.get('/api/analytics/');
        return response.data;
    },

    getUserAnalytics: async (limit: number = 100): Promise<UserAnalytics[]> => {
        const response = await apiClient.get('/api/analytics/users', {
            params: { limit },
        });
        return response.data;
    },

    getPredictionTimeline: async (days: number = 30): Promise<PredictionTimeline[]> => {
        const response = await apiClient.get('/api/analytics/predictions/timeline', {
            params: { days },
        });
        return response.data;
    },

    
    predictChurn: async (userId: number): Promise<Prediction> => {
        const response = await apiClient.post('/api/predictions/', {
            user_id: userId,
        });
        return response.data;
    },

    batchPredict: async (userIds: number[]): Promise<Prediction[]> => {
        const response = await apiClient.post('/api/predictions/batch', userIds);
        return response.data;
    },

    
    healthCheck: async (): Promise<{ status: string; model_version: string }> => {
        const response = await apiClient.get('/health');
        return response.data;
    },
};

export default api;
