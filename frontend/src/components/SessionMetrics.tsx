'use client';

import { useEffect, useState } from 'react';
import { useChat } from '@/hooks/useChat';
import { TrendingUp, AlertCircle } from 'lucide-react';

interface MetricsData {
  total_messages: number;
  total_corrections: number;
  correction_rate: number;
  avg_confidence: number;
  confidence_trend: number[];
}

export const SessionMetrics = () => {
  const { getSessionMetrics } = useChat();
  const [metrics, setMetrics] = useState<MetricsData | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchMetrics = async () => {
      setLoading(true);
      const data = await getSessionMetrics();
      if (data) {
        setMetrics(data);
      }
      setLoading(false);
    };

    // Fetch every 10 seconds
    const interval = setInterval(fetchMetrics, 10000);
    fetchMetrics();

    return () => clearInterval(interval);
  }, [getSessionMetrics]);

  if (loading || !metrics) {
    return null;
  }

  const correctionTrend = metrics.correction_rate > 0 ? (
    <div className="flex items-center gap-1 text-green-600">
      <TrendingUp className="w-4 h-4" />
      <span className="text-sm font-medium">Learning: {(metrics.correction_rate * 100).toFixed(1)}% corrections</span>
    </div>
  ) : (
    <div className="flex items-center gap-1 text-gray-500">
      <AlertCircle className="w-4 h-4" />
      <span className="text-sm font-medium">No corrections yet</span>
    </div>
  );

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-3 p-4 bg-gray-50 rounded-lg border">
      <div>
        <div className="text-xs text-gray-500 uppercase tracking-wider">Messages</div>
        <div className="text-2xl font-bold text-gray-900">{metrics.total_messages}</div>
      </div>
      <div>
        <div className="text-xs text-gray-500 uppercase tracking-wider">Corrections</div>
        <div className="text-2xl font-bold text-blue-600">{metrics.total_corrections}</div>
      </div>
      <div>
        <div className="text-xs text-gray-500 uppercase tracking-wider">Avg Confidence</div>
        <div className="text-2xl font-bold text-gray-900">{(metrics.avg_confidence * 100).toFixed(0)}%</div>
      </div>
      <div>
        <div className="text-xs text-gray-500 uppercase tracking-wider">Trend</div>
        {correctionTrend}
      </div>
    </div>
  );
};
