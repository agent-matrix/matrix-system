// Matrix System Types

export interface HealthCheckResponse {
  app_uid: string;
  check_type: string;
  result: string;
  status: 'HEALTHY' | 'DEGRADED' | 'UNHEALTHY';
  score: number;
  latency_ms: number;
  timestamp?: string;
}

export interface ServiceInfo {
  id: string;
  name: string;
  version: string;
  uptime: string;
  status: 'ONLINE' | 'DEGRADED' | 'OFFLINE';
  latency: number;
  type: 'CORE' | 'AI' | 'SEC' | 'DB' | 'GATE';
}

export interface TopologyLink {
  source: string;
  target: string;
}

export interface LogEntry {
  id: number;
  type: 'INFO' | 'WARN' | 'ERROR' | 'SUCCESS' | 'CRIT';
  source: string;
  msg: string;
  time?: string;
  message?: string;
}

export interface ProposalData {
  id: string;
  type: string;
  risk: 'HIGH' | 'LOW' | 'MEDIUM';
  desc: string;
  status: 'PENDING' | 'APPROVED' | 'REJECTED';
}

export interface AutoLogEntry {
  id: number;
  time: string;
  message: string;
  type: 'SCAN' | 'MAINT' | 'SEC' | 'HEALTH' | 'SYNC';
  status: string;
}

export interface AssistantPlan {
  summary: string;
  steps: Array<{
    step_number: number;
    summary: string;
    status?: string;
  }>;
}

export interface AssistantMessageData {
  from: 'user' | 'ai';
  text?: string;
  answer?: string;
  plan?: AssistantPlan;
  executionLog?: AssistantPlan;
}

export interface ProviderSettings {
  api_key?: string;
  model?: string;
  model_id?: string;
  project_id?: string;
  base_url?: string;
}

export interface SystemSettings {
  provider: string;
  providers: string[];
  openai: ProviderSettings;
  claude: ProviderSettings;
  watsonx: ProviderSettings;
  ollama: ProviderSettings;
}

export type ViewState = 'dashboard' | 'assistant' | 'guardian' | 'services' | 'docs';

// API Response Types
export interface EventLog {
  event_id: string;
  app_uid: string;
  event_type: string;
  severity: 'INFO' | 'WARNING' | 'ERROR' | 'CRITICAL';
  message: string;
  timestamp: string;
  metadata?: Record<string, unknown>;
}

export interface SystemStats {
  total_services: number;
  healthy_services: number;
  degraded_services: number;
  offline_services: number;
  total_events: number;
  pending_proposals: number;
  cpu_usage?: number;
  memory_usage?: number;
  uptime?: string;
}
