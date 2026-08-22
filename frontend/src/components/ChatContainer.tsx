'use client';

import { useEffect } from 'react';
import { ChatMessage } from './ChatMessage';
import { ChatInput } from './ChatInput';
import { SessionMetrics } from './SessionMetrics';
import { useChat } from '@/hooks/useChat';
import { AlertCircle } from 'lucide-react';

export const ChatContainer = () => {
  const { sessionId, messages, isLoading, error, initSession, sendMessage, recordCorrection } =
    useChat();

  useEffect(() => {
    initSession();
  }, []);

  return (
    <div className="flex flex-col h-screen bg-white">
      {/* Header */}
      <header className="border-b border-gray-200 px-4 py-4 sm:px-6 sm:py-5">
        <h1 className="text-2xl font-bold text-gray-900">Sentinel</h1>
        <p className="text-sm text-gray-500 mt-1">AI with transparency and judgment</p>
        {sessionId && (
          <p className="text-xs text-gray-400 mt-2 font-mono">Session: {sessionId.slice(0, 20)}...</p>
        )}
      </header>

      {/* Metrics */}
      {messages.length > 0 && (
        <div className="px-4 py-3 sm:px-6 border-b border-gray-200 bg-gray-50">
          <SessionMetrics />
        </div>
      )}

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-4 py-6 sm:px-6 space-y-4">
        {messages.length === 0 ? (
          <div className="h-full flex items-center justify-center text-center">
            <div className="max-w-sm">
              <h2 className="text-xl font-semibold text-gray-900 mb-2">Welcome to Sentinel</h2>
              <p className="text-gray-600 text-sm leading-relaxed">
                Every response includes transparency about confidence and reasoning. Correct me when
                I'm wrong—that's how I learn.
              </p>
            </div>
          </div>
        ) : (
          messages.map((message) => (
            <ChatMessage
              key={message.id}
              message={message}
              onCorrect={(correctInfo) =>
                recordCorrection(correctInfo, 'User correction from chat')
              }
            />
          ))
        )}

        {/* Error Message */}
        {error && (
          <div className="flex gap-3 mb-4">
            <div className="bg-red-100 border border-red-300 text-red-800 rounded-lg px-4 py-3 flex gap-3 items-start">
              <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" />
              <div>
                <p className="text-sm font-medium">Error</p>
                <p className="text-xs mt-1 opacity-75">{error}</p>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Input */}
      <div className="border-t border-gray-200 px-4 py-4 sm:px-6">
        <ChatInput onSend={sendMessage} isLoading={isLoading} />
      </div>
    </div>
  );
};
