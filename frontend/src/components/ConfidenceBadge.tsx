'use client';

import { AlertCircle, CheckCircle2, HelpCircle } from 'lucide-react';
import { clsx } from 'clsx';

interface ConfidenceBadgeProps {
  level: 'confident' | 'cautious' | 'guessing';
  score: number;
  compact?: boolean;
}

const confidenceConfig = {
  confident: {
    color: 'bg-green-100 border-green-300 text-green-800',
    icon: CheckCircle2,
    label: 'Confident',
  },
  cautious: {
    color: 'bg-amber-100 border-amber-300 text-amber-800',
    icon: AlertCircle,
    label: 'Cautious',
  },
  guessing: {
    color: 'bg-red-100 border-red-300 text-red-800',
    icon: HelpCircle,
    label: 'Guessing',
  },
};

export const ConfidenceBadge = ({ level, score, compact = false }: ConfidenceBadgeProps) => {
  const config = confidenceConfig[level];
  const Icon = config.icon;

  if (compact) {
    return (
      <span
        className={clsx(
          'inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium border',
          config.color
        )}
      >
        <Icon className="w-3 h-3" />
        {config.label}
      </span>
    );
  }

  return (
    <div
      className={clsx(
        'flex items-center gap-3 p-3 rounded-lg border',
        config.color
      )}
    >
      <Icon className="w-5 h-5 flex-shrink-0" />
      <div>
        <div className="font-semibold text-sm">{config.label}</div>
        <div className="text-xs opacity-75">Confidence: {(score * 100).toFixed(0)}%</div>
      </div>
    </div>
  );
};
