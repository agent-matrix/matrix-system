import React, { ReactNode } from 'react';
import { LucideIcon } from 'lucide-react';

interface CardProps {
  children: ReactNode;
  className?: string;
  title?: string;
  icon?: LucideIcon;
  action?: ReactNode;
}

export const Card: React.FC<CardProps> = ({ children, className = "", title, icon: Icon, action }) => (
  <div className={`relative bg-zinc-900/60 backdrop-blur-md border border-white/5 rounded-xl overflow-hidden flex flex-col group ${className}`}>
    <div className="absolute inset-0 bg-gradient-to-br from-emerald-500/5 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none" />
    
    {(title || Icon) && (
      <div className="flex items-center justify-between p-4 border-b border-white/5 bg-white/[0.02]">
        <div className="flex items-center gap-2 text-zinc-300 font-medium tracking-wide">
          {Icon && <Icon size={16} className="text-emerald-400" />}
          <span className="font-sans text-sm uppercase tracking-wider opacity-80">{title}</span>
        </div>
        {action}
      </div>
    )}
    <div className="p-4 flex-1 relative z-10">
      {children}
    </div>
  </div>
);
