# Matrix System 1.0 — The First Alive AI Platform

> Executive reference for the **Agent-Matrix** ecosystem. This repo explains the *alive* AI architecture, how to deploy it, why it matters, and how to evolve toward supervised autonomy with zero-destructive upgrades.

<p align="center">
  <img src="https://raw.githubusercontent.com/agent-matrix/.github/main/profile/logo.png" alt="Agent-Matrix" width="140">
</p>

<p align="center">
  <a href="https://github.com/agent-matrix"><img src="https://img.shields.io/badge/Ecosystem-Agent--Matrix-black" /></a>
  <a href="#license"><img src="https://img.shields.io/badge/License-Apache%202.0-blue" /></a>
  <a href="#roadmap"><img src="https://img.shields.io/badge/Status-Stage%201%2F2-green" /></a>
  <a href="#security-and-compliance"><img src="https://img.shields.io/badge/Security-Audit%20%7C%20PII%20Redaction%20%7C%20JWT-orange" /></a>
</p>

---

## TL;DR

**Matrix System 1.0** turns a static app registry into an **alive**, policy-governed, self-healing platform. It observes health, proposes low-risk remedies via AI, and executes inside **guardrails** (HITL by default; **Autopilot** optional). Every action is **audited**. All upgrades are **additive** and **idempotent**.

* **Observe** → health snapshots and probe timelines
* **Decide** → AI returns **short, low-risk JSON plans**
* **Approve or Execute** → human-in-the-loop or Autopilot (LangGraph) behind a policy gate
* **Audit** → append-only events, ETags on reads, idempotent writes

**Business value:** lower MTTR, safer changes, clear compliance trail, and a pragmatic path to production autonomy with humans as **AI supervisors**.

---

## Part of the Agent-Matrix Ecosystem

**Matrix System** is a pillar of the broader **Agent-Matrix** initiative: a community and enterprise hub for production-ready AI agents, tools, and MCP servers. It integrates tightly with Agent-Matrix principles: reuse-first, observable, governable, easy to operate, and portable from laptops to k8s clusters.

---

## Repositories

> Replace `agent-matrix` with your org if you fork or mirror.

| Component           | Purpose                                                                        | Repository                                                                                         |
| ------------------- | ------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------- |
| **Matrix-Guardian** | Control plane; safe probes, health scoring, HITL; optional LangGraph Autopilot | [https://github.com/agent-matrix/matrix-guardian](https://github.com/agent-matrix/matrix-guardian) |
| **Matrix-AI**       | Hugging Face service that generates **safe JSON remediation plans**            | [https://github.com/agent-matrix/matrix-ai](https://github.com/agent-matrix/matrix-ai)             |
| **Matrix-Hub**      | Public API and registry server (FastAPI)                                       | [https://github.com/agent-matrix/matrix-hub](https://github.com/agent-matrix/matrix-hub)           |
| **MatrixDB**        | Postgres schema/init SQL, **additive only**                                    | [https://github.com/agent-matrix/matrix-hub-db](https://github.com/agent-matrix/matrix-hub-db)     |

---

## What we are building

* A **self-healing, policy-aligned** platform that keeps the registry healthy and usable—**even when upstreams vanish**.
* HITL default with **supervised Autopilot** available. Operators become **AI supervisors**: tune policy, monitor, and audit.
* **Zero-destructive** upgrades: DB and API changes are additive, feature-flagged, and idempotent.

---

## Architecture Overview

```mermaid
flowchart LR
  subgraph Clients
    U[End Users and SDK/CLI]
  end

  subgraph Hub[Matrix-Hub API]
    R[Routes: apps, status, bundles, guardian, patches, advisories]
    MW[Middlewares: RateLimit, Idempotency, optional JWT]
  end

  subgraph DB[MatrixDB Postgres]
    T1[health, checks, events]
    T2[versions, artifacts]
    T3[bundles, proposals, jobs optional]
  end

  subgraph Guardian[Matrix-Guardian]
    G1[Probers HTTP and MCP echo]
    G2[Health scorer]
    G3[Policy Gate]
    G4[Autopilot LangGraph optional]
  end

  subgraph AI[Matrix-AI on Hugging Face]
    A1[POST v1 plan returns JSON plan]
  end

  U -->|Install and Browse| Hub
  Guardian -->|POST status| Hub
  Hub <--> DB
  Guardian -->|Plan context| AI
  AI -->|JSON plan| Guardian
  U -->|HITL approvals| Hub
```

### Runtime Flow

```mermaid
sequenceDiagram
  participant G as Guardian
  participant H as Matrix-Hub
  participant D as MatrixDB
  participant A as Matrix-AI
  participant O as Operator

  G->>H: POST /status health and checks
  H->>D: upsert health and append checks
  G->>A: POST /v1/plan with concise context
  A-->>G: JSON plan low risk
  G->>H: POST event guardian.plan
  O->>H: POST /guardian/approve or /guardian/reject
  H-->>G: approval decision
  G->>H: optional bundles and patches Stage 2
  H->>D: append event audit
```

### Policy Gate

```mermaid
flowchart TD
  S[Signal detected] --> C[Compute risk]
  C -->|Low| P[Allowed by policy]
  C -->|Medium High| H[Hold for HITL]
  P -->|Yes| X[Execute safe steps]
  P -->|No| H
  X --> E[Emit event and re-probe]
  H --> E
```

### Deployment Topologies

```mermaid
flowchart LR
  subgraph Local
    L1[Docker Compose Hub DB Guardian]
  end
  subgraph Cloud
    K1[Hub on k8s]
    K2[DBaaS Postgres]
    K3[Guardian on k8s]
  end
  subgraph HF
    S1[Matrix-AI Space]
  end
  L1 <--dev test--> K1
  K1 <--> K2
  K3 <--> K1
  K3 <--> S1
```

### Data Model Additions

```mermaid
erDiagram
  entity ||--o{ health : maintains
  entity ||--o{ checks : has
  entity ||--o{ events : causes
  versions ||--o{ artifacts : supplies
  entity ||--o{ bundles : ships
  entity ||--o{ proposals : considers

  entity {
    text uid PK
    text name
    text summary
    float health_score
    text health_status
    timestamptz health_last_checked
    text lkg_version
    text lkg_digest
  }
  health {
    text app_uid PK
    float score
    text status
    timestamptz last_checked
    jsonb reasons
    timestamptz updated_at
  }
  checks {
    bigserial id PK
    text app_uid FK
    text check
    text result
    float latency_ms
    jsonb reasons
    timestamptz ts
  }
  events {
    bigserial id PK
    text type
    text app_uid
    jsonb payload
    timestamptz ts
  }
  versions {
    bigserial id PK
    text app_uid FK
    text version
    text commit
    timestamptz published_at
    bool is_lkg
    timestamptz created_at
  }
  artifacts {
    bigserial id PK
    bigint version_id FK
    text type
    text sha256
    bigint size_bytes
    text canonical_url
    text mirror_uri
    timestamptz created_at
  }
  bundles {
    bigserial id PK
    text app_uid FK
    text version
    text sha256
    text location
    jsonb meta
    timestamptz created_at
  }
  proposals {
    bigserial id PK
    text app_uid FK
    text type
    jsonb diff
    text proposed_by
    text state
    timestamptz ts
  }
```

---

## Why now (Executive brief)

* **Close the loop** from **detection → plan → approval → execution**, safely.
* **Reduce MTTR** with short, explainable, low-risk plans.
* **Comply by design** with append-only events, idempotent APIs, and optional JWT roles.
* **Future-proof** via supervised autonomy and reversible, additive upgrades.

**Consulting value:** A reusable blueprint for AI-assisted SRE with governance.
**Community value:** Portable, production-minded patterns anyone can adopt.

---

## Features

* **HITL default**; **Autopilot** with LangGraph optional and policy-gated
* **Idempotent POSTs** and **ETag GETs**
* **Optional JWT RS256** roles with token fallback
* **Additive DB and API patches**; no route breakages, no destructive schema
* **Append-only audit** of events; **jobs** table optional for visibility
* **CAS friendly**: LKG digest redirects and bundle inventory

---

## Autonomy Levels

* **A0 Manual**: Observe and propose only
* **A1 Suggest**: Draft proposals; auto re-probe
* **A2 Safe Autopilot**: Auto LKG pin and rollback, cache warm-ups, metadata fixes
* **A3 Extended**: Sandbox patchers with provenance and rollbacks (later)

Advance gradually with canaries, strict policies, and a kill-switch.

---

## Install and Upgrade (Additive only)

> All operations are **idempotent**. Re-running produces no duplicates.

### 1) Patch MatrixDB

Use the additive patcher to create only **new** tables and indexes.

```bash
./apply_matrixhub_db_patch_v2a.sh /path/to/matrixhub-db.zip
# Creates: 25_matrixhub_stage1_core.sql, 35_matrixhub_stage1_indexes.sql,
#          27_matrixhub_stage2_core.sql, 37_matrixhub_stage2_indexes.sql
```

### 2) Deploy Matrix-AI (Hugging Face)

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export HF_TOKEN=your_hf_token
uvicorn app.main:app --host 0.0.0.0 --port 7860
```

Deploy to a Space and set `HF_TOKEN` as a Secret.
Endpoints: `POST /v1/plan` (active), `POST /v1/chat` (RAG placeholder).

### 3) Patch Matrix-Hub API

```bash
./apply_matrixhub_patch_v2.sh /path/to/matrixhub.zip
# Rebuild and redeploy Hub from the patched source
```

Feature flags:

```
ADVISORIES_ENABLED=true
PATCHES_FACADE_ENABLED=true
RATE_LIMIT_PER_MIN=600
IDEMPOTENCY_ENABLED=true
CAS_BASE_URL=https://cas.matrixhub.io
JWT_PUBLIC_KEY_PEM="-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----"
```

### 4) Deploy Matrix-Guardian

```bash
make dev && cp configs/.env.example .env && make run
# or
docker compose -f infra/docker/compose.yaml up --build
```

Required env:

```
DATABASE_URL=postgresql+psycopg://user:pass@host:5432/guardian
MATRIXHUB_API_BASE=https://api.matrixhub.io
MATRIX_AI_BASE=https://hf.space/agent-matrix/matrix-ai
API_TOKEN=internal-bearer-token
```

### 5) Enable Autopilot (Optional)

```bash
export AUTOPILOT_ENABLED=true
export AUTOPILOT_API_ENABLED=true
export AUTOPILOT_INTERVAL_SEC=60
export AUTOPILOT_POLICY=src/guardian/agents/policies/default_policy.yaml
export AUTOPILOT_SAFE_MODE=true
python -m guardian.runner.autopilot_worker
```

---

## Security and Compliance

* **PII redaction** in matrix-ai prompts
* **JWT RS256** roles (optional) and **API tokens** for internal calls
* **Idempotency-Key** on POST, **ETag** on GET
* **Append-only audit** in `events`
* **Network safety**: low timeouts, exponential backoff, minimal egress

---

## For Consulting and IT Leaders

* **Operational rigor** with explainable AI actions and full audit trail
* **Modular adoption**: start with HITL, graduate to A2 where safe
* **Portability**: Docker Compose, k8s, and HF Spaces
* **Blueprint** for AI-assisted SRE and governance you can take to clients today

---

## Roadmap

* **M0**: Stage-1 and Stage-2 patches, HITL mode
* **M1**: Autopilot A1, dashboards and SLOs
* **M2**: Orphan custody and LKG mirroring to CAS
* **M3**: Discovery and Normalizer agents (web research and manifest standardization)
* **M4**: Extended Autopilot A2 or A3 with sandboxed patchers and provenance

---

## FAQ

**Why patches, not rewrites?**
Zero downtime and quick rollback. DB and API changes are additive and gated.

**Is this safe for production?**
Yes—HITL by default, strict plan schema, policy gate, and immutable audit trail.

**What if upstreams disappear?**
Custody workflow pins **LKG**, mirrors bundles to CAS, and keeps apps usable.

---

## Contributing

* Keep shared components **additive**
* Propose policies under `src/guardian/agents/policies/` with tests
* Include rollout and rollback steps in PRs

See `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md`.

---

## License

Apache-2.0 (ensure model and provider terms are respected in your environment).

---

### A note on the vision

Matrix System 1.0 formalizes **AI supervisors** as a first-class operating role. It upgrades brittle automation into **policy-aligned autonomy**: measurable, explainable, reversible. It is designed to become a template for **alive systems** on the internet.

---

**You can say succinctly:** *Matrix System is part of the Agent-Matrix ecosystem.*
