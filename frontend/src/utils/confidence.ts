import { CONFIDENCE_LEVELS, CONFIDENCE_THRESHOLDS } from "@/config/constants";

export type ConfidenceLevel = keyof typeof CONFIDENCE_LEVELS;

export const getConfidenceLevel = (score: number): ConfidenceLevel => {
  if (score >= CONFIDENCE_THRESHOLDS.CONFIDENT_MIN) {
    return "CONFIDENT";
  } else if (score >= CONFIDENCE_THRESHOLDS.CAUTIOUS_MIN) {
    return "CAUTIOUS";
  } else {
    return "GUESSING";
  }
};

export const getConfidenceColor = (score: number): string => {
  const level = getConfidenceLevel(score);
  return CONFIDENCE_LEVELS[level].color;
};

export const getConfidenceBgColor = (score: number): string => {
  const level = getConfidenceLevel(score);
  return CONFIDENCE_LEVELS[level].bgLight;
};

export const getConfidenceTextColor = (score: number): string => {
  const level = getConfidenceLevel(score);
  return CONFIDENCE_LEVELS[level].textColor;
};

export const getConfidenceLabel = (score: number): string => {
  const level = getConfidenceLevel(score);
  return CONFIDENCE_LEVELS[level].label;
};

export const formatConfidencePercentage = (score: number): string => {
  return `${Math.round(score * 100)}%`;
};
