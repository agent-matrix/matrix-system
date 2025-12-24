"use client";

import React, { useState, useEffect, useRef } from 'react';

// --- Types ---
type ViewState = 'DASHBOARD' | 'GUARDIAN' | 'SERVICES' | 'DOCS';
type LogType = 'INFO' | 'WARN' | 'CRIT';

interface LogEntry {
  id: number;
  time: string;
  type: LogType;
  message: string;
}

// --- Main Component ---
export default function MatrixAdmin() {
  const [currentView, setCurrentView] = useState<ViewState>('DASHBOARD');
  const [clock, setClock] = useState('00:00:00');
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [integrity, setIntegrity] = useState(98.4);

  // Matrix Rain Canvas Ref
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const logEndRef = useRef<HTMLDivElement>(null);

  // --- Effects ---

  // 1. Clock
  useEffect(() => {
    const timer = setInterval(() => {
      setClock(new Date().toISOString().split('T')[1].split('.')[0]);
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  // 2. Simulated Integrity Fluctuation
  useEffect(() => {
    const timer = setInterval(() => {
      const fluctuation = (Math.random() * 2 - 1);
      setIntegrity(prev => Math.min(100, Math.max(90, prev + fluctuation)));
    }, 2000);
    return () => clearInterval(timer);
  }, []);

  // 3. Simulated Logs
  useEffect(() => {
    const processes = ['MATRIX_HUB', 'MATRIX_AI', 'GUARDIAN', 'AUTH_GATE'];
    const actions = ['Health OK', 'Token Refreshed', 'Scanning...', 'Sync Complete'];

    const addLog = () => {
      const type: LogType = Math.random() > 0.95 ? 'CRIT' : Math.random() > 0.85 ? 'WARN' : 'INFO';
      const msg = `${processes[Math.floor(Math.random() * processes.length)]}: ${actions[Math.floor(Math.random() * actions.length)]}`;

      setLogs(prev => {
        const newLogs = [...prev, {
          id: Date.now(),
          time: new Date().toISOString().split('T')[1].split('.')[0],
          type,
          message: msg
        }];
        return newLogs.slice(-50); // Keep last 50
      });
    };

    // Initial fill
    for(let i=0; i<5; i++) addLog();

    const timer = setInterval(addLog, 2500);
    return () => clearInterval(timer);
  }, []);

  // 4. Auto-scroll logs
  useEffect(() => {
    logEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [logs]);

  // 5. Matrix Rain Effect
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789アァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピ';
    const fontSize = 14;
    const columns = canvas.width / fontSize;
    const drops: number[] = new Array(Math.floor(columns)).fill(1);

    const draw = () => {
      ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      ctx.fillStyle = '#0F0';
      ctx.font = `${fontSize}px monospace`;

      for (let i = 0; i < drops.length; i++) {
        const text = chars[Math.floor(Math.random() * chars.length)];
        ctx.fillText(text, i * fontSize, drops[i] * fontSize);

        if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
          drops[i] = 0;
        }
        drops[i]++;
      }
    };

    const interval = setInterval(draw, 33);
    const handleResize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };

    window.addEventListener('resize', handleResize);
    return () => {
      clearInterval(interval);
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  // --- Handlers ---
  const handleLogout = () => {
    if (confirm("DISCONNECT CARRIER SIGNAL?")) {
      window.location.reload();
    }
  };

  return (
    <div className="relative w-screen h-screen overflow-hidden bg-black text-[#00FF41] font-mono uppercase">

      {/* Background & Overlay */}
      <canvas ref={canvasRef} className="fixed top-0 left-0 w-full h-full opacity-30 z-0" />
      <div className="crt-overlay" />

      {/* Main Grid Layout */}
      <div className="relative z-10 grid grid-cols-[260px_1fr] grid-rows-[70px_1fr] gap-5 p-5 h-full">

        {/* Header */}
        <header className="col-span-2 flex justify-between items-center border-b-2 border-[#00FF41] bg-glass px-5 border-glow">
          <div className="flex items-center gap-4">
            <h1 className="text-2xl font-bold tracking-widest text-glow">[ MATRIX SYSTEM ]</h1>
            <span className="text-xs opacity-70">SDK v0.1.0</span>
          </div>
          <div className="text-right text-sm">
            <div>OPERATOR: <span className="font-bold text-glow">RUSLAN MAGANA</span></div>
            <div className="text-[10px] opacity-80">SESSION: 8X-2991</div>
            <div>{clock} UTC</div>
          </div>
        </header>

        {/* Sidebar */}
        <aside className="bg-glass border border-[#00FF41] border-glow flex flex-col py-5">
          <NavItem active={currentView === 'DASHBOARD'} onClick={() => setCurrentView('DASHBOARD')} label="DASHBOARD" />
          <NavItem active={currentView === 'GUARDIAN'} onClick={() => setCurrentView('GUARDIAN')} label="GUARDIAN" />
          <NavItem active={currentView === 'SERVICES'} onClick={() => setCurrentView('SERVICES')} label="SERVICES" />
          <div className="h-px bg-[#00FF41] opacity-50 my-4 mx-5" />
          <NavItem active={currentView === 'DOCS'} onClick={() => setCurrentView('DOCS')} label="DOCS" />
          <NavItem active={false} onClick={handleLogout} label="LOGOUT" />
        </aside>

        {/* Main Content Area */}
        <main className="overflow-y-auto pb-5">

          {/* VIEW: DASHBOARD */}
          {currentView === 'DASHBOARD' && (
            <div className="grid grid-cols-3 grid-rows-2 gap-5 h-full animate-fade-in">

              {/* Card: System Integrity */}
              <Card>
                <CardHeader title="SYSTEM_INTEGRITY" badge="LIVE" />
                <div className="flex flex-col items-center justify-center h-full">
                  <div className="text-6xl font-bold text-glow mb-4">{integrity.toFixed(1)}%</div>
                  <div className="text-[10px]">HUB: OK | AI: OK | GUARDIAN: OK</div>
                </div>
              </Card>

              {/* Card: Traffic (Visualizer) */}
              <Card className="col-span-2">
                <CardHeader title="NEURAL_TRAFFIC" right="TPS: 1,024" />
                <div className="flex items-end gap-1 h-full pt-4 opacity-80">
                   {Array.from({ length: 40 }).map((_, i) => (
                     <div key={i} className="flex-1 bg-[#00FF41] animate-pulse" style={{
                       height: `${Math.random() * 80 + 20}%`,
                       animationDuration: `${Math.random() * 1000 + 500}ms`
                     }} />
                   ))}
                </div>
              </Card>

              {/* Card: Logs */}
              <Card className="col-span-2 text-xs">
                <CardHeader title="GUARDIAN_LOGS" right="TAIL -F" />
                <div className="flex-1 overflow-y-auto text-[#ccffcc] space-y-1 h-48">
                  {logs.map((log) => (
                    <div key={log.id}>
                      <span className="opacity-70 mr-2">{log.time}</span>
                      {log.type === 'CRIT' ? <span className="text-red-500 text-glow">[CRIT]</span> :
                       log.type === 'WARN' ? <span className="text-yellow-500">[WARN]</span> :
                       <span className="text-[#00FF41]">[OK]</span>}
                      {' '}{log.message}
                    </div>
                  ))}
                  <div ref={logEndRef} />
                </div>
              </Card>

              {/* Card: Proposals */}
              <Card>
                <CardHeader title="PROPOSALS" right="2 PENDING" rightColor="text-yellow-400" />
                <div className="space-y-3 overflow-y-auto">
                  <ProposalItem id="PR-1024" type="LKG_PIN" risk="HIGH" desc="Version 1.2.4 failing checks." />
                  <ProposalItem id="PR-1025" type="SCALE" risk="LOW" desc="Latency spike in Matrix-AI." />
                </div>
              </Card>
            </div>
          )}

          {/* VIEW: GUARDIAN */}
          {currentView === 'GUARDIAN' && (
            <div className="grid grid-cols-1 gap-5 h-full animate-fade-in">
              <Card className="h-64">
                <CardHeader title="THREAT_DETECTION_MAP" right="GLOBAL_SCOPE" />
                <div className="flex items-center justify-center h-full border border-[#00FF41] m-4 opacity-50 relative">
                  [ GEO-MAP RENDER PLACEHOLDER ]
                  <div className="absolute top-1/4 left-1/4 text-red-500 animate-blink">X</div>
                  <div className="absolute top-3/4 left-3/4 text-red-500 animate-blink">X</div>
                </div>
              </Card>
              <Card className="flex-1">
                <CardHeader title="ACCESS_LOGS" />
                <div className="p-2 text-xs text-[#ccffcc]">
                  <p>12:00:01 - ADMIN ACCESS GRANTED - IP 192.168.1.10</p>
                  <p>12:00:05 - PROBE BLOCKED - PORT 8080</p>
                  <p>12:01:22 - SERVICE SYNC - MATRIX HUB</p>
                </div>
              </Card>
            </div>
          )}

          {/* VIEW: SERVICES */}
          {currentView === 'SERVICES' && (
            <div className="h-full animate-fade-in">
              <Card className="h-full">
                <CardHeader title="MICROSERVICES_REGISTRY" right="CLUSTER: ZION-1" />
                <table className="w-full text-left border-collapse mt-4">
                  <thead>
                    <tr className="border-b-2 border-[#003B00] text-white">
                      <th className="p-3">SERVICE ID</th>
                      <th className="p-3">ENDPOINT</th>
                      <th className="p-3">VERSION</th>
                      <th className="p-3">STATUS</th>
                    </tr>
                  </thead>
                  <tbody className="text-sm">
                    <ServiceRow id="MATRIX-HUB" url="api.matrixhub.io" ver="v1.2.3" status="ONLINE" />
                    <ServiceRow id="MATRIX-AI" url="ai.internal" ver="v2.0.0" status="ONLINE" />
                    <ServiceRow id="GUARDIAN-CORE" url="sec.internal" ver="v1.1.0" status="ONLINE" />
                    <ServiceRow id="AUTH-GATE" url="auth.internal" ver="v1.0.1" status="DEGRADED" />
                  </tbody>
                </table>
              </Card>
            </div>
          )}

          {/* VIEW: DOCS */}
          {currentView === 'DOCS' && (
             <Card className="h-full animate-fade-in overflow-y-auto">
               <div className="p-5 leading-relaxed text-[#ccffcc] max-w-4xl">
                 <h1 className="text-xl font-bold border-b-2 border-[#00FF41] mb-4 pb-2">{'// SYSTEM DOCUMENTATION'}</h1>
                 <p className="mb-4"><strong>CLASSIFIED: LEVEL 5</strong></p>

                 <h3 className="text-lg font-bold mt-6 mb-2">1. OVERVIEW</h3>
                 <p>The Matrix System is a production-ready Python SDK and CLI for the Agent-Matrix ecosystem. It provides self-healing, policy-governed capabilities.</p>

                 <h3 className="text-lg font-bold mt-6 mb-2">2. CLI COMMANDS</h3>
                 <code className="block bg-[#003B00] p-2 mb-2">{`> matrix health --service all`}</code>
                 <code className="block bg-[#003B00] p-2 mb-2">{`> matrix proposals --state pending`}</code>

                 <h3 className="text-lg font-bold mt-6 mb-2">3. HITL GOVERNANCE</h3>
                 <p>Operators must approve all high-risk remediation plans generated by the AI. Use the Dashboard to review PRs.</p>
               </div>
             </Card>
          )}

        </main>
      </div>
    </div>
  );
}

// --- Sub Components ---

const NavItem = ({ label, active, onClick }: { label: string, active: boolean, onClick: () => void }) => (
  <div
    onClick={onClick}
    className={`
      flex items-center gap-2 px-5 py-4 cursor-pointer transition-all border-l-4
      ${active ? 'bg-[#003B00] border-[#00FF41] text-glow pl-6' : 'border-transparent hover:bg-[#001a00] hover:pl-6 hover:text-white'}
    `}
  >
    <span>&gt;</span>
    <span>{label}</span>
  </div>
);

const Card = ({ children, className = '' }: { children: React.ReactNode, className?: string }) => (
  <div className={`relative flex flex-col bg-glass border border-[#00FF41] p-5 ${className}`}>
    {/* Decorative corners */}
    <div className="absolute top-0 left-0 w-2.5 h-2.5 border-t-2 border-l-2 border-[#00FF41]" />
    <div className="absolute bottom-0 right-0 w-2.5 h-2.5 border-b-2 border-r-2 border-[#00FF41]" />
    {children}
  </div>
);

const CardHeader = ({ title, badge, right, rightColor }: { title: string, badge?: string, right?: string, rightColor?: string }) => (
  <div className="flex justify-between items-center border-b border-[#003B00] pb-2 mb-4 text-lg">
    <span>{title}</span>
    {badge && <span className="bg-[#00FF41] text-black text-xs font-bold px-2 py-1 animate-pulse">{badge}</span>}
    {right && <span className={`text-sm ${rightColor || ''}`}>{right}</span>}
  </div>
);

const ProposalItem = ({ id, type, risk, desc }: { id: string, type: string, risk: string, desc: string }) => {
  const [status, setStatus] = useState<'PENDING' | 'APPROVED' | 'REJECTED'>('PENDING');

  if (status !== 'PENDING') return null;

  return (
    <div className="border border-[#005500] bg-[rgba(0,0,0,0.5)] p-3 hover:border-[#00FF41] transition-colors">
      <div className="flex justify-between mb-1">
        <span className="text-white font-bold">{id} [{type}]</span>
        <span className={risk === 'HIGH' ? 'text-red-500' : 'text-[#00FF41]'}>RISK: {risk}</span>
      </div>
      <p className="text-[10px] opacity-80 mb-2">{desc}</p>
      <div className="flex gap-2">
        <button
          onClick={() => setStatus('APPROVED')}
          className="flex-1 border border-[#00FF41] text-[#00FF41] text-xs py-1 hover:bg-[#00FF41] hover:text-black transition-all"
        >
          [ ACCEPT ]
        </button>
        <button
          onClick={() => setStatus('REJECTED')}
          className="flex-1 border border-red-500 text-red-500 text-xs py-1 hover:bg-red-500 hover:text-black transition-all"
        >
          [ REJECT ]
        </button>
      </div>
    </div>
  );
};

const ServiceRow = ({ id, url, ver, status }: { id: string, url: string, ver: string, status: string }) => (
  <tr className="border-b border-[#002200] hover:bg-[#001a00]">
    <td className="p-3">{id}</td>
    <td className="p-3 opacity-70">{url}</td>
    <td className="p-3">{ver}</td>
    <td className={`p-3 ${status === 'ONLINE' ? 'text-[#00FF41]' : 'text-yellow-500'}`}>{status}</td>
  </tr>
);
