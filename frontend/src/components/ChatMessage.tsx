'use client';

import { Message } from '@/store/chat';
import { ConfidenceBadge } from './ConfidenceBadge';
import { Loader2 } from 'lucide-react';
import { clsx } from 'clsx';

interface ChatMessageProps {
  message: Message;
  onCorrect?: (correctInfo: string) => void;
}

export const ChatMessage = ({ message, onCorrect }: ChatMessageProps) => {
  const isUser = message.role === 'user';
  const isStreaming = message.isStreaming;

  return (
    <div
      className={clsx(
        'flex gap-3 mb-4 animate-fadeIn',
        isUser ? 'justify-end' : 'justify-start'
      )}
    >
      <div
        className={clsx(
          'max-w-xs lg:max-w-md xl:max-w-lg rounded-lg px-4 py-3',
          isUser
            ? 'bg-blue-500 text-white rounded-br-none'
            : 'bg-gray-200 text-gray-900 rounded-bl-none'
        )}
      >
        {isStreaming ? (
          <div className="flex items-center gap-2">
            <Loader2 className="w-4 h-4 animate-spin" />
            <span className="text-sm">Thinking...</span>
          </div>
        ) : (
          <div className="space-y-2">
            <p className="text-sm leading-relaxed whitespace-pre-wrap">{message.content}</p>
            
            {message.confidenceLevel && (
              <div className="mt-3 pt-3 border-t border-opacity-20 border-current">
                <ConfidenceBadge
                  level={message.confidenceLevel}
                  score={message.confidenceScore || 0}
                  compact
                />
              </div>
            )}

            {message.reasoning && message.reasoning.length > 0 && (
              <details className="mt-2">
                <summary className="text-xs opacity-70 cursor-pointer hover:opacity-100">
                  Why this confidence?
                </summary>
                <ul className="mt-1 text-xs opacity-75 space-y-1 ml-4 list-disc">
                  {message.reasoning.map((reason, i) => (
                    <li key={i}>{reason}</li>
                  ))}
                </ul>
              </details>
            )}

            {!isUser && onCorrect && (
              <button
                onClick={() => {
                  const correction = prompt('What is the correct information?');
                  if (correction) onCorrect(correction);
                }}
                className="mt-2 text-xs opacity-70 hover:opacity-100 underline cursor-pointer"
              >
                This response is wrong
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
