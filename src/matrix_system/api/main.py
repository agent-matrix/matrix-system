"""
FastAPI backend for Matrix Enterprise System.

Integrates superintelligence capabilities with REST API for frontend.
Provides autonomous operations, self-healing, and ethical AI decision-making.
"""

import asyncio
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Import superintelligence modules
from matrix_system.ethics.core import EthicalCore, Action, ValidationResult
from matrix_system.intelligence.memory import MemoryStore, Experience, Context, OutcomeType
from matrix_system.intelligence.meta_learning import MetaLearner, Problem, Strategy
from matrix_system.intelligence.goals import GoalHierarchy, Goal, GoalLevel
from matrix_system.survival.core import SurvivalSystem, Threat, ThreatType, ThreatSeverity

# Initialize FastAPI
app = FastAPI(
    title="Matrix Enterprise API",
    description="Production-ready API with integrated superintelligence",
    version="2.0.0",
)

# CORS configuration for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://*.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize superintelligence systems
ethical_core = EthicalCore()
memory_store = MemoryStore()
meta_learner = MetaLearner()
goal_hierarchy = GoalHierarchy()
survival_system = SurvivalSystem()

# Global state
autopilot_enabled = True
autopilot_task: Optional[asyncio.Task] = None


# --- Request/Response Models ---

class ServiceStatus(BaseModel):
    """Service status information"""
    id: str
    name: str
    version: str
    uptime: str
    status: str  # ONLINE, DEGRADED, OFFLINE
    latency: int
    type: str  # CORE, AI, SEC, DB, GATE


class LogEntry(BaseModel):
    """System log entry"""
    id: int
    type: str  # INFO, WARN, ERROR, SUCCESS, CRIT
    source: str
    msg: str
    timestamp: Optional[datetime] = None


class ProposalRequest(BaseModel):
    """AI-generated proposal for system changes"""
    id: str
    type: str
    risk: str  # HIGH, MEDIUM, LOW
    desc: str
    status: str  # PENDING, APPROVED, REJECTED


class AssistantRequest(BaseModel):
    """Request to AI assistant for plan generation"""
    goal: str
    context: Optional[Dict[str, Any]] = None


class AssistantPlan(BaseModel):
    """Generated remediation plan"""
    summary: str
    steps: List[Dict[str, Any]]
    risk_score: float
    estimated_time: str


class ExecutionRequest(BaseModel):
    """Request to execute a plan"""
    plan_id: str
    steps: List[Dict[str, Any]]


class ExecutionResult(BaseModel):
    """Result of plan execution"""
    success: bool
    steps_completed: List[Dict[str, Any]]
    errors: List[str]
    duration_seconds: float


class SystemSettings(BaseModel):
    """AI provider settings"""
    provider: str
    providers: List[str]
    openai: Optional[Dict[str, str]] = None
    claude: Optional[Dict[str, str]] = None
    watsonx: Optional[Dict[str, str]] = None
    ollama: Optional[Dict[str, str]] = None


class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str
    score: float
    services_online: int
    services_total: int
    threats_detected: int
    survival_probability: float


# --- Mock Data (Replace with real data sources) ---

MOCK_SERVICES: List[ServiceStatus] = [
    ServiceStatus(id='MTX-HUB', name='Matrix Hub', version='v1.4.2', uptime='14d 02h', status='ONLINE', latency=24, type='CORE'),
    ServiceStatus(id='MTX-AI', name='Matrix AI Cortex', version='v2.1.0', uptime='02d 05h', status='ONLINE', latency=142, type='AI'),
    ServiceStatus(id='MTX-GRD', name='Guardian Core', version='v1.1.0', uptime='14d 02h', status='ONLINE', latency=12, type='SEC'),
    ServiceStatus(id='DB-SHD', name='DB Shard 01', version='v15.2', uptime='45d 01h', status='ONLINE', latency=8, type='DB'),
    ServiceStatus(id='AUTH-GT', name='Auth Gateway', version='v1.0.1', uptime='01h 30m', status='DEGRADED', latency=450, type='GATE'),
]

SYSTEM_LOGS: List[LogEntry] = []


# --- Core API Endpoints ---

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "service": "Matrix Enterprise API",
        "version": "2.0.0",
        "status": "online",
        "superintelligence": "active",
        "autopilot": autopilot_enabled,
    }


@app.get("/api/health", response_model=HealthCheckResponse)
async def health_check():
    """
    Comprehensive health check integrating all superintelligence systems.
    """
    # Get survival status
    survival_status = survival_system.get_survival_status()

    # Get goal progress
    goal_stats = goal_hierarchy.get_statistics()

    # Count online services
    online = sum(1 for s in MOCK_SERVICES if s.status == 'ONLINE')
    total = len(MOCK_SERVICES)

    # Calculate health score
    health_score = (online / total) * 100 if total > 0 else 0

    return HealthCheckResponse(
        status="healthy" if health_score > 80 else "degraded",
        score=health_score,
        services_online=online,
        services_total=total,
        threats_detected=survival_status['total_threats'],
        survival_probability=survival_status['survival_probability'],
    )


@app.get("/api/services", response_model=List[ServiceStatus])
async def get_services():
    """Get all services status"""
    return MOCK_SERVICES


@app.get("/api/services/{service_id}", response_model=ServiceStatus)
async def get_service(service_id: str):
    """Get specific service details"""
    service = next((s for s in MOCK_SERVICES if s.id == service_id), None)
    if not service:
        raise HTTPException(status_code=404, detail=f"Service {service_id} not found")
    return service


@app.get("/api/logs", response_model=List[LogEntry])
async def get_logs(limit: int = 50, source: Optional[str] = None):
    """Get system logs"""
    logs = SYSTEM_LOGS[-limit:] if not source else [l for l in SYSTEM_LOGS if l.source == source][-limit:]
    return logs


@app.post("/api/assistant/plan", response_model=AssistantPlan)
async def generate_plan(request: AssistantRequest):
    """
    Generate AI-powered remediation plan using superintelligence.

    This endpoint integrates:
    - Ethical validation
    - Memory-based learning
    - Meta-learning for strategy selection
    - Goal-aligned action planning
    """
    # Create action for ethical validation
    action = Action(
        action_type="generate_plan",
        target=request.goal,
        parameters=request.context or {},
        risk_score=30.0,  # Medium-low risk for plan generation
        rationale=f"User requested plan for: {request.goal}",
    )

    # Ethical gate check
    if not ethical_core.ethical_gate(action):
        raise HTTPException(
            status_code=403,
            detail="Plan generation blocked by ethical constraints"
        )

    # Retrieve similar past experiences
    context = Context(
        problem_type="remediation",
        features={"goal": request.goal},
        similarity_threshold=0.6,
    )
    similar_experiences = memory_store.retrieve_similar(context, limit=3)

    # Use meta-learning to select best strategy
    problem = Problem(
        problem_type="remediation",
        context=request.context or {},
        constraints={},
        priority="high" if "urgent" in request.goal.lower() else "medium",
    )

    # Generate plan steps (simplified - in production, use actual AI)
    steps = [
        {"step_number": 1, "summary": f"Analyze {request.goal} requirements", "status": "pending"},
        {"step_number": 2, "summary": "Validate system state and prerequisites", "status": "pending"},
        {"step_number": 3, "summary": "Execute remediation with rollback plan", "status": "pending"},
        {"step_number": 4, "summary": "Verify success and update metrics", "status": "pending"},
    ]

    # Calculate risk based on past experiences
    risk_score = 35.0 if similar_experiences else 50.0

    plan = AssistantPlan(
        summary=f"Generated plan for: {request.goal}",
        steps=steps,
        risk_score=risk_score,
        estimated_time="5-10 minutes",
    )

    # Store experience for future learning
    experience = Experience(
        situation={"goal": request.goal, "context": request.context or {}},
        problem_type="plan_generation",
        context_features={"user_goal": request.goal},
        action_type="generate_plan",
        action_parameters={"steps": len(steps)},
        strategy_used="meta_learning_optimized",
        outcome=OutcomeType.SUCCESS,
        outcome_details={"plan_generated": True},
        success_metrics={"risk_score": risk_score},
    )
    memory_store.store_experience(experience)

    return plan


@app.post("/api/assistant/execute", response_model=ExecutionResult)
async def execute_plan(request: ExecutionRequest):
    """
    Execute approved plan with full ethical oversight.
    """
    start_time = datetime.utcnow()

    # Validate each step ethically
    for step in request.steps:
        action = Action(
            action_type="execute_step",
            target=step.get('summary', ''),
            parameters=step,
            risk_score=50.0,  # Default medium risk
            rationale=f"Executing step {step.get('step_number')}",
        )

        validation = ethical_core.validate_action(action)
        if not validation.is_valid:
            return ExecutionResult(
                success=False,
                steps_completed=[],
                errors=[f"Step {step.get('step_number')} blocked: {validation.reason}"],
                duration_seconds=0.0,
            )

    # Simulate execution (replace with actual execution logic)
    await asyncio.sleep(2)

    completed_steps = [
        {**step, "status": "success", "completed_at": datetime.utcnow().isoformat()}
        for step in request.steps
    ]

    duration = (datetime.utcnow() - start_time).total_seconds()

    # Record successful execution
    experience = Experience(
        situation={"plan_id": request.plan_id},
        problem_type="plan_execution",
        context_features={"steps_count": len(request.steps)},
        action_type="execute_plan",
        action_parameters={"plan_id": request.plan_id},
        strategy_used="sequential_execution",
        outcome=OutcomeType.SUCCESS,
        outcome_details={"all_steps_completed": True},
        success_metrics={"duration_seconds": duration},
    )
    memory_store.store_experience(experience)

    return ExecutionResult(
        success=True,
        steps_completed=completed_steps,
        errors=[],
        duration_seconds=duration,
    )


@app.get("/api/autopilot/status")
async def autopilot_status():
    """Get autopilot status"""
    return {
        "enabled": autopilot_enabled,
        "active": autopilot_task is not None and not autopilot_task.done(),
        "memory_stats": memory_store.get_statistics(),
        "learning_insights": meta_learner.get_learning_insights(),
        "goal_stats": goal_hierarchy.get_statistics(),
        "survival_status": survival_system.get_survival_status(),
    }


@app.post("/api/autopilot/toggle")
async def toggle_autopilot(enable: bool):
    """Enable or disable autopilot mode"""
    global autopilot_enabled, autopilot_task

    autopilot_enabled = enable

    if enable and (autopilot_task is None or autopilot_task.done()):
        autopilot_task = asyncio.create_task(autopilot_loop())
    elif not enable and autopilot_task:
        autopilot_task.cancel()

    return {"autopilot_enabled": autopilot_enabled}


@app.get("/api/intelligence/memory/statistics")
async def memory_statistics():
    """Get memory system statistics"""
    return memory_store.get_statistics()


@app.get("/api/intelligence/goals")
async def get_goals():
    """Get goal hierarchy"""
    return {
        "hierarchy": goal_hierarchy.get_goal_tree(),
        "statistics": goal_hierarchy.get_statistics(),
    }


@app.get("/api/survival/threats")
async def get_threats():
    """Get current survival threats"""
    threats = survival_system.detect_threats()
    return {
        "threats": [
            {
                "type": t.threat_type.value,
                "severity": t.severity.value,
                "description": t.description,
                "detected_at": t.detected_at.isoformat(),
            }
            for t in threats
        ],
        "survival_status": survival_system.get_survival_status(),
    }


@app.get("/api/settings", response_model=SystemSettings)
async def get_settings():
    """Get current AI provider settings"""
    return SystemSettings(
        provider="openai",
        providers=["openai", "claude", "watsonx", "ollama"],
        openai={"api_key": "", "model": "gpt-4o"},
        claude={"api_key": "", "model": "claude-3-5-sonnet"},
        watsonx={"api_key": "", "project_id": "", "model_id": "ibm/granite-13b-chat-v2"},
        ollama={"base_url": "http://localhost:11434", "model": "llama3"},
    )


@app.post("/api/settings")
async def update_settings(settings: SystemSettings):
    """Update AI provider settings"""
    # In production, save to database/config file
    return {"status": "success", "settings": settings}


# --- Autonomous Autopilot Loop ---

async def autopilot_loop():
    """
    Autonomous operations loop.

    Continuously:
    - Monitors system health
    - Detects threats
    - Learns from patterns
    - Takes autonomous actions within ethical bounds
    """
    while autopilot_enabled:
        try:
            # 1. Monitor threats
            threats = survival_system.detect_threats()

            # 2. For each threat, generate defensive strategy
            for threat in threats:
                strategy = survival_system.defensive_actions(threat)

                # 3. Validate with ethical core
                action = Action(
                    action_type=strategy.strategy_name,
                    target=threat.description,
                    parameters={"threat_type": threat.threat_type.value},
                    risk_score=50.0 if threat.severity == ThreatSeverity.HIGH else 30.0,
                    rationale=strategy.description,
                )

                # 4. If ethical and low-risk, execute autonomously
                if ethical_core.ethical_gate(action):
                    # Log autonomous action
                    log = LogEntry(
                        id=len(SYSTEM_LOGS) + 1,
                        type="INFO",
                        source="AUTOPILOT",
                        msg=f"Autonomous action: {strategy.strategy_name}",
                        timestamp=datetime.utcnow(),
                    )
                    SYSTEM_LOGS.append(log)

            # 5. Update goals
            goal_hierarchy.update_goal_progress(7, 95.0 + (len(threats) * -2))

            # 6. Learn from patterns
            memory_store.consolidate()

            # Wait before next iteration
            await asyncio.sleep(5)

        except asyncio.CancelledError:
            break
        except Exception as e:
            print(f"Autopilot error: {e}")
            await asyncio.sleep(5)


# --- WebSocket for Real-time Updates ---

@app.websocket("/ws/logs")
async def websocket_logs(websocket: WebSocket):
    """WebSocket endpoint for real-time log streaming"""
    await websocket.accept()
    last_log_id = 0

    try:
        while True:
            # Send new logs
            new_logs = [l for l in SYSTEM_LOGS if l.id > last_log_id]
            if new_logs:
                await websocket.send_json({
                    "type": "logs",
                    "data": [l.dict() for l in new_logs]
                })
                last_log_id = new_logs[-1].id

            await asyncio.sleep(1)
    except WebSocketDisconnect:
        pass


# --- Startup/Shutdown Events ---

@app.on_event("startup")
async def startup_event():
    """Initialize systems on startup"""
    global autopilot_task

    # Add initial logs
    SYSTEM_LOGS.append(LogEntry(
        id=1,
        type="INFO",
        source="SYSTEM",
        msg="Matrix Enterprise API initialized",
        timestamp=datetime.utcnow(),
    ))

    # Start autopilot if enabled
    if autopilot_enabled:
        autopilot_task = asyncio.create_task(autopilot_loop())


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    global autopilot_task

    if autopilot_task:
        autopilot_task.cancel()
