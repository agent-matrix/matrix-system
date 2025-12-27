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
