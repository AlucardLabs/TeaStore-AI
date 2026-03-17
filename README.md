# TeaStore-AI

An enhanced version of the TeaStore microservices reference application with integrated AI-powered semantic search capabilities.

## Overview

**TeaStore-AI** combines the original [TeaStore](https://github.com/DescartesResearch/TeaStore) microservices architecture with a modern AI stack to demonstrate:
- ✅ Integration of traditional Java microservices with Python-based AI services
- ✅ Vector embeddings and semantic search using Qdrant
- ✅ LLM-powered natural language interfaces with LangChain/LangGraph
- ✅ Cross-stack orchestration and service discovery

### What's New
- **Semantic Search**: AI-powered product search using vector embeddings (sentence-transformers)
- **Natural Language Interface**: Query products using conversational language
- **Unified Orchestration**: Single command to start the full stack (TeaStore + AI)
- **Reusability Demonstration**: AI services integrate seamlessly with existing TeaStore components

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- 8GB+ RAM
- Available ports: 3306, 6333-6334, 8000-8003, 8080, 11434

### Start Everything

```bash
# Start full stack (TeaStore + AI)
scripts/start-full-stack.sh
```

This single command:
1. Starts all TeaStore services (Registry, DB, Persistence, Auth, Image, Recommender, WebUI)
2. Starts all AI services (Qdrant, Search, Indexer, AI Orchestrator, Ollama, AI Gateway)
3. Waits for services to be healthy
4. Automatically indexes 50 tea products
5. Displays all service URLs

### Access the Application

- **TeaStore WebUI**: http://localhost:8080/tools.descartes.teastore.webui/
- **Semantic Search**: http://localhost:8080/tools.descartes.teastore.webui/semanticsearch
- **AI Gateway API**: http://localhost:8000/docs
- **Qdrant Dashboard**: http://localhost:6333/dashboard

### Try Semantic Search

Navigate to the Semantic Search page and try queries like:
- "organic green tea"
- "relaxing herbal blend"
- "morning energy tea"
- "tea for digestion"

### Stop Everything

```bash
# Stop all services
scripts/stop-full-stack.sh

# Stop and clear all data
scripts/stop-full-stack.sh --volumes
```

---

## 📚 Documentation

### Getting Started
- **[Quick Start Guide](docs/docs/FULL_STACK.md)** - Complete setup and deployment guide
- **[Scripts Documentation](scripts/README.md)** - Utility scripts reference

### Architecture & Components

#### Legacy TeaStore
- **[TeaStore Overview](docs/TEASTORE_LEGACY.md)** - Original TeaStore documentation
- **[Detailed Deployment Guide](docs/GET_STARTED.md)** - TeaStore deployment options
- **[CLAUDE.md](CLAUDE.md)** - Development guide for working with TeaStore code

#### AI Capabilities
- **[AI Capabilities Overview](docs/AI_CAPABILITIES.md)** - AI stack architecture and services
- **[AI Development Guide](ai-capabilities/CLAUDE.md)** - Detailed AI services documentation

### Integration
- **[Integration Architecture](docs/FULL_STACK.md#architecture)** - How TeaStore and AI services work together
- **[Semantic Search Implementation](services/tools.descartes.teastore.webui/src/main/java/tools/descartes/teastore/webui/servlet/SemanticSearchServlet.java)** - WebUI integration code

---

## 🏗️ Architecture

### Services

**TeaStore Services** (Java/Jakarta EE):
- `registry` - Service discovery
- `db` - MariaDB database
- `persistence` - JPA data layer
- `auth` - Authentication service
- `image` - Image provider with caching
- `recommender` - Product recommendations (SlopeOne, Popularity, OrderBased)
- `webui` - Web interface with Semantic Search integration

**AI Services** (Python/FastAPI):
- `qdrant` - Vector database (384-dim embeddings)
- `search-service` - Embedding generation (sentence-transformers)
- `indexer-service` - Product indexing with mock data
- `ai-orchestrator` - LangChain/LangGraph workflows
- `ollama` - Local LLM (llama3.2 for intent detection)
- `ai-gateway` - Unified API with Track 1 (direct) and Track 2 (intelligent) endpoints

### Integration Point

The WebUI's `SemanticSearchServlet` calls the AI Gateway at:
```
http://host.docker.internal:8000/api/v1/search
```

This demonstrates cross-stack service communication using Docker networking.

---

## 💻 Development

### Building TeaStore

```bash
# Build all modules
mvn clean install

# Skip tests for faster builds
mvn clean install -DskipTests

# Build Docker images
cd tools/
./build_docker.sh
```

### Building AI Services

```bash
cd ai-capabilities

# Rebuild specific service
docker-compose up -d --build search-service

# Rebuild all AI services
docker-compose up -d --build
```

### Running Individual Stacks

```bash
# TeaStore only
docker-compose -f examples/docker/docker-compose_default.yaml up -d

# AI Capabilities only
cd ai-capabilities
docker-compose up -d
```

### Viewing Logs

```bash
# All services
scripts/logs.sh

# Specific service
scripts/logs.sh webui
scripts/logs.sh ai-gateway
scripts/logs.sh search-service
```

### Checking Status

```bash
scripts/status.sh
```

---

## 🧪 Testing

### Manual Testing

1. Start the full stack: `scripts/start-full-stack.sh`
2. Navigate to: http://localhost:8080/tools.descartes.teastore.webui/semanticsearch
3. Try semantic searches:
   - "organic green tea" → finds organic varieties
   - "relaxing tea" → finds chamomile, lavender, etc.
   - "morning energy" → finds caffeinated breakfast teas

### Load Testing

TeaStore supports multiple load testing tools:
- **LIMBO HTTP Load Generator** (recommended)
- **JMeter**
- **Locust**

See [GET_STARTED.md](docs/GET_STARTED.md) for load testing details.

---

## 📊 Monitoring

### Service Health Checks

```bash
# Quick health checks
scripts/status.sh

# Individual service health
curl http://localhost:8000/health  # AI Gateway
curl http://localhost:8001/health  # Search Service
curl http://localhost:6333/health  # Qdrant
```

### Dashboards

- **Qdrant Dashboard**: http://localhost:6333/dashboard
- **AI Gateway Swagger**: http://localhost:8000/docs
- **Search Service Swagger**: http://localhost:8001/docs

### Kieker Monitoring

TeaStore supports Kieker instrumentation for distributed tracing:

```bash
# Start with Kieker monitoring
docker-compose -f examples/docker/docker-compose_kieker.yaml up -d
```

See [GET_STARTED.md](docs/GET_STARTED.md) for Kieker setup details.

---

## 🔧 Configuration

### Environment Variables

**TeaStore Services** (configured in `web.xml`):
- `aiGatewayURL` - AI Gateway endpoint (default: `http://host.docker.internal:8000/api/v1/search`)
- `servicePort` - Service port
- `registryURL` - Registry endpoint

**AI Services** (configured in `.env`):
- `EMBEDDING_MODEL` - sentence-transformers model (default: `all-MiniLM-L6-v2`)
- `QDRANT_HOST` - Qdrant hostname
- `BATCH_SIZE` - Indexing batch size
- `LOG_FORMAT` - Logging format (json/text)

See [docs/FULL_STACK.md](docs/FULL_STACK.md) for complete configuration guide.

---

## 🐛 Troubleshooting

### Services Won't Start

```bash
# Check status
scripts/status.sh

# View logs
scripts/logs.sh [service-name]

# Restart everything
scripts/stop-full-stack.sh
scripts/start-full-stack.sh
```

### Port Conflicts

Ensure these ports are available:
- `3306` - MariaDB
- `6333-6334` - Qdrant
- `8000-8003` - AI services
- `8080` - TeaStore WebUI
- `11434` - Ollama

### AI Gateway Connection Issues

If WebUI can't reach AI Gateway, edit:
```
services/tools.descartes.teastore.webui/src/main/webapp/WEB-INF/web.xml
```

Change `host.docker.internal` to your host IP or `172.17.0.1` (Linux).

### Clear All Data and Restart Fresh

```bash
scripts/stop-full-stack.sh --volumes
scripts/start-full-stack.sh
```

---

## 📖 Research & Publications

### Original TeaStore

The TeaStore was first published at MASCOTS 2018:

```bibtex
@inproceedings{KiEiScBaGrKo2018-MASCOTS-TeaStore,
  author = {Kistowski, J{\'o}akim von and Eismann, Simon and Schmitt, Norbert and Bauer, Andr{\'e} and Grohmann, Johannes and Kounev, Samuel},
  title = {{TeaStore: A Micro-Service Reference Application for Benchmarking, Modeling and Resource Management Research}},
  booktitle = {Proceedings of the 26th IEEE International Symposium on the Modelling, Analysis, and Simulation of Computer and Telecommunication Systems},
  series = {MASCOTS '18},
  year = {2018},
  month = {September},
  location = {Milwaukee, WI, USA},
}
```

See [TEASTORE_LEGACY.md](docs/TEASTORE_LEGACY.md) for complete citation list.

### TeaStore-AI Integration

This enhanced version demonstrates:
- Cross-language microservices integration (Java ↔ Python)
- Vector embeddings in e-commerce applications
- LLM-powered natural language interfaces
- Unified orchestration of heterogeneous service stacks

---

## 🤝 Contributing

When contributing:
1. Follow existing code patterns (see [CLAUDE.md](CLAUDE.md) for TeaStore, [ai-capabilities/CLAUDE.md](ai-capabilities/CLAUDE.md) for AI)
2. Maintain separation between TeaStore and AI services
3. Update relevant documentation
4. Test the full stack integration

---

## 📝 License

Apache 2.0 (same as original TeaStore)

---

## 🔗 Links

- **Original TeaStore**: https://github.com/DescartesResearch/TeaStore
- **Documentation**: See `docs/` folder
- **Issues**: Open issues for bugs or feature requests

---

## 🎯 Project Structure

```
TeaStore-AI/
├── README.md                        # This file
├── docs/FULL_STACK.md                    # Complete deployment guide
├── CLAUDE.md                        # TeaStore development guide
├── docker-compose.yaml              # Full stack orchestration
├── docs/                            # Documentation
│   ├── TEASTORE_LEGACY.md          # Original TeaStore README
│   ├── GET_STARTED.md              # Detailed deployment guide
│   └── AI_CAPABILITIES.md          # AI stack overview
├── scripts/                         # Utility scripts
│   ├── start-full-stack.sh         # Start everything
│   ├── stop-full-stack.sh          # Stop everything
│   ├── status.sh                   # Check status
│   └── logs.sh                     # View logs
├── services/                        # TeaStore Java services
│   ├── tools.descartes.teastore.webui/
│   ├── tools.descartes.teastore.auth/
│   ├── tools.descartes.teastore.persistence/
│   ├── tools.descartes.teastore.recommender/
│   ├── tools.descartes.teastore.image/
│   └── tools.descartes.teastore.registry/
├── ai-capabilities/                 # AI Python services
│   ├── services/
│   │   ├── ai-gateway/
│   │   ├── search-service/
│   │   ├── indexer-service/
│   │   └── ai-orchestrator/
│   └── docker-compose.yaml
├── examples/                        # Example configurations
│   ├── docker/                     # Docker Compose files
│   ├── kubernetes/                 # Kubernetes manifests
│   └── httploadgenerator/          # Load testing profiles
└── utilities/                       # Shared utilities
```

---

**Ready to start?** → `scripts/start-full-stack.sh` 🚀
