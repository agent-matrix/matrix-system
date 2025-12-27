import React from 'react';

interface StatusBadgeProps {
  status: 'ONLINE' | 'DEGRADED' | 'OFFLINE';
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status }) => {
  const styles = {
    ONLINE: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
    DEGRADED: 'bg-amber-500/10 text-amber-400 border-amber-500/20',
    OFFLINE: 'bg-rose-500/10 text-rose-400 border-rose-500/20',
  };
  const dotStyles = {
    ONLINE: 'bg-emerald-400',
    DEGRADED: 'bg-amber-400',
    OFFLINE: 'bg-rose-400',
  };

  return (
    <span className={`px-2 py-1 rounded text-xs font-mono font-medium border flex items-center gap-2 w-fit ${styles[status] || styles.OFFLINE}`}>
      <span className={`w-1.5 h-1.5 rounded-full animate-pulse ${dotStyles[status] || dotStyles.OFFLINE}`} />
      {status}
    </span>
  );
};
