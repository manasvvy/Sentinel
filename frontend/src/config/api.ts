import axios, {
  AxiosInstance,
  InternalAxiosRequestConfig,
  AxiosError,
} from "axios";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

const apiClient: AxiosInstance = axios.create({
  baseURL: API_URL,
  timeout: 30000,
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor to add session ID if available
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const sessionId = localStorage.getItem("sessionId");
    if (sessionId && config.headers) {
      config.headers["X-Session-ID"] = sessionId;
    }
    return config;
  },
  (error: AxiosError) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      // Handle unauthorized - clear session
      localStorage.removeItem("sessionId");
      window.location.href = "/";
    }
    return Promise.reject(error);
  }
);

export default apiClient;