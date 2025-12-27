# Multi-stage Dockerfile for Matrix System
# Supports both backend (Python) and frontend (Next.js)

# ==============================================
# Stage 1: Python Backend Base
# ==============================================
FROM python:3.11-slim as python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast Python package management
RUN pip install uv

# ==============================================
# Stage 2: Python Dependencies
# ==============================================
FROM python-base as python-deps

COPY pyproject.toml ./
COPY README.md ./

# Install Python dependencies using uv
RUN uv pip install --system -e .

# ==============================================
# Stage 3: Node.js Frontend Base
# ==============================================
FROM node:18-alpine as node-base

WORKDIR /app/frontend

# Install dependencies only when needed
RUN apk add --no-cache libc6-compat

# ==============================================
# Stage 4: Frontend Dependencies
# ==============================================
FROM node-base as frontend-deps

COPY frontend/package.json frontend/package-lock.json* ./

RUN npm ci

# ==============================================
# Stage 5: Frontend Builder
# ==============================================
FROM node-base as frontend-builder

COPY --from=frontend-deps /app/frontend/node_modules ./node_modules
COPY frontend/ ./

# Set build-time environment variables
ARG BUILD_VERSION
ARG BUILD_COMMIT
ARG BUILD_DATE

ENV NEXT_PUBLIC_APP_VERSION=${BUILD_VERSION} \
    NEXT_TELEMETRY_DISABLED=1

# Build Next.js application
RUN npm run build

# ==============================================
# Stage 6: Production Backend
# ==============================================
FROM python-base as backend-production

# Copy Python dependencies from deps stage
COPY --from=python-deps /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=python-deps /usr/local/bin /usr/local/bin

# Copy application code
COPY src/ /app/src/
COPY pyproject.toml README.md /app/

# Create non-root user
RUN useradd -m -u 1000 matrixuser && \
    chown -R matrixuser:matrixuser /app

USER matrixuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Expose backend port
EXPOSE 8000

# Default command for backend
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

# ==============================================
# Stage 7: Production Frontend
# ==============================================
FROM node:18-alpine as frontend-production

WORKDIR /app

ENV NODE_ENV=production \
    NEXT_TELEMETRY_DISABLED=1

RUN apk add --no-cache libc6-compat

# Copy built application
COPY --from=frontend-builder /app/frontend/.next/standalone ./
COPY --from=frontend-builder /app/frontend/.next/static ./.next/static
COPY --from=frontend-builder /app/frontend/public ./public

# Create non-root user
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs && \
    chown -R nextjs:nodejs /app

USER nextjs

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000/api/health || exit 1

EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

# Start Next.js server
CMD ["node", "server.js"]

# ==============================================
# Stage 8: Full Stack (Combined)
# ==============================================
FROM python:3.11-slim as fullstack

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    NODE_ENV=production

WORKDIR /app

# Install system dependencies including Node.js
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    ca-certificates \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Copy Python backend
COPY --from=python-deps /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY src/ /app/src/
COPY pyproject.toml README.md /app/

# Copy Frontend
COPY --from=frontend-builder /app/frontend/.next /app/frontend/.next
COPY --from=frontend-builder /app/frontend/public /app/frontend/public
COPY --from=frontend-deps /app/frontend/node_modules /app/frontend/node_modules
COPY frontend/package.json /app/frontend/

# Create startup script
RUN echo '#!/bin/bash\n\
# Start backend\n\
uvicorn src.main:app --host 0.0.0.0 --port 8000 &\n\
# Start frontend\n\
cd /app/frontend && npm start &\n\
# Wait for both\n\
wait -n\n\
exit $?\n\
' > /app/start.sh && chmod +x /app/start.sh

# Create non-root user
RUN useradd -m -u 1000 matrixuser && \
    chown -R matrixuser:matrixuser /app

USER matrixuser

EXPOSE 3000 8000

# Health check for both services
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:3000/api/health && python -c "import sys; sys.exit(0)" || exit 1

CMD ["/app/start.sh"]

# ==============================================
# Build Arguments (can be overridden)
# ==============================================
ARG BUILD_VERSION=0.1.0
ARG BUILD_COMMIT=unknown
ARG BUILD_DATE=unknown
ARG GATEWAY_REF=main
ARG PIP_INDEX_URL

# Labels
LABEL org.opencontainers.image.title="matrix-system" \
      org.opencontainers.image.description="Matrix Hub — central catalog & monitoring dashboard" \
      org.opencontainers.image.version="${BUILD_VERSION}" \
      org.opencontainers.image.created="${BUILD_DATE}" \
      org.opencontainers.image.revision="${BUILD_COMMIT}" \
      org.opencontainers.image.source="https://github.com/agent-matrix/matrix-system" \
      org.opencontainers.image.licenses="Apache-2.0"
