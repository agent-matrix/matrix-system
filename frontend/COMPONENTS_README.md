# Matrix System Dashboard - Component Architecture

## Directory Structure
```
frontend/src/components/
├── shared/          # Reusable UI components
│   ├── Card.tsx
│   ├── StatusBadge.tsx
│   └── TrafficVisualizer.tsx
├── layout/          # Layout components
│   ├── Sidebar.tsx
│   └── Header.tsx
├── dashboard/       # Dashboard view components
│   ├── DashboardView.tsx
│   ├── SystemIntegrity.tsx
│   ├── TrafficAnalysis.tsx
│   ├── EventStream.tsx
│   └── RemediationProposals.tsx
├── assistant/       # AI Assistant components
│   ├── AssistantView.tsx
│   ├── AssistantMessage.tsx
│   └── MonitorFeed.tsx
├── services/        # Services management
│   ├── ServicesView.tsx
│   ├── ServiceTable.tsx
│   ├── TopologyMap.tsx
│   └── ServiceDetailDrawer.tsx
├── guardian/        # Security monitoring
│   └── GuardianView.tsx
├── docs/            # Documentation
│   └── DocsView.tsx
└── settings/        # Settings modal
    └── SettingsModal.tsx
```

## Component Responsibilities

### Shared Components
- **Card**: Reusable container with optional header/icon
- **StatusBadge**: Service status indicator (ONLINE/DEGRADED/OFFLINE)
- **TrafficVisualizer**: Animated network traffic bars

### Layout Components
- **Sidebar**: Main navigation with user profile
- **Header**: Top bar with search and clock

### View Components
Each view is self-contained with its own state management and sub-components.

