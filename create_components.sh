#!/bin/bash

# Create StatusBadge component
cat > frontend/src/components/shared/StatusBadge.tsx << 'EOF'
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
EOF

# Create TrafficVisualizer component
cat > frontend/src/components/shared/TrafficVisualizer.tsx << 'EOF'
'use client';

import React, { useState, useEffect } from 'react';

export const TrafficVisualizer: React.FC = () => {
  const [bars, setBars] = useState(() => Array(30).fill(20));

  useEffect(() => {
    const interval = setInterval(() => {
      setBars(prev => prev.map(() => Math.floor(Math.random() * 80) + 10));
    }, 800);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex items-end gap-[2px] h-16 w-full opacity-60">
      {bars.map((height, i) => (
        <div 
          key={i} 
          className="flex-1 bg-emerald-500/40 rounded-t-sm transition-all duration-700 ease-in-out hover:bg-emerald-400"
          style={{ height: `${height}%` }}
        />
      ))}
    </div>
  );
};
EOF

echo "Shared components created successfully"
