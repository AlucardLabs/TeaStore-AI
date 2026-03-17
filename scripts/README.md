# TeaStore AI - Scripts

Utility scripts for managing the full stack (TeaStore + AI Capabilities).

## Quick Reference

### Start/Stop

```bash
# Start everything
./start-full-stack.sh

# Stop everything
./stop-full-stack.sh

# Stop and remove volumes (clears all data)
./stop-full-stack.sh --volumes
```

### Monitoring

```bash
# Check status of all services
./status.sh

# View all logs (last 50 lines)
./logs.sh

# Follow logs for specific service
./logs.sh webui
./logs.sh ai-gateway
./logs.sh search-service
```

## Scripts

| Script | Purpose |
|--------|---------|
| `start-full-stack.sh` | Start all services, wait for health, auto-index products |
| `stop-full-stack.sh` | Stop all services (add `--volumes` to clear data) |
| `status.sh` | Show service status and health checks |
| `logs.sh` | View logs (all or specific service) |

## Requirements

- Docker & Docker Compose
- Bash shell
- curl (for health checks)

## Services Started

**TeaStore**: registry, db, persistence, auth, image, recommender, webui
**AI Stack**: qdrant, search-service, indexer-service, ai-orchestrator, ollama, ai-gateway

## Documentation

See [FULL_STACK.md](../docs/FULL_STACK.md) for complete documentation.
