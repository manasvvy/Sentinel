// Confidence levels and their visual representations
export const CONFIDENCE_LEVELS = {
  CONFIDENT: { label: "Confident", color: "bg-green-500", bgLight: "bg-green-50", textColor: "text-green-700", borderColor: "border-green-200" },
  CAUTIOUS: { label: "Cautious", color: "bg-amber-500", bgLight: "bg-amber-50", textColor: "text-amber-700", borderColor: "border-amber-200" },
  GUESSING: { label: "Guessing", color: "bg-red-500", bgLight: "bg-red-50", textColor: "text-red-700", borderColor: "border-red-200" },
} as const;

// Confidence score thresholds
export const CONFIDENCE_THRESHOLDS = {
  CONFIDENT_MIN: 0.8,
  CAUTIOUS_MIN: 0.5,
  GUESSING_MIN: 0,
} as const;

// API endpoints
export const API_ENDPOINTS = {
  CHAT: "/chat",
  CORRECT: "/correct",
  SESSION_SUMMARY: "/session/:id/summary",
  HEALTH: "/health",
} as const;

// UI constants
export const UI_CONSTANTS = {
  MESSAGE_CHAR_LIMIT: 5000,
  MAX_MESSAGES_PER_SESSION: 1000,
  AUTO_SCROLL_THRESHOLD: 100, // pixels from bottom
  TOAST_DURATION: 3000, // ms
} as const;

// Local storage keys
export const STORAGE_KEYS = {
  SESSION_ID: "sessionId",
  CHAT_HISTORY: "chatHistory",
  USER_PREFERENCES: "userPreferences",
  THEME: "theme",
} as const;