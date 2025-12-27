# Matrix System - Docker Deployment Guide

## 🐳 Available Docker Images

The Matrix System provides three Docker image variants:

1. **Full Stack** (frontend + backend combined)
2. **Frontend Only** (Next.js dashboard)
3. **Backend Only** (Python SDK/API)

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended for Development)

```bash
# Clone the repository
git clone https://github.com/agent-matrix/matrix-system.git
cd matrix-system

# Create .env file from example
cp .env.example .env

# Edit .env with your configuration
nano .env

# Start all services
docker-compose up -d

# Or start full-stack single container
docker-compose --profile fullstack up -d
```

Access the dashboard at: http://localhost:3000

### Option 2: Docker Run (Quick Test)

**Full Stack:**
```bash
docker run -d \
  -p 3000:3000 \
  -p 8000:8000 \
  --env-file .env \
  --name matrix-system \
  docker.io/ruslanmv/matrix-system:latest
```

**Frontend Only:**
```bash
docker run -d \
  -p 3000:3000 \
  -e NEXT_PUBLIC_API_URL=https://api.matrixhub.io \
  --name matrix-frontend \
  docker.io/ruslanmv/matrix-system:frontend-latest
```

**Backend Only:**
```bash
docker run -d \
  -p 8000:8000 \
  -e API_TOKEN=your-token \
  --name matrix-backend \
  docker.io/ruslanmv/matrix-system:backend-latest
```

## 📦 Building Images Locally

### Build Full Stack
```bash
docker build \
  --target fullstack \
  --build-arg BUILD_VERSION=0.1.0 \
  --build-arg BUILD_COMMIT=$(git rev-parse --short HEAD) \
  --build-arg BUILD_DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ") \
  -t matrix-system:latest \
  .
```

### Build Frontend Only
```bash
docker build \
  --target frontend-production \
  -t matrix-system:frontend \
  .
```

### Build Backend Only
```bash
docker build \
  --target backend-production \
  -t matrix-system:backend \
  .
```

## 🔧 Environment Variables

### Required Variables

```bash
# API Endpoints
NEXT_PUBLIC_API_URL=https://api.matrixhub.io
MATRIX_HUB_URL=https://api.matrixhub.io

# Authentication
API_TOKEN=your-secret-token-here
```

### Optional Variables

```bash
# AI Providers
OPENAI_API_KEY=sk-...
CLAUDE_API_KEY=sk-ant-...
AI_PROVIDER=openai

# Logging
LOG_LEVEL=INFO
LOG_JSON=false

# Features
ENABLE_AUTOPILOT=true
ENABLE_HITL_MODE=true
```

See `.env.example` for complete list.

## 🏗️ Multi-Architecture Support

All images support:
- `linux/amd64` (Intel/AMD)
- `linux/arm64` (Apple Silicon, ARM servers)

Pull command automatically selects the correct architecture:
```bash
docker pull docker.io/ruslanmv/matrix-system:latest
```

## 📊 Health Checks

All containers include health checks:

**Frontend:**
```bash
docker exec matrix-frontend wget --spider http://localhost:3000/api/health
```

**Backend:**
```bash
docker exec matrix-backend python -c "import sys; sys.exit(0)"
```

**Full Stack:**
```bash
docker exec matrix-system sh -c "curl -f http://localhost:3000/api/health && python -c 'import sys; sys.exit(0)'"
```

## 🔒 Security Best Practices

1. **Never bake secrets into images**
   - Use environment variables or secrets management
   - Our images enforce this with sanity checks

2. **Use specific version tags**
   ```bash
   docker pull docker.io/ruslanmv/matrix-system:v0.1.0
   ```

3. **Run as non-root user**
   - All images use non-root users by default

4. **Network isolation**
   - Use Docker networks to isolate services

## 🚢 Production Deployment

### Kubernetes (Helm recommended)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: matrix-system
spec:
  replicas: 3
  selector:
    matchLabels:
      app: matrix-system
  template:
    metadata:
      labels:
        app: matrix-system
    spec:
      containers:
      - name: matrix
        image: docker.io/ruslanmv/matrix-system:v0.1.0
        ports:
        - containerPort: 3000
        - containerPort: 8000
        envFrom:
        - secretRef:
            name: matrix-secrets
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "2000m"
```

### Docker Swarm

```bash
docker stack deploy -c docker-compose.yml matrix
```

### Cloud Run / App Runner

Use frontend-only image for serverless deployment:

```bash
gcloud run deploy matrix-dashboard \
  --image docker.io/ruslanmv/matrix-system:frontend-latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars NEXT_PUBLIC_API_URL=https://api.matrixhub.io
```

## 📈 Monitoring

### Logs
```bash
# View logs
docker logs matrix-system -f

# With docker-compose
docker-compose logs -f frontend backend
```

### Metrics
```bash
# Container stats
docker stats matrix-system

# Resource usage
docker inspect matrix-system --format='{{.State.Health.Status}}'
```

## 🛠️ Troubleshooting

### Container won't start
```bash
# Check logs
docker logs matrix-system

# Inspect container
docker inspect matrix-system

# Verify environment variables
docker exec matrix-system env
```

### Port conflicts
```bash
# Use different ports
docker run -p 3001:3000 -p 8001:8000 matrix-system:latest
```

### Performance issues
```bash
# Increase resources
docker run --memory=4g --cpus=2 matrix-system:latest
```

## 🔄 Updates

### Pull latest images
```bash
docker pull docker.io/ruslanmv/matrix-system:latest
docker-compose pull
docker-compose up -d
```

### Rolling updates (zero-downtime)
```bash
docker-compose up -d --no-deps --build frontend
docker-compose up -d --no-deps --build backend
```

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [Matrix System GitHub](https://github.com/agent-matrix/matrix-system)

## 🐛 Reporting Issues

If you encounter any issues:
1. Check logs: `docker logs matrix-system`
2. Verify environment variables
3. Open an issue: https://github.com/agent-matrix/matrix-system/issues

---

**Built with ❤️ for the Agent-Matrix ecosystem**
