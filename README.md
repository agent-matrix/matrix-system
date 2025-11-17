# Matrix System SDK & CLI

<p align="center">
  <img src="https://raw.githubusercontent.com/agent-matrix/.github/main/profile/logo.png" alt="Agent-Matrix" width="140">
</p>

<p align="center">
  <strong>The First Alive AI Platform - Production-Ready SDK and CLI</strong>
</p>

<p align="center">
  <a href="https://github.com/agent-matrix/matrix-system"><img src="https://img.shields.io/badge/Ecosystem-Agent--Matrix-black" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-Apache%202.0-blue" /></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.10%2B-brightgreen" /></a>
  <a href="https://github.com/astral-sh/uv"><img src="https://img.shields.io/badge/Package%20Manager-uv-purple" /></a>
  <a href="https://mypy-lang.org/"><img src="https://img.shields.io/badge/Type%20Checked-mypy-blue" /></a>
</p>

---

## 🚀 About

**Matrix System** is a production-ready Python SDK and CLI for the **Agent-Matrix** ecosystem - the first truly alive AI platform featuring self-healing, policy-governed, and autonomous capabilities. This package provides developers and operators with a comprehensive toolkit to interact with Matrix-Hub, Matrix-AI, and Matrix-Guardian services.

### Key Features

- 🔍 **Self-Healing Architecture** - Automated health monitoring and remediation
- 🛡️ **Policy-Governed** - HITL (Human-in-the-Loop) by default with optional Autopilot
- 📊 **Observable** - Comprehensive logging, metrics, and audit trails
- 🔐 **Secure** - JWT authentication, PII redaction, and idempotent operations
- 🎯 **Type-Safe** - Full type hints and Pydantic validation
- 🧪 **Production-Ready** - Extensive test coverage and error handling
- 📦 **Modern Tooling** - Built with uv, ruff, mypy, and pytest

---

## 📋 Table of Contents

- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage](#-usage)
- [Configuration](#-configuration)
- [Development](#-development)
- [Architecture](#-architecture)
- [API Reference](#-api-reference)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

---

## 📦 Installation

### Using uv (Recommended)

```bash
# Install using uv
uv pip install matrix-system

# Or install from source
git clone https://github.com/agent-matrix/matrix-system.git
cd matrix-system
make install
```

### Using pip

```bash
pip install matrix-system
```

### Development Installation

```bash
# Clone the repository
git clone https://github.com/agent-matrix/matrix-system.git
cd matrix-system

# Install development dependencies
make dev-install

# Or manually with uv
uv pip install -e ".[dev]"
```

---

## 🚀 Quick Start

### CLI Usage

```bash
# Display version and help
matrix --version
matrix --help

# Check health of Matrix services
matrix health --service hub
matrix health --service all

# Display system information
matrix info

# View recent events
matrix events --limit 20 --app my-app

# View proposals
matrix proposals --state pending
```

### Python SDK Usage

```python
from matrix_system import __version__
from matrix_system.api.client import MatrixClient
from matrix_system.models.health import HealthCheck, HealthStatus
from matrix_system.utils.config import get_config
from matrix_system.utils.logger import setup_logging, get_logger

# Setup logging
setup_logging(log_level="INFO")
logger = get_logger(__name__)

# Initialize client
config = get_config()
client = MatrixClient(config=config)

# Check service health
try:
    health_data = client.health_check("hub")
    logger.info("health_check_success", data=health_data)
except Exception as e:
    logger.error("health_check_failed", error=str(e))

# Create health check model
health_check = HealthCheck(
    app_uid="my-app-123",
    check_type="http",
    result="pass",
    status=HealthStatus.HEALTHY,
    score=95.5,
    latency_ms=45.2,
)

print(f"Is healthy: {health_check.is_healthy()}")
print(f"Score: {health_check.score}")
```

---

## ⚙️ Configuration

Matrix System can be configured via environment variables or a `.env` file:

```bash
# API Endpoints
MATRIX_HUB_URL=https://api.matrixhub.io
MATRIX_AI_URL=https://huggingface.co/spaces/agent-matrix/matrix-ai
MATRIX_GUARDIAN_URL=http://localhost:8080

# Authentication
API_TOKEN=your-bearer-token-here

# HTTP Configuration
TIMEOUT=30
MAX_RETRIES=3

# Logging
LOG_LEVEL=INFO
LOG_JSON=false
```

### Configuration Example

Create a `.env` file in your project root:

```env
# .env
MATRIX_HUB_URL=https://api.matrixhub.io
API_TOKEN=your-secret-token
LOG_LEVEL=DEBUG
TIMEOUT=60
```

---

## 🛠️ Usage

### API Client

```python
from matrix_system.api.client import MatrixClient
from matrix_system.api.exceptions import (
    MatrixAPIError,
    MatrixAuthError,
    MatrixTimeoutError,
)

# Initialize client with context manager
with MatrixClient() as client:
    try:
        # Make API requests
        response = client.get("https://api.matrixhub.io/apps")
        print(response)

        # Check health
        health = client.health_check("hub")
        print(f"Status: {health['status']}")

    except MatrixAuthError as e:
        print(f"Authentication failed: {e}")
    except MatrixTimeoutError as e:
        print(f"Request timed out: {e}")
    except MatrixAPIError as e:
        print(f"API error: {e}")
```

### Health Monitoring

```python
from matrix_system.models.health import (
    HealthCheck,
    HealthStatus,
    HealthSummary,
)

# Create health check
check = HealthCheck(
    app_uid="my-service",
    check_type="http",
    result="pass",
    status=HealthStatus.HEALTHY,
    score=98.5,
    latency_ms=23.4,
)

# Check status
if check.is_healthy():
    print("Service is healthy!")
elif check.is_degraded():
    print("Service is degraded")
else:
    print("Service is unhealthy")

# Create summary
summary = HealthSummary(
    total_entities=100,
    healthy_count=95,
    degraded_count=3,
    unhealthy_count=2,
    average_score=94.2,
)

print(f"Health percentage: {summary.health_percentage()}%")
```

### Event Tracking

```python
from matrix_system.models.events import Event, EventType

# Create event
event = Event(
    event_type=EventType.PLAN_CREATED,
    app_uid="my-app",
    payload={
        "action": "pin_lkg",
        "version": "1.2.3",
    },
    actor="matrix-guardian",
)

# Check event properties
if event.is_critical():
    print("Critical event detected!")
elif event.is_success():
    print("Success event logged")
```

### Proposals

```python
from matrix_system.models.proposal import (
    Proposal,
    ProposalType,
    ProposalState,
)

# Create proposal
proposal = Proposal(
    app_uid="my-app",
    proposal_type=ProposalType.LKG_PIN,
    rationale="Version 1.2.4 has failing health checks",
    risk_score=15.0,
    diff={
        "action": "pin_version",
        "from_version": "1.2.4",
        "to_version": "1.2.3",
    },
)

# Check proposal status
if proposal.is_low_risk():
    print("Low risk proposal - safe to auto-approve")
elif proposal.is_high_risk():
    print("High risk - requires human review")
```

---

## 🏗️ Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/agent-matrix/matrix-system.git
cd matrix-system

# Install development dependencies
make dev-install

# Install pre-commit hooks
make pre-commit-install
```

### Available Make Commands

```bash
make help              # Display all available commands
make install           # Install production dependencies
make dev-install       # Install development dependencies
make lint              # Run linting checks
make lint-fix          # Run linting with auto-fix
make format            # Format code with black and ruff
make type-check        # Run type checking with mypy
make test              # Run all tests
make test-cov          # Run tests with coverage
make test-unit         # Run unit tests only
make test-integration  # Run integration tests only
make build             # Build distribution packages
make clean             # Clean build artifacts
make docs              # Build documentation
make serve-docs        # Serve documentation locally
```

### Running Tests

```bash
# Run all tests
make test

# Run with coverage report
make test-cov

# Run specific test file
uv run pytest tests/unit/test_config.py -v

# Run tests with specific marker
uv run pytest -m "not integration" -v
```

### Code Quality

```bash
# Run all quality checks
make check

# Individual checks
make lint              # Linting
make format            # Code formatting
make type-check        # Type checking

# Fix issues automatically
make lint-fix          # Auto-fix linting issues
make format            # Auto-format code
```

---

## 🏛️ Architecture

Matrix System is part of the **Agent-Matrix** ecosystem:

```
┌─────────────────────────────────────────────────────────┐
│                    Matrix System SDK                     │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐       │
│  │    CLI     │  │  API Client│  │   Models   │       │
│  └────────────┘  └────────────┘  └────────────┘       │
└──────────────────────┬──────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
   ┌────▼────┐   ┌────▼────┐   ┌────▼────┐
   │Matrix   │   │Matrix   │   │Matrix   │
   │Hub      │   │AI       │   │Guardian │
   └─────────┘   └─────────┘   └─────────┘
```

### Components

- **CLI** - Command-line interface for operators
- **API Client** - HTTP client with retry and error handling
- **Models** - Pydantic models for data validation
- **Utils** - Configuration, logging, and helpers

### Design Principles

1. **Type Safety** - Full type hints and runtime validation
2. **Error Handling** - Comprehensive exception hierarchy
3. **Observability** - Structured logging with context
4. **Testability** - High test coverage with unit and integration tests
5. **Standards Compliance** - PEP 8, PEP 257, PEP 484

---

## 📚 API Reference

### Client

```python
from matrix_system.api.client import MatrixClient

client = MatrixClient(config=config, logger=logger)
client.get(url, **kwargs)
client.post(url, **kwargs)
client.put(url, **kwargs)
client.delete(url, **kwargs)
client.health_check(service="hub")
```

### Models

```python
from matrix_system.models.health import HealthCheck, HealthStatus
from matrix_system.models.events import Event, EventType
from matrix_system.models.proposal import Proposal, ProposalType
```

### Configuration

```python
from matrix_system.utils.config import Config, get_config

config = get_config()  # Singleton instance
custom_config = Config(timeout=60, log_level="DEBUG")
```

### Logging

```python
from matrix_system.utils.logger import setup_logging, get_logger

setup_logging(log_level="INFO", json_format=False)
logger = get_logger(__name__)
logger.info("message", key="value")
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes** with tests and documentation
4. **Run quality checks** (`make check`)
5. **Run tests** (`make test`)
6. **Commit your changes** (`git commit -m 'Add amazing feature'`)
7. **Push to the branch** (`git push origin feature/amazing-feature`)
8. **Open a Pull Request**

### Development Standards

- Follow PEP 8 style guidelines
- Add type hints to all functions
- Write comprehensive docstrings
- Maintain test coverage above 80%
- Update documentation for new features

---

## 📄 License

This project is licensed under the **Apache License 2.0** - see the [LICENSE](LICENSE) file for details.

```
Copyright 2025 Ruslan Magana

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

---

## 👤 Author

**Ruslan Magana**

- Website: [ruslanmv.com](https://ruslanmv.com)
- GitHub: [@ruslanmv](https://github.com/ruslanmv)

---

## 🌟 Acknowledgments

Matrix System is part of the **Agent-Matrix** ecosystem, a community and enterprise hub for production-ready AI agents, tools, and MCP servers.

- **Matrix-Guardian** - Control plane for safe probes and health scoring
- **Matrix-AI** - Hugging Face service for AI-generated remediation plans
- **Matrix-Hub** - Public API and registry server
- **MatrixDB** - PostgreSQL schema for data persistence

For the full ecosystem documentation, see [README.ecosystem.md](README.ecosystem.md).

---

## 📊 Project Status

- ✅ **Production Ready** - Fully tested and documented
- ✅ **Type Safe** - 100% type coverage
- ✅ **Well Tested** - Comprehensive test suite
- ✅ **Documented** - Complete API documentation
- ✅ **Standards Compliant** - PEP 8, PEP 257, PEP 484

---

## 🔗 Links

- [Documentation](https://github.com/agent-matrix/matrix-system)
- [Issue Tracker](https://github.com/agent-matrix/matrix-system/issues)
- [Agent-Matrix Ecosystem](https://github.com/agent-matrix)
- [Author Website](https://ruslanmv.com)

---

<p align="center">
  <strong>Built with ❤️ by Ruslan Magana</strong>
</p>
