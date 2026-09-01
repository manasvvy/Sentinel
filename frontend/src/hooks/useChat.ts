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

        // Call backend API
        const response = await apiClient.post(API_ENDPOINTS.CHAT, {
          sessionId: store.sessionId,
          message: content,
        });

        // Update streaming message with response
        const { message, confidence, confidenceReasoning } = response.data;
        store.updateLastMessage({
          content: message,
          confidenceScore: confidence,
          confidenceLevel:
            confidence >= 0.8
              ? 'confident'
              : confidence >= 0.5
              ? 'cautious'
              : 'guessing',
          reasoning: confidenceReasoning
            ? [confidenceReasoning]
            : undefined,
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
    async (correctInfo: CorrectInfo, context: string) => {
      try {
        await apiClient.post(API_ENDPOINTS.CORRECT, {
          sessionId: store.sessionId,
          messageId: correctInfo.messageId,
          feedbackText: correctInfo.feedbackText || context,
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
      return response.data.metrics;
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
