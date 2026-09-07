'use client';

import { useCallback } from 'react';
import { useChatStore, Message } from '@/store/chat';
import apiClient from '@/config/api';
import { API_ENDPOINTS } from '@/config/constants';

interface CorrectInfo {
  messageId: string;
  feedbackText?: string;
}

export const useChat = () => {
  const store = useChatStore();

  const initSession = useCallback(() => {
    store.initSession();
  }, [store]);

  const sendMessage = useCallback(
    async (content: string) => {
      if (!content.trim()) return;

      try {
        // Ensure session is initialized
        if (!store.sessionId) {
          store.initSession();
        }

        // Add user message
        const userMessage: Message = {
          id: `user-${Date.now()}`,
          role: 'user',
          content,
          timestamp: Date.now(),
        };
        store.addMessage(userMessage);

        // Set loading state
        store.setLoading(true);
        store.setError(null);

        // Add streaming placeholder
        const assistantMessage: Message = {
          id: `assistant-${Date.now()}`,
          role: 'assistant',
          content: '',
          isStreaming: true,
          timestamp: Date.now(),
        };
        store.addMessage(assistantMessage);

        // Call backend API - matches backend schema
        const response = await apiClient.post(API_ENDPOINTS.CHAT, {
          user_input: content,
          session_id: store.sessionId,
        });

        // Extract response data matching backend response format
        const { response_text, confidence_score, confidence_state, reasoning } = response.data;
        
        store.updateLastMessage({
          content: response_text,
          confidenceScore: confidence_score,
          confidenceLevel: confidence_state,
          reasoning: reasoning && Array.isArray(reasoning) ? reasoning : [reasoning].filter(Boolean),
          isStreaming: false,
        });

        store.setLoading(false);
      } catch (error) {
        store.setLoading(false);
        const errorMessage =
          error instanceof Error ? error.message : 'Failed to send message';
        store.setError(errorMessage);
        console.error('Chat error:', error);
      }
    },
    [store]
  );

  const recordCorrection = useCallback(
    async (correctInfo: string, context: string) => {
      try {
        await apiClient.post(API_ENDPOINTS.CORRECT, {
          session_id: store.sessionId,
          correct_info: correctInfo,
          note: context,
        });
      } catch (error) {
        console.error('Error recording correction:', error);
        store.setError('Failed to record correction');
      }
    },
    [store]
  );

  const getSessionMetrics = useCallback(async () => {
    try {
      const response = await apiClient.get(
        API_ENDPOINTS.SESSION_SUMMARY.replace(':id', store.sessionId)
      );
      return response.data;
    } catch (error) {
      console.error('Error fetching metrics:', error);
      return null;
    }
  }, [store.sessionId]);

  return {
    sessionId: store.sessionId,
    messages: store.messages,
    isLoading: store.isLoading,
    error: store.error,
    initSession,
    sendMessage,
    recordCorrection,
    getSessionMetrics,
    clearChat: store.clearChat,
  };
};
