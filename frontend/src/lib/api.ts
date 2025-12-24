// Matrix System API Client

import type {
  HealthCheckResponse,
  ServiceInfo,
  ProposalData,
  EventLog,
  SystemStats
} from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://api.matrixhub.io';
const API_TOKEN = process.env.NEXT_PUBLIC_API_TOKEN;

class MatrixAPIClient {
  private baseURL: string;
  private token?: string;

  constructor(baseURL: string = API_BASE_URL, token?: string) {
    this.baseURL = baseURL;
    this.token = token || API_TOKEN;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...(options.headers as Record<string, string>),
    };

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    try {
      const response = await fetch(`${this.baseURL}${endpoint}`, {
        ...options,
        headers,
      });

      if (!response.ok) {
        throw new Error(`API Error: ${response.status} ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API Request Failed:', error);
      throw error;
    }
  }

  // Health Check
  async getHealth(service?: string): Promise<HealthCheckResponse> {
    const endpoint = service ? `/health/${service}` : '/health';
    return this.request<HealthCheckResponse>(endpoint);
  }

  // Services
  async getServices(): Promise<ServiceInfo[]> {
    return this.request<ServiceInfo[]>('/services');
  }

  async getServiceStatus(serviceId: string): Promise<ServiceInfo> {
    return this.request<ServiceInfo>(`/services/${serviceId}`);
  }

  // Proposals
  async getProposals(state?: string): Promise<ProposalData[]> {
    const endpoint = state ? `/proposals?state=${state}` : '/proposals';
    return this.request<ProposalData[]>(endpoint);
  }

  async approveProposal(proposalId: string): Promise<ProposalData> {
    return this.request<ProposalData>(`/proposals/${proposalId}/approve`, {
      method: 'POST',
    });
  }

  async rejectProposal(proposalId: string): Promise<ProposalData> {
    return this.request<ProposalData>(`/proposals/${proposalId}/reject`, {
      method: 'POST',
    });
  }

  // Events
  async getEvents(limit: number = 50, appUid?: string): Promise<EventLog[]> {
    let endpoint = `/events?limit=${limit}`;
    if (appUid) {
      endpoint += `&app_uid=${appUid}`;
    }
    return this.request<EventLog[]>(endpoint);
  }

  // System Stats
  async getSystemStats(): Promise<SystemStats> {
    return this.request<SystemStats>('/stats');
  }
}

// Export singleton instance
export const apiClient = new MatrixAPIClient();

// Export class for custom instances
export default MatrixAPIClient;
