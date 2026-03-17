# TeaStore AI - Full Stack Orchestration

This directory contains scripts for unified orchestration of TeaStore + AI Capabilities.

## Quick Start

### Start Everything
```bash
scripts/start-full-stack.sh
```

This will:
1. Start all AI services (Qdrant, Search, Indexer, AI Gateway, etc.)
2. Start all TeaStore services (Registry, DB, Persistence, WebUI, etc.)
3. Wait for services to be healthy
4. Automatically index products
5. Display service URLs

### Stop Everything
```bash
scripts/stop-full-stack.sh
```

To stop AND remove all data (volumes):
```bash
scripts/stop-full-stack.sh --volumes
```

### Check Status
```bash
scripts/status.sh
```

Shows running services and quick health checks.

### View Logs
```bash
# All services (last 50 lines)
scripts/logs.sh

# Specific service (follow mode)
scripts/logs.sh webui
scripts/logs.sh ai-gateway
scripts/logs.sh search-service
```

---

## Architecture

The full stack combines:

**TeaStore Services** (from `examples/docker/docker-compose_default.yaml`):
- Registry (service discovery)
- Database (MariaDB)
- Persistence (JPA layer)
- Auth (authentication)
- Image (image provider)
- Recommender (product recommendations)
- WebUI (web interface)

**AI Services** (from `ai-capabilities/docker-compose.yaml`):
- Qdrant (vector database)
- Search Service (embeddings + vector search)
- Indexer Service (product indexing)
- AI Orchestrator (LangChain workflows)
- Ollama (local LLM)
- AI Gateway (unified API)

**Integration Point**:
- WebUI calls AI Gateway at `http://host.docker.internal:8000/api/v1/search`
- Semantic Search feature available at: `/semanticsearch`

---

## Service URLs

### TeaStore
- **WebUI**: http://localhost:8080/tools.descartes.teastore.webui/
- **Semantic Search**: http://localhost:8080/tools.descartes.teastore.webui/semanticsearch
- **Database**: localhost:3306

### AI Services
- **AI Gateway**: http://localhost:8000/docs
- **Search Service**: http://localhost:8001/docs
- **Indexer Service**: http://localhost:8002/docs
- **AI Orchestrator**: http://localhost:8003/docs
- **Qdrant Dashboard**: http://localhost:6333/dashboard
- **Ollama**: http://localhost:11434

---

## Manual Commands

If you prefer manual control:

```bash
# Set environment variable for compose files
export COMPOSE_FILE="docker-compose.yaml:examples/docker/docker-compose_default.yaml:ai-capabilities/docker-compose.yaml"

# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View status
docker-compose ps

# View logs
docker-compose logs -f [service-name]

# Restart specific service
docker-compose restart webui

# Rebuild and restart
docker-compose up -d --build webui
```

---

## Running Individual Stacks

### TeaStore Only
```bash
docker-compose -f examples/docker/docker-compose_default.yaml up -d
```

### AI Capabilities Only
```bash
cd ai-capabilities
docker-compose up -d
```

---

## Troubleshooting

### Services won't start
```bash
# Check status
scripts/status.sh

# View logs
scripts/logs.sh [service-name]

# Restart everything
scripts/stop-full-stack.sh
scripts/start-full-stack.sh
```

### Port conflicts
Ensure these ports are available:
- 3306 (MariaDB)
- 6333-6334 (Qdrant)
- 8000-8003 (AI services)
- 8080 (TeaStore WebUI)
- 11434 (Ollama)

### AI Gateway connection issues
The WebUI container connects to AI Gateway using `host.docker.internal:8000`.

On Linux, you may need to use `172.17.0.1:8000` instead. Edit:
```
services/tools.descartes.teastore.webui/src/main/webapp/WEB-INF/web.xml
```

### Clear all data and restart fresh
```bash
scripts/stop-full-stack.sh --volumes
scripts/start-full-stack.sh
```

---

## Under the Hood

### How it works

The `docker-compose.yaml` file in the root serves as a coordination file that:
1. References both `examples/docker/docker-compose_default.yaml` and `ai-capabilities/docker-compose.yaml`
2. Adds overrides (e.g., webui dependency on ai-gateway)
3. Creates a shared network

The `COMPOSE_FILE` environment variable tells Docker Compose to merge multiple files:
```bash
COMPOSE_FILE="docker-compose.yaml:examples/docker/docker-compose_default.yaml:ai-capabilities/docker-compose.yaml"
```

Docker Compose automatically:
- Merges service definitions
- Resolves dependencies
- Creates shared networks
- Handles startup order

### File Structure
```
.
├── docker-compose.yaml                          # Coordination file (overrides)
├── FULL_STACK.md                                # This documentation
├── scripts/                                     # Utility scripts
│   ├── README.md                                # Scripts documentation
│   ├── start-full-stack.sh                      # Start everything
│   ├── stop-full-stack.sh                       # Stop everything
│   ├── status.sh                                # Status checker
│   └── logs.sh                                  # Log viewer
├── examples/docker/docker-compose_default.yaml  # TeaStore services
└── ai-capabilities/docker-compose.yaml          # AI services
```

---

## Development Workflow

### Rebuilding after code changes

**WebUI (after Java changes):**
```bash
# Build Java
mvn clean install -DskipTests

# Rebuild Docker image
docker build -t descartesresearch/teastore-webui services/tools.descartes.teastore.webui/

# Restart service
export COMPOSE_FILE="docker-compose.yaml:examples/docker/docker-compose_default.yaml:ai-capabilities/docker-compose.yaml"
docker-compose up -d webui
```

**AI Services (after Python changes):**
```bash
export COMPOSE_FILE="docker-compose.yaml:examples/docker/docker-compose_default.yaml:ai-capabilities/docker-compose.yaml"

# Rebuild specific service
docker-compose up -d --build ai-gateway

# Or rebuild all AI services
docker-compose up -d --build search-service indexer-service ai-orchestrator ai-gateway
```

---

## Migration from Separate Commands

**Before:**
```bash
# Terminal 1
cd ai-capabilities
docker-compose up -d
curl -X POST http://localhost:8002/index/full

# Terminal 2
cd ..
docker-compose -f examples/docker/docker-compose_default.yaml up -d
```

**After:**
```bash
scripts/start-full-stack.sh
```

That's it! 🎉

---

## Contributing

When adding new services:
1. Add to either `examples/docker/docker-compose_default.yaml` (TeaStore) or `ai-capabilities/docker-compose.yaml` (AI)
2. If services need to interact, add dependencies in root `docker-compose.yaml`
3. Update this README with new service URLs

---

## License

Same as TeaStore - Apache 2.0
