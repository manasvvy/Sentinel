import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    const sessionId = localStorage.getItem('sessionId');
    if (sessionId) {
      config.headers['X-Session-ID'] = sessionId;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle auth errors
      localStorage.removeItem('sessionId');
    }
    return Promise.reject(error);
  }
);

export const chatApi = {
  sendMessage: async (userInput: string, sessionId: string) => {
    const response = await apiClient.post('/chat', {
      user_input: userInput,
      session_id: sessionId,
    });
    return response.data;
  },

  recordCorrection: async (sessionId: string, correctInfo: string, note?: string) => {
    const response = await apiClient.post('/correct', {
      session_id: sessionId,
      correct_info: correctInfo,
      note: note || null,
    });
    return response.data;
  },

  getSessionSummary: async (sessionId: string) => {
    const response = await apiClient.get(`/session/${sessionId}/summary`);
    return response.data;
  },

  healthCheck: async () => {
    const response = await apiClient.get('/health');
    return response.data;
  },
};
