# Matrix System - Deployment Guide

Complete deployment guide for the Matrix System monitoring dashboard.

## 📋 Overview

The Matrix System consists of two main components:
- **Backend**: Python SDK/CLI (can run on Render, Heroku, or any Python hosting)
- **Frontend**: Next.js dashboard (optimized for Vercel deployment)

## 🚀 Quick Start

### Local Development

```bash
# Install all dependencies (backend + frontend)
make install-all

# Start the frontend development server
make serve

# Or start backend and frontend separately
make install          # Backend only
make frontend-install # Frontend only
```

The dashboard will be available at http://localhost:3000

## 🌐 Production Deployment

### Option 1: Full Vercel Deployment (Recommended)

Deploy both frontend and backend to Vercel for simplicity.

#### Deploy Frontend to Vercel

1. **Via Vercel CLI:**

```bash
cd frontend
npm install -g vercel
vercel login
vercel --prod
```

2. **Via GitHub Integration:**

   - Push code to GitHub
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your repository
   - Set Root Directory: `frontend`
   - Click "Deploy"

3. **Environment Variables (Vercel Dashboard):**

```bash
NEXT_PUBLIC_API_URL=https://your-backend-url.vercel.app
NEXT_PUBLIC_MATRIX_AI_URL=https://huggingface.co/spaces/agent-matrix/matrix-ai
NEXT_PUBLIC_GUARDIAN_URL=https://your-guardian-url.com
NEXT_PUBLIC_API_TOKEN=your-optional-token
```

### Option 2: Backend on Render + Frontend on Vercel

Separate hosting for backend and frontend.

#### Deploy Backend to Render

1. Create a new **Web Service** on [render.com](https://render.com)
2. Connect your GitHub repository
3. Configure:
   - **Name**: matrix-system-backend
   - **Environment**: Python 3.10+
   - **Build Command**: `make install`
   - **Start Command**: `uv run uvicorn app:app --host 0.0.0.0 --port $PORT` (adjust based on your backend)
4. Add Environment Variables:
   ```
   MATRIX_HUB_URL=https://api.matrixhub.io
   MATRIX_AI_URL=https://huggingface.co/spaces/agent-matrix/matrix-ai
   API_TOKEN=your-secret-token
   LOG_LEVEL=INFO
   ```
5. Click "Create Web Service"

#### Deploy Frontend to Vercel

1. Follow the Vercel deployment steps above
2. Set `NEXT_PUBLIC_API_URL` to your Render backend URL:
   ```
   NEXT_PUBLIC_API_URL=https://matrix-system-backend.onrender.com
   ```

## 🔧 Configuration

### Environment Variables

#### Frontend (.env.local)

```bash
# API Endpoints
NEXT_PUBLIC_API_URL=https://api.matrixhub.io
NEXT_PUBLIC_MATRIX_AI_URL=https://huggingface.co/spaces/agent-matrix/matrix-ai
NEXT_PUBLIC_GUARDIAN_URL=http://localhost:8080

# Optional: Authentication
NEXT_PUBLIC_API_TOKEN=

# App Config
NEXT_PUBLIC_APP_NAME=Matrix System
NEXT_PUBLIC_APP_VERSION=0.1.0
```

#### Backend (.env)

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

## 📦 Build Commands

### Backend

```bash
# Install dependencies
make install

# Run tests
make test

# Run linting
make lint

# Build package
make build
```

### Frontend

```bash
# Install dependencies
make frontend-install

# Development server
make frontend-dev
# or
make serve

# Production build
make frontend-build

# Start production server
make frontend-start

# Lint and type-check
make frontend-lint
make frontend-type-check
```

## 🧪 Testing

### Local Testing

1. Start backend (if you have one):
```bash
make run
```

2. Start frontend:
```bash
make serve
```

3. Access dashboard: http://localhost:3000

### Production Testing

After deployment, verify:
- ✅ Dashboard loads and displays Matrix rain effect
- ✅ All views (Dashboard, Guardian, Services, Docs) work
- ✅ System integrity displays correctly
- ✅ Logs are updating in real-time
- ✅ Proposals can be accepted/rejected
- ✅ No console errors

## 🔒 Security Checklist

- [ ] API tokens are stored as environment variables (never in code)
- [ ] HTTPS is enabled for all endpoints
- [ ] CORS is properly configured on backend
- [ ] CSP headers are set (configured in vercel.json)
- [ ] Rate limiting is enabled on API endpoints
- [ ] All dependencies are up to date

## 🐛 Troubleshooting

### Issue: "Failed to fetch" errors

**Cause**: CORS or network issues

**Solution**:
1. Check API URL in environment variables
2. Verify CORS settings on backend
3. Check browser console for specific error

### Issue: Environment variables not loading

**Cause**: Variables not prefixed with NEXT_PUBLIC_

**Solution**: All client-side env vars must start with `NEXT_PUBLIC_`

### Issue: Build fails on Vercel

**Cause**: Dependencies or type errors

**Solution**:
1. Run `npm run build` locally first
2. Fix any TypeScript errors
3. Ensure all dependencies are in package.json

### Issue: Blank screen after deployment

**Cause**: JavaScript errors or missing files

**Solution**:
1. Check browser console for errors
2. Verify all files were deployed
3. Check Vercel deployment logs

## 📊 Performance Optimization

### Frontend

- ✅ Static generation for all pages
- ✅ Automatic code splitting
- ✅ Image optimization
- ✅ Gzip compression
- ✅ CDN caching via Vercel Edge

### Backend

- Configure caching headers
- Enable compression
- Use connection pooling
- Implement rate limiting

## 🔄 CI/CD Pipeline

### GitHub Actions (Example)

```yaml
name: Deploy Frontend

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
        with:
          node-version: '18'
      - run: cd frontend && npm install
      - run: cd frontend && npm run build
      - uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.ORG_ID }}
          vercel-project-id: ${{ secrets.PROJECT_ID }}
```

## 📈 Monitoring

### Vercel Analytics

Enable in Vercel dashboard:
- Real-time visitor analytics
- Performance metrics
- Error tracking

### Custom Monitoring

The dashboard includes:
- System integrity monitoring
- Service health checks
- Live log streaming
- Proposal tracking

## 🔗 Useful Links

- [Vercel Documentation](https://vercel.com/docs)
- [Next.js Deployment](https://nextjs.org/docs/deployment)
- [Render Documentation](https://render.com/docs)
- [Matrix System GitHub](https://github.com/agent-matrix/matrix-system)

## 📞 Support

For issues or questions:
- GitHub Issues: https://github.com/agent-matrix/matrix-system/issues
- Author: Ruslan Magana (ruslanmv.com)

---

**Built with ❤️ for the Agent-Matrix ecosystem**
