import { v4 as uuidv4 } from "uuid";
import { STORAGE_KEYS } from "@/config/constants";

export const generateSessionId = (): string => {
  return uuidv4();
};

export const getOrCreateSessionId = (): string => {
  let sessionId = localStorage.getItem(STORAGE_KEYS.SESSION_ID);
  if (!sessionId) {
    sessionId = generateSessionId();
    localStorage.setItem(STORAGE_KEYS.SESSION_ID, sessionId);
  }
  return sessionId;
};

export const clearSession = (): void => {
  localStorage.removeItem(STORAGE_KEYS.SESSION_ID);
  localStorage.removeItem(STORAGE_KEYS.CHAT_HISTORY);
};
