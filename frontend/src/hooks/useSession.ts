'use client';

import { useEffect, useState } from 'react';
import { getOrCreateSessionId, clearSession } from '@/utils/session';

export const useSession = () => {
  const [sessionId, setSessionId] = useState<string>('');
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    const id = getOrCreateSessionId();
    setSessionId(id);
    setIsReady(true);
  }, []);

  return {
    sessionId,
    isReady,
    clearSession,
  };
};
