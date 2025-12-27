"use client";

import React, { useState, useEffect, useRef } from 'react';
import {
  Activity,
  ShieldCheck,
  Server,
  Terminal,
  FileText,
  LogOut,
  Cpu,
  Zap,
  AlertTriangle,
  CheckCircle,
  XCircle,
  Globe,
  Clock,
  LayoutDashboard,
  Menu,
  X,
  Search,
  Share2,
  Database,
  Lock,
  BrainCircuit,
  Network,
  Bot,
  Play,
  Square,
  MessageSquare,
  GitBranch,
  TerminalSquare,
  Settings,
  Radar,
  ChevronRight,
  Eye,
  EyeOff,
  RefreshCw
} from 'lucide-react';

/**
 * MATRIX ENTERPRISE SYSTEM // UI CORE
 * A production-ready, self-healing interface for the Agent-Matrix ecosystem.
 * Integrated with superintelligence backend for autonomous operations.
 */

// --- UTILITIES & MOCK DATA ---

const MOCK_SERVICES = [
  { id: 'MTX-HUB', name: 'Matrix Hub', version: 'v1.4.2', uptime: '14d 02h', status: 'ONLINE' as const, latency: 24, type: 'CORE' as const },
  { id: 'MTX-AI', name: 'Matrix AI Cortex', version: 'v2.1.0', uptime: '02d 05h', status: 'ONLINE' as const, latency: 142, type: 'AI' as const },
  { id: 'MTX-GRD', name: 'Guardian Core', version: 'v1.1.0', uptime: '14d 02h', status: 'ONLINE' as const, latency: 12, type: 'SEC' as const },
  { id: 'DB-SHD', name: 'DB Shard 01', version: 'v15.2', uptime: '45d 01h', status: 'ONLINE' as const, latency: 8, type: 'DB' as const },
  { id: 'AUTH-GT', name: 'Auth Gateway', version: 'v1.0.1', uptime: '01h 30m', status: 'DEGRADED' as const, latency: 450, type: 'GATE' as const },
];

const TOPOLOGY_LINKS = [
  { source: 'AUTH-GT', target: 'MTX-HUB' },
  { source: 'MTX-HUB', target: 'MTX-AI' },
  { source: 'MTX-HUB', target: 'MTX-GRD' },
  { source: 'MTX-HUB', target: 'DB-SHD' },
  { source: 'MTX-AI', target: 'DB-SHD' },
];

const MOCK_LOGS = [
  { id: 1, type: 'INFO' as const, source: 'MTX-HUB', msg: 'Health check passed successfully.' },
  { id: 2, type: 'WARN' as const, source: 'AUTH-GT', msg: 'Latency spike detected in region: us-east-1.' },
  { id: 3, type: 'INFO' as const, source: 'MTX-AI', msg: 'Neural weights optimized. Model version: 2.1.0' },
  { id: 4, type: 'SUCCESS' as const, source: 'MTX-GRD', msg: 'Threat neutralized: IP 192.168.X.X blocked.' },
  { id: 5, type: 'ERROR' as const, source: 'AUTH-GT', msg: 'Token validation timeout (5001ms).' },
  { id: 6, type: 'INFO' as const, source: 'DB-SHD', msg: 'Vacuum complete. Index optimized.' },
];

const MOCK_PROPOSALS = [
  { id: 'PR-1024', type: 'LKG_PIN', risk: 'HIGH' as const, desc: 'Version 1.2.4 failing checks. Rollback to 1.2.3.', status: 'PENDING' as const },
  { id: 'PR-1025', type: 'SCALE', risk: 'LOW' as const, desc: 'Latency spike in AI Cortex. Scaling +2 replicas.', status: 'PENDING' as const },
];

type StatusType = 'ONLINE' | 'DEGRADED' | 'OFFLINE';
type ServiceType = 'CORE' | 'AI' | 'SEC' | 'DB' | 'GATE';
type LogType = 'INFO' | 'WARN' | 'ERROR' | 'SUCCESS' | 'CRIT';
type RiskType = 'HIGH' | 'LOW' | 'MEDIUM';

interface ServiceInfo {
  id: string;
  name: string;
  version: string;
  uptime: string;
  status: StatusType;
  latency: number;
  type: ServiceType;
}

interface TopologyLink {
  source: string;
  target: string;
}

interface LogEntry {
  id: number;
  type: LogType;
  source: string;
  msg: string;
  time?: string;
  message?: string;
}

interface ProposalData {
  id: string;
  type: string;
  risk: RiskType;
  desc: string;
  status: 'PENDING' | 'APPROVED' | 'REJECTED';
}

interface AutoLogEntry {
  id: number;
  time: string;
  message: string;
  type: 'SCAN' | 'MAINT' | 'SEC' | 'HEALTH' | 'SYNC';
  status: string;
}

interface AssistantPlan {
  summary: string;
  steps: Array<{
    step_number: number;
    summary: string;
    status?: string;
  }>;
}

interface AssistantMessageData {
  from: 'user' | 'ai';
  text?: string;
  answer?: string;
  plan?: AssistantPlan;
  executionLog?: AssistantPlan;
}

// --- COMPONENTS ---

const StatusBadge = ({ status }: { status: StatusType }) => {
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

interface CardProps {
  children: React.ReactNode;
  className?: string;
  title?: string;
  icon?: React.ElementType;
  action?: React.ReactNode;
}

const Card = ({ children, className = "", title, icon: Icon, action }: CardProps) => (
  <div className={`relative bg-zinc-900/60 backdrop-blur-md border border-white/5 rounded-xl overflow-hidden flex flex-col group ${className}`}>
    {/* Animated Border Gradient on Hover */}
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

const TrafficVisualizer = () => {
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

// [CONTINUING IN NEXT MESSAGE DUE TO LENGTH LIMIT...]
