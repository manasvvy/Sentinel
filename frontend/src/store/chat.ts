import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  confidenceScore?: number;
  confidenceLevel?: 'confident' | 'cautious' | 'guessing';
  reasoning?: string[];
  timestamp: number;
  isStreaming?: boolean;
}

export interface ChatStore {
  sessionId: string;
  messages: Message[];
  isLoading: boolean;
  error: string | null;
  
  initSession: () => void;
  addMessage: (message: Message) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  clearChat: () => void;
  updateLastMessage: (partial: Partial<Message>) => void;
}

const generateSessionId = () => {
  return `session-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
};

export const useChatStore = create<ChatStore>()(
  devtools(
    persist(
      (set, get) => ({
        sessionId: '',
        messages: [],
        isLoading: false,
        error: null,

        initSession: () => {
          const stored = localStorage.getItem('sessionId');
          const sessionId = stored || generateSessionId();
          localStorage.setItem('sessionId', sessionId);
          set({ sessionId });
        },

        addMessage: (message: Message) => {
          set((state) => ({
            messages: [...state.messages, message],
          }));
        },

        setLoading: (loading: boolean) => {
          set({ isLoading: loading });
        },

        setError: (error: string | null) => {
          set({ error });
        },

        clearChat: () => {
          set({
            messages: [],
            sessionId: generateSessionId(),
            error: null,
          });
          localStorage.removeItem('sessionId');
        },

        updateLastMessage: (partial: Partial<Message>) => {
          set((state) => {
            const messages = [...state.messages];
            const lastIndex = messages.length - 1;
            if (lastIndex >= 0) {
              messages[lastIndex] = { ...messages[lastIndex], ...partial };
            }
            return { messages };
          });
        },
      }),
      {
        name: 'sentinel-chat-store',
        partialize: (state) => ({
          sessionId: state.sessionId,
          messages: state.messages,
        }),
      }
    )
  )
);
