"use client";

import React, { useState, useEffect, useRef } from 'react';
import {
  Activity, ShieldCheck, Server, Terminal, FileText, LogOut, Cpu, Zap,
  AlertTriangle, CheckCircle, XCircle, Globe, Clock, LayoutDashboard, Menu, X,
  Search, Share2, Database, Lock, BrainCircuit, Network, Bot, Play, Square,
  MessageSquare, GitBranch, TerminalSquare, Settings, Radar, ChevronRight,
  Eye, EyeOff, RefreshCw
} from 'lucide-react';

/** MATRIX ENTERPRISE SYSTEM - FULL IMPLEMENTATION */

const MOCK_SERVICES = [
  { id: 'MTX-HUB', name: 'Matrix Hub', version: 'v1.4.2', uptime: '14d 02h', status: 'ONLINE', latency: 24, type: 'CORE' },
  { id: 'MTX-AI', name: 'Matrix AI Cortex', version: 'v2.1.0', uptime: '02d 05h', status: 'ONLINE', latency: 142, type: 'AI' },
  { id: 'MTX-GRD', name: 'Guardian Core', version: 'v1.1.0', uptime: '14d 02h', status: 'ONLINE', latency: 12, type: 'SEC' },
  { id: 'DB-SHD', name: 'DB Shard 01', version: 'v15.2', uptime: '45d 01h', status: 'ONLINE', latency: 8, type: 'DB' },
  { id: 'AUTH-GT', name: 'Auth Gateway', version: 'v1.0.1', uptime: '01h 30m', status: 'DEGRADED', latency: 450, type: 'GATE' },
];

const TOPOLOGY_LINKS = [
  { source: 'AUTH-GT', target: 'MTX-HUB' },
  { source: 'MTX-HUB', target: 'MTX-AI' },
  { source: 'MTX-HUB', target: 'MTX-GRD' },
  { source: 'MTX-HUB', target: 'DB-SHD' },
  { source: 'MTX-AI', target: 'DB-SHD' },
];

const MOCK_LOGS = [
  { id: 1, type: 'INFO', source: 'MTX-HUB', msg: 'Health check passed successfully.' },
  { id: 2, type: 'WARN', source: 'AUTH-GT', msg: 'Latency spike detected in region: us-east-1.' },
  { id: 3, type: 'INFO', source: 'MTX-AI', msg: 'Neural weights optimized. Model version: 2.1.0' },
  { id: 4, type: 'SUCCESS', source: 'MTX-GRD', msg: 'Threat neutralized: IP 192.168.X.X blocked.' },
  { id: 5, type: 'ERROR', source: 'AUTH-GT', msg: 'Token validation timeout (5001ms).' },
  { id: 6, type: 'INFO', source: 'DB-SHD', msg: 'Vacuum complete. Index optimized.' },
];

const MOCK_PROPOSALS = [
  { id: 'PR-1024', type: 'LKG_PIN', risk: 'HIGH', desc: 'Version 1.2.4 failing checks. Rollback to 1.2.3.', status: 'PENDING' },
  { id: 'PR-1025', type: 'SCALE', risk: 'LOW', desc: 'Latency spike in AI Cortex. Scaling +2 replicas.', status: 'PENDING' },
];

const StatusBadge = ({ status }) => {
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
    <span className={\`px-2 py-1 rounded text-xs font-mono font-medium border flex items-center gap-2 w-fit \${styles[status] || styles.OFFLINE}\`}>
      <span className={\`w-1.5 h-1.5 rounded-full animate-pulse \${dotStyles[status] || dotStyles.OFFLINE}\`} />
      {status}
    </span>
  );
};

const Card = ({ children, className = "", title, icon: Icon, action }) => (
  <div className={\`relative bg-zinc-900/60 backdrop-blur-md border border-white/5 rounded-xl overflow-hidden flex flex-col group \${className}\`}>
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
        <div key={i} className="flex-1 bg-emerald-500/40 rounded-t-sm transition-all duration-700 ease-in-out hover:bg-emerald-400" style={{ height: \`\${height}%\` }} />
      ))}
    </div>
  );
};

export default function App() {
  const [activeView, setActiveView] = useState('dashboard');
  const [healthScore, setHealthScore] = useState(98.4);
  const [logs, setLogs] = useState(MOCK_LOGS);
  const [proposals, setProposals] = useState(MOCK_PROPOSALS);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => setTime(new Date()), 1000);
    const healthTimer = setInterval(() => {
      setHealthScore(prev => +(prev + (Math.random() * 0.4 - 0.2)).toFixed(1));
    }, 2000);
    return () => { clearInterval(timer); clearInterval(healthTimer); };
  }, []);

  const navItems = [
    { id: 'dashboard', label: 'Command Center', icon: LayoutDashboard },
    { id: 'assistant', label: 'Assistant', icon: Bot },
    { id: 'guardian', label: 'Guardian', icon: ShieldCheck },
    { id: 'services', label: 'Services', icon: Server },
    { id: 'docs', label: 'Documentation', icon: FileText },
  ];

  return (
    <div className="min-h-screen bg-black text-zinc-100 font-sans selection:bg-emerald-500/30 overflow-hidden flex relative">
      <div className="fixed inset-0 z-0 pointer-events-none">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-emerald-500/5 blur-[120px]" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-indigo-500/5 blur-[120px]" />
      </div>

      <aside className={\`fixed inset-y-0 left-0 z-50 w-64 bg-black/80 backdrop-blur-xl border-r border-white/5 transform transition-transform duration-300 ease-in-out \${sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}\`}>
        <div className="h-full flex flex-col">
          <div className="h-16 flex items-center px-6 border-b border-white/5">
            <div className="w-3 h-3 bg-emerald-500 rounded-sm animate-pulse mr-3 shadow-[0_0_10px_rgba(16,185,129,0.5)]"></div>
            <span className="font-bold text-lg tracking-widest text-white">MATRIX<span className="text-zinc-500">SYS</span></span>
          </div>
          <nav className="flex-1 p-4 space-y-1">
            {navItems.map((item) => (
              <button key={item.id} onClick={() => { setActiveView(item.id); setSidebarOpen(false); }}
                className={\`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-all duration-200 group \${activeView === item.id ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'text-zinc-400 hover:bg-white/5 hover:text-white border border-transparent'}\`}>
                <item.icon size={18} />
                {item.label}
                {activeView === item.id && <div className="ml-auto w-1.5 h-1.5 rounded-full bg-emerald-400" />}
              </button>
            ))}
          </nav>
          <div className="p-4 border-t border-white/5 flex items-center gap-3">
            <div className="w-8 h-8 rounded bg-gradient-to-tr from-emerald-500 to-cyan-500 flex items-center justify-center text-black font-bold text-xs">RM</div>
            <div className="flex-1">
              <div className="text-sm font-medium">Ruslan Magana</div>
              <div className="text-xs text-zinc-500">SYS_ADMIN_L5</div>
            </div>
          </div>
        </div>
      </aside>

      <div className="flex-1 flex flex-col lg:pl-64 h-screen relative z-10">
        <header className="h-16 flex items-center justify-between px-6 border-b border-white/5 bg-black/20 backdrop-blur-sm">
          <div className="flex items-center gap-4">
            <button onClick={() => setSidebarOpen(true)} className="lg:hidden text-zinc-400"><Menu size={24} /></button>
            <div className="hidden md:flex items-center gap-2 text-xs font-mono text-zinc-500">
              <span className="text-emerald-500">●</span><span>SYSTEM ONLINE</span>
            </div>
          </div>
          <div className="flex items-center gap-2 font-mono text-sm text-zinc-400 bg-white/5 px-3 py-1 rounded">
            <Clock size={14} className="text-emerald-500" />
            <span>{time.toLocaleTimeString()}</span>
          </div>
        </header>

        <main className="flex-1 overflow-y-auto p-8">
          <div className="max-w-7xl mx-auto">
            {activeView === 'dashboard' && (
              <div className="space-y-6">
                <Card title="System Health" icon={Activity}>
                  <div className="flex items-center gap-6">
                    <div className="text-6xl font-bold text-emerald-400">{healthScore.toFixed(1)}%</div>
                    <TrafficVisualizer />
                  </div>
                </Card>
                <Card title="System Logs" icon={Terminal}>
                  <div className="font-mono text-xs space-y-1">
                    {logs.map((log) => (
                      <div key={log.id} className="flex gap-2">
                        <span className={\`font-bold \${log.type === 'ERROR' ? 'text-rose-500' : log.type === 'WARN' ? 'text-amber-500' : 'text-emerald-400'}\`}>{log.type}</span>
                        <span className="text-zinc-400">{log.source}</span>
                        <span className="text-zinc-300">{log.msg}</span>
                      </div>
                    ))}
                  </div>
                </Card>
              </div>
            )}
            {activeView === 'assistant' && <div className="text-center text-zinc-500 py-20">AI Assistant View - Coming Soon</div>}
            {activeView === 'guardian' && <div className="text-center text-zinc-500 py-20">Guardian Security View - Coming Soon</div>}
            {activeView === 'services' && (
              <div className="grid grid-cols-3 gap-6">
                {MOCK_SERVICES.map(svc => (
                  <Card key={svc.id}>
                    <div className="flex justify-between mb-4">
                      <Server className="text-emerald-400" />
                      <StatusBadge status={svc.status} />
                    </div>
                    <h3 className="text-lg font-bold">{svc.name}</h3>
                    <p className="text-xs text-zinc-500">{svc.id} • {svc.version}</p>
                  </Card>
                ))}
              </div>
            )}
            {activeView === 'docs' && <Card title="Documentation" icon={FileText}><div className="text-zinc-400">System documentation and API reference...</div></Card>}
          </div>
        </main>
      </div>
    </div>
  );
}
