import { useCallback, useRef } from 'react';
import { chatApi } from '@/config/api';
import { useChatStore, Message } from '@/store/chat';

export const useChat = () => {
  const store = useChatStore();
  const abortControllerRef = useRef<AbortController | null>(null);

  const sendMessage = useCallback(
    async (userInput: string) => {
      if (!userInput.trim()) return;

      try {
        // Initialize session if needed
        if (!store.sessionId) {
          store.initSession();
        }

        // Add user message
        const userMessage: Message = {
          id: `msg-${Date.now()}`,
          role: 'user',
          content: userInput,
          timestamp: Date.now(),
        };
        store.addMessage(userMessage);

        // Add loading message
        const loadingMessage: Message = {
          id: `msg-${Date.now()}-loading`,
          role: 'assistant',
          content: '',
          timestamp: Date.now(),
          isStreaming: true,
        };
        store.addMessage(loadingMessage);
        store.setLoading(true);
        store.setError(null);

        // Call API
        const response = await chatApi.sendMessage(userInput, store.sessionId);

        // Update loading message with response
        store.updateLastMessage({
          content: response.response_text,
          confidenceScore: response.confidence_score,
          confidenceLevel: response.confidence_state,
          reasoning: response.reasoning,
          isStreaming: false,
        });

        store.setLoading(false);
      } catch (error: any) {
        store.setError(error.message || 'Failed to send message');
        // Remove loading message on error
        const messages = store.messages.filter((m) => !m.isStreaming);
        // Reset to previous state (simplified)
        store.setLoading(false);
      }
    },
    [store]
  );

  const recordCorrection = useCallback(
    async (correctInfo: string, note?: string) => {
      try {
        await chatApi.recordCorrection(store.sessionId, correctInfo, note);
        // Optionally show success feedback
      } catch (error: any) {
        store.setError('Failed to record correction');
      }
    },
    [store.sessionId]
  );

  const getSessionMetrics = useCallback(async () => {
    try {
      const summary = await chatApi.getSessionSummary(store.sessionId);
      return summary;
    } catch (error: any) {
      store.setError('Failed to load session metrics');
      return null;
    }
  }, [store.sessionId]);

  return {
    ...store,
    sendMessage,
    recordCorrection,
    getSessionMetrics,
  };
};
