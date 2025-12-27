// Utility functions

export function classNames(...classes: (string | boolean | undefined)[]) {
  return classes.filter(Boolean).join(' ');
}

export function formatTimestamp(timestamp: string): string {
  return new Date(timestamp).toISOString().split('T')[1].split('.')[0];
}

export function getRiskColor(riskScore: number): string {
  if (riskScore >= 50) return 'text-red-500';
  if (riskScore >= 25) return 'text-yellow-500';
  return 'text-[#00FF41]';
}

export function getStatusColor(status: string): string {
  switch (status.toUpperCase()) {
    case 'ONLINE':
    case 'HEALTHY':
      return 'text-[#00FF41]';
    case 'DEGRADED':
      return 'text-yellow-500';
    case 'OFFLINE':
    case 'UNHEALTHY':
      return 'text-red-500';
    default:
      return 'text-gray-500';
  }
}

export function generateSessionId(): string {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
  let id = '';
  for (let i = 0; i < 2; i++) {
    id += chars[Math.floor(Math.random() * chars.length)];
  }
  id += 'X-';
  for (let i = 0; i < 4; i++) {
    id += Math.floor(Math.random() * 10);
  }
  return id;
}

export function generateId(): string {
  return Math.random().toString(36).substr(2, 9).toUpperCase();
}
