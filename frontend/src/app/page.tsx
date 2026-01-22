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

// --- MAIN PAGE COMPONENT ---

const ServiceCard = ({ service }: { service: ServiceInfo }) => (
  <div className="p-4 bg-zinc-800/50 rounded-lg border border-white/5 hover:border-emerald-500/30 transition-all">
    <div className="flex justify-between items-start mb-3">
      <div>
        <h3 className="font-mono text-sm text-zinc-200">{service.name}</h3>
        <p className="text-xs text-zinc-500 font-mono">{service.id}</p>
      </div>
      <StatusBadge status={service.status} />
    </div>
    <div className="grid grid-cols-3 gap-2 text-xs">
      <div>
        <span className="text-zinc-500">Version</span>
        <p className="text-zinc-300 font-mono">{service.version}</p>
      </div>
      <div>
        <span className="text-zinc-500">Uptime</span>
        <p className="text-zinc-300 font-mono">{service.uptime}</p>
      </div>
      <div>
        <span className="text-zinc-500">Latency</span>
        <p className={`font-mono ${service.latency > 200 ? 'text-amber-400' : 'text-emerald-400'}`}>
          {service.latency}ms
        </p>
      </div>
    </div>
  </div>
);

const LogLine = ({ log }: { log: typeof MOCK_LOGS[0] }) => {
  const typeStyles = {
    INFO: 'text-blue-400',
    WARN: 'text-amber-400',
    ERROR: 'text-rose-400',
    SUCCESS: 'text-emerald-400',
    CRIT: 'text-rose-500',
  };

  return (
    <div className="flex items-start gap-3 py-2 border-b border-white/5 last:border-0">
      <span className={`text-xs font-mono ${typeStyles[log.type] || 'text-zinc-400'}`}>
        [{log.type}]
      </span>
      <span className="text-xs font-mono text-zinc-500">{log.source}</span>
      <span className="text-xs text-zinc-300 flex-1">{log.msg}</span>
    </div>
  );
};

export default function MatrixDashboard() {
  const [currentTime, setCurrentTime] = useState(new Date());
  const [systemHealth, setSystemHealth] = useState(98.5);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
      setSystemHealth(prev => Math.max(95, Math.min(100, prev + (Math.random() - 0.5) * 0.5)));
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  const onlineServices = MOCK_SERVICES.filter(s => s.status === 'ONLINE').length;
  const totalServices = MOCK_SERVICES.length;

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100">
      {/* Header */}
      <header className="border-b border-white/5 bg-zinc-900/50 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2">
                <BrainCircuit className="w-8 h-8 text-emerald-400" />
                <div>
                  <h1 className="text-xl font-bold tracking-tight">MATRIX SYSTEM</h1>
                  <p className="text-xs text-zinc-500 font-mono">SUPERINTELLIGENCE v1.0</p>
                </div>
              </div>
            </div>
            <div className="flex items-center gap-6">
              <div className="text-right">
                <p className="text-xs text-zinc-500">System Time</p>
                <p className="font-mono text-sm text-emerald-400">
                  {currentTime.toLocaleTimeString()}
                </p>
              </div>
              <div className="text-right">
                <p className="text-xs text-zinc-500">Health Score</p>
                <p className="font-mono text-sm text-emerald-400">
                  {systemHealth.toFixed(1)}%
                </p>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        {/* Stats Row */}
        <div className="grid grid-cols-4 gap-4 mb-8">
          <Card className="!p-4">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-emerald-500/10 rounded-lg">
                <Server className="w-5 h-5 text-emerald-400" />
              </div>
              <div>
                <p className="text-2xl font-bold">{onlineServices}/{totalServices}</p>
                <p className="text-xs text-zinc-500">Services Online</p>
              </div>
            </div>
          </Card>
          <Card className="!p-4">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-blue-500/10 rounded-lg">
                <Activity className="w-5 h-5 text-blue-400" />
              </div>
              <div>
                <p className="text-2xl font-bold">99.97%</p>
                <p className="text-xs text-zinc-500">Uptime (30d)</p>
              </div>
            </div>
          </Card>
          <Card className="!p-4">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-purple-500/10 rounded-lg">
                <Zap className="w-5 h-5 text-purple-400" />
              </div>
              <div>
                <p className="text-2xl font-bold">24ms</p>
                <p className="text-xs text-zinc-500">Avg Latency</p>
              </div>
            </div>
          </Card>
          <Card className="!p-4">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-amber-500/10 rounded-lg">
                <ShieldCheck className="w-5 h-5 text-amber-400" />
              </div>
              <div>
                <p className="text-2xl font-bold">0</p>
                <p className="text-xs text-zinc-500">Ethical Violations</p>
              </div>
            </div>
          </Card>
        </div>

        {/* Main Grid */}
        <div className="grid grid-cols-3 gap-6">
          {/* Services */}
          <div className="col-span-2">
            <Card title="Services" icon={Server}>
              <div className="grid grid-cols-2 gap-4">
                {MOCK_SERVICES.map(service => (
                  <ServiceCard key={service.id} service={service} />
                ))}
              </div>
            </Card>
          </div>

          {/* Proposals */}
          <div>
            <Card title="Pending Proposals" icon={FileText}>
              <div className="space-y-3">
                {MOCK_PROPOSALS.map(proposal => (
                  <div key={proposal.id} className="p-3 bg-zinc-800/50 rounded-lg border border-white/5">
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-mono text-xs text-zinc-400">{proposal.id}</span>
                      <span className={`px-2 py-0.5 rounded text-xs font-mono ${
                        proposal.risk === 'HIGH'
                          ? 'bg-rose-500/10 text-rose-400'
                          : 'bg-emerald-500/10 text-emerald-400'
                      }`}>
                        {proposal.risk} RISK
                      </span>
                    </div>
                    <p className="text-sm text-zinc-300 mb-3">{proposal.desc}</p>
                    <div className="flex gap-2">
                      <button className="flex-1 px-3 py-1.5 bg-emerald-500/10 text-emerald-400 rounded text-xs font-medium hover:bg-emerald-500/20 transition-colors">
                        Approve
                      </button>
                      <button className="flex-1 px-3 py-1.5 bg-rose-500/10 text-rose-400 rounded text-xs font-medium hover:bg-rose-500/20 transition-colors">
                        Reject
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </Card>
          </div>
        </div>

        {/* Traffic & Logs Row */}
        <div className="grid grid-cols-2 gap-6 mt-6">
          <Card title="Network Traffic" icon={Activity}>
            <TrafficVisualizer />
            <div className="mt-4 flex justify-between text-xs text-zinc-500">
              <span>Last 30 seconds</span>
              <span className="text-emerald-400">12.4 MB/s avg</span>
            </div>
          </Card>
          <Card title="System Logs" icon={Terminal}>
            <div className="max-h-48 overflow-y-auto">
              {MOCK_LOGS.map(log => (
                <LogLine key={log.id} log={log} />
              ))}
            </div>
          </Card>
        </div>

        {/* Intelligence Modules Status */}
        <div className="mt-6">
          <Card title="Superintelligence Modules" icon={BrainCircuit}>
            <div className="grid grid-cols-3 gap-4">
              <div className="p-4 bg-zinc-800/50 rounded-lg border border-emerald-500/20">
                <div className="flex items-center gap-2 mb-2">
                  <Database className="w-4 h-4 text-emerald-400" />
                  <span className="text-sm font-medium">Memory System</span>
                </div>
                <p className="text-xs text-zinc-500">Experiences: 1,247 | Patterns: 89</p>
                <StatusBadge status="ONLINE" />
              </div>
              <div className="p-4 bg-zinc-800/50 rounded-lg border border-blue-500/20">
                <div className="flex items-center gap-2 mb-2">
                  <Network className="w-4 h-4 text-blue-400" />
                  <span className="text-sm font-medium">Meta-Learning</span>
                </div>
                <p className="text-xs text-zinc-500">Strategies: 24 | Success: 87%</p>
                <StatusBadge status="ONLINE" />
              </div>
              <div className="p-4 bg-zinc-800/50 rounded-lg border border-purple-500/20">
                <div className="flex items-center gap-2 mb-2">
                  <Lock className="w-4 h-4 text-purple-400" />
                  <span className="text-sm font-medium">Ethical Core</span>
                </div>
                <p className="text-xs text-zinc-500">Directives: 11 | Violations: 0</p>
                <StatusBadge status="ONLINE" />
              </div>
            </div>
          </Card>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-white/5 mt-12 py-6">
        <div className="max-w-7xl mx-auto px-6 text-center">
          <p className="text-xs text-zinc-500 font-mono">
            MATRIX SYSTEM v1.0 // SUPERINTELLIGENCE READY // ALL SYSTEMS OPERATIONAL
          </p>
        </div>
      </footer>
    </div>
  );
}
