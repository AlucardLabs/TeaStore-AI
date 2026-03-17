# Documentation

This folder contains detailed documentation for TeaStore-AI components.

## Available Documentation

### Core Documentation
| File | Description |
|------|-------------|
| [FULL_STACK.md](FULL_STACK.md) | Complete deployment guide for unified TeaStore + AI stack |
| [TEASTORE_LEGACY.md](TEASTORE_LEGACY.md) | Original TeaStore documentation, overview, and citations |
| [GET_STARTED.md](GET_STARTED.md) | Comprehensive deployment guide for TeaStore (Docker, Kubernetes, Helm) |
| [AI_CAPABILITIES.md](AI_CAPABILITIES.md) | AI stack architecture, services, and Phase 1 completion details |

### Quick Links

**For New Users**:
- Start here: [../README.md](../README.md) - Project overview and quick start
- Then read: [FULL_STACK.md](FULL_STACK.md) - Complete deployment guide

**For Developers**:
- TeaStore: [../CLAUDE.md](../CLAUDE.md) - Development guide for Java services
- AI Services: [../ai-capabilities/CLAUDE.md](../ai-capabilities/CLAUDE.md) - Development guide for Python services

**For Deployment**:
- Simple: [GET_STARTED.md](GET_STARTED.md) - Traditional TeaStore deployment
- Full Stack: [FULL_STACK.md](FULL_STACK.md) - Unified deployment (TeaStore + AI)

## Document Overview

### TEASTORE_LEGACY.md
**Original TeaStore documentation** including:
- Project overview and architecture
- Service descriptions (Registry, Persistence, Auth, Recommender, Image, WebUI)
- Research citations (MASCOTS 2018, ICPE 2020, etc.)
- Use cases in scientific publications

### GET_STARTED.md
**Detailed deployment guide** covering:
1. **Deployment Options**:
   - Docker containers (manual setup)
   - Docker Compose
   - Kubernetes (Ribbon vs ClusterIP)
   - Helm charts

2. **Load Testing**:
   - LIMBO HTTP Load Generator
   - JMeter
   - Locust

3. **Monitoring**:
   - Kieker instrumentation (AMQP and local logging)
   - OpenTracing with Istio

4. **Building & Customizing**:
   - Maven build instructions
   - Docker image building
   - Environment variables

### AI_CAPABILITIES.md
**AI stack documentation** including:
- Architecture overview (Qdrant, Search Service, Indexer, AI Orchestrator, Ollama, AI Gateway)
- Two-track architecture (Direct APIs vs Intelligent APIs)
- Mock data structure (50 tea products)
- Quick start commands
- API endpoints and examples
- Development workflow

## Navigation Guide

```
Where to go based on your need:

📚 "I want to understand the project"
   → ../README.md (main overview)
   → TEASTORE_LEGACY.md (original TeaStore)
   → AI_CAPABILITIES.md (AI stack)

🚀 "I want to deploy and run it"
   → FULL_STACK.md (unified deployment)
   → GET_STARTED.md (traditional TeaStore only)

💻 "I want to develop/modify code"
   → ../CLAUDE.md (TeaStore Java development)
   → ../ai-capabilities/CLAUDE.md (AI Python development)

🧪 "I want to test/benchmark"
   → GET_STARTED.md (load testing section)
   → FULL_STACK.md (monitoring section)

🔧 "I want to customize deployment"
   → GET_STARTED.md (environment variables)
   → FULL_STACK.md (configuration)
```

## Related Files

- **Scripts**: [../scripts/README.md](../scripts/README.md) - Utility scripts documentation
- **Full Stack Guide**: [FULL_STACK.md](FULL_STACK.md) - Complete deployment orchestration
- **Main README**: [../README.md](../README.md) - Project entry point

---

**Quick Start**: If you just want to run everything, use:
```bash
scripts/start-full-stack.sh
```

See [FULL_STACK.md](FULL_STACK.md) for details.
