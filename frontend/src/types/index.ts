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
  url: string;
  version: string;
  status: 'ONLINE' | 'DEGRADED' | 'OFFLINE';
  uptime?: string;
}

export interface ProposalData {
  id: string;
  app_uid: string;
  proposal_type: string;
  rationale: string;
  risk_score: number;
  state: 'PENDING' | 'APPROVED' | 'REJECTED';
  diff: Record<string, any>;
}

export interface EventLog {
  id: string;
  event_type: string;
  app_uid: string;
  timestamp: string;
  payload: Record<string, any>;
  actor?: string;
}

export interface SystemStats {
  integrity: number;
  traffic_tps: number;
  services_online: number;
  services_total: number;
}
