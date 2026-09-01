// Message types
export interface Message {
  id: string;
  sessionId: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
  confidence?: number;
  confidenceReasoning?: string;
  isCorrection?: boolean;
}

// Session types
export interface Session {
  id: string;
  createdAt: Date;
  updatedAt: Date;
  messages: Message[];
  corrections: number;
  totalInteractions: number;
  metrics?: SessionMetrics;
}

// Metrics types
export interface SessionMetrics {
  correctionRate: number;
  averageConfidence: number;
  topicsDiscussed: string[];
  confidenceByTopic: Record<string, number>;
  sessionDuration: number; // in seconds
}

// API request/response types
export interface ChatRequest {
  sessionId: string;
  message: string;
}

export interface ChatResponse {
  id: string;
  sessionId: string;
  message: string;
  confidence: number;
  confidenceReasoning: string;
  timestamp: Date;
}

export interface CorrectionRequest {
  sessionId: string;
  messageId: string;
  feedbackText?: string;
}

export interface CorrectionResponse {
  success: boolean;
  message: string;
}

export interface SessionSummaryResponse {
  session: Session;
  metrics: SessionMetrics;
}

// UI state types
export interface UIState {
  isLoading: boolean;
  error: string | null;
  selectedMessage: string | null;
  showMetrics: boolean;
}

// Error types
export interface APIError {
  code: string;
  message: string;
  details?: unknown;
}
