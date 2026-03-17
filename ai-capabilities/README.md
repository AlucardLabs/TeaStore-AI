# TeaStore AI - Phase 1

Semantic search and AI capabilities for TeaStore using vector embeddings and open-source models.

## Phase 1: Foundation Services

This release includes:
- ✅ **Search Service**: Embedding generation using sentence-transformers and vector search with Qdrant
- ✅ **Indexer Service**: Product indexing with mock data generator (50+ tea products)
- ✅ **Qdrant Vector Database**: Production-ready vector storage
- ✅ **Mock Data**: 50 realistic tea products across 5 categories for standalone testing

## Quick Start

### Prerequisites

- Docker and Docker Compose
- 8GB+ RAM (for embedding model)
- Ports 6333, 8001, 8002 available

### Start Services

```bash
# Clone/navigate to project
cd microservices-ai-capabilities

# Start all services
docker-compose up -d

# Check service health
docker-compose ps
```

### Index Products

```bash
# Trigger full indexing (loads 50 mock products)
curl -X POST http://localhost:8002/index/full

# Check indexing status
curl http://localhost:8002/index/status
```

### Search Products

```bash
# Simple semantic search
curl -X POST http://localhost:8001/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "organic green tea",
    "limit": 5
  }'

# Search with filters
curl -X POST http://localhost:8001/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "relaxing tea",
    "limit": 10,
    "filters": {
      "category": "Herbal Tea",
      "max_price_cents": 2000
    }
  }'

# Find similar products
curl http://localhost:8001/similar/5?limit=5
```

## Architecture

```
┌─────────────────────────────────────────────────┐
│              Client (Postman/curl)               │
└─────────────────────────────────────────────────┘
         │                           │
         │ Search                    │ Index
         ↓                           ↓
┌──────────────────┐       ┌──────────────────────┐
│ Search Service   │       │ Indexer Service      │
│ (Port 8001)      │       │ (Port 8002)          │
│                  │       │                      │
│ - Embeddings     │←──────│ - Mock Data (50)     │
│ - Vector Search  │       │ - Batch Processing   │
└──────────────────┘       └──────────────────────┘
         │                           │
         └──────────┬────────────────┘
                    ↓
         ┌──────────────────────┐
         │ Qdrant Vector DB     │
         │ (Port 6333)          │
         │                      │
         │ - 384-dim vectors    │
         │ - Cosine similarity  │
         └──────────────────────┘
```

## Services

### Search Service (`:8001`)

**Endpoints:**
- `POST /search` - Semantic search with optional filters
- `POST /embed` - Generate embeddings for texts
- `GET /similar/{product_id}` - Find similar products
- `GET /health` - Health check

**Technology:**
- FastAPI for REST API
- sentence-transformers (`all-MiniLM-L6-v2`) for embeddings
- Qdrant client for vector search

### Indexer Service (`:8002`)

**Endpoints:**
- `POST /index/full` - Index all products
- `POST /index/product/{id}` - Index single product
- `GET /index/status` - Get indexing status
- `GET /mock/products` - View mock product data
- `GET /health` - Health check

**Features:**
- 50 realistic tea products across 5 categories
- Batch processing (32 products at a time)
- Rich product descriptions for semantic search

### Qdrant (`:6333`)

**Features:**
- Vector database for embeddings
- Dashboard: `http://localhost:6333/dashboard`
- REST API: `http://localhost:6333`

## Mock Data

50 products across 5 categories:
- **Green Tea** (10): Sencha, Matcha, Dragon Well, etc.
- **Black Tea** (12): Earl Grey, Assam, Ceylon, etc.
- **Herbal Tea** (10): Chamomile, Peppermint, Rooibos, etc.
- **Oolong Tea** (8): Ti Kuan Yin, Milk Oolong, etc.
- **White Tea** (10): Silver Needle, White Peony, etc.

Each product includes:
- Name, description, category, price
- Origin country
- Flavor notes for rich semantic search

## Testing with Postman

1. **Import OpenAPI Spec:**
   - Search Service: `http://localhost:8001/openapi.json`
   - Indexer Service: `http://localhost:8002/openapi.json`

2. **Test Sequence:**
   ```
   1. POST /index/full         → Index products
   2. GET /index/status        → Verify indexing
   3. POST /search             → Test semantic search
   4. GET /similar/5           → Test similarity
   ```

3. **Example Searches:**
   - "organic green tea with grassy notes"
   - "relaxing bedtime tea"
   - "strong breakfast tea"
   - "tea for digestion"

## Development

### Local Development (without Docker)

```bash
# Install dependencies
pip install -r requirements.txt
pip install -r services/search-service/requirements.txt
pip install -r services/indexer-service/requirements.txt

# Start Qdrant
docker run -p 6333:6333 qdrant/qdrant:v1.7.0

# Run services
cd services/search-service && python main.py
cd services/indexer-service && python main.py
```

### Environment Variables

See `.env.example` for all configuration options.

Key variables:
- `QDRANT_HOST` - Qdrant hostname
- `EMBEDDING_MODEL` - sentence-transformers model name
- `USE_MOCK_DATA` - Use mock data (true) or TeaStore API (false)
- `BATCH_SIZE` - Batch size for indexing

## Monitoring

```bash
# View logs
docker-compose logs -f search-service
docker-compose logs -f indexer-service

# Access Qdrant dashboard
open http://localhost:6333/dashboard

# Check collection stats
curl http://localhost:8001/health
```

## Troubleshooting

**Services won't start:**
- Check ports 6333, 8001, 8002 are available
- Ensure Docker has 8GB+ RAM allocated
- Check logs: `docker-compose logs`

**Indexing fails:**
- Ensure Search Service is healthy: `curl http://localhost:8001/health`
- Check Qdrant is accessible: `curl http://localhost:6333/health`
- Review indexer logs: `docker-compose logs indexer-service`

**Search returns no results:**
- Verify products are indexed: `curl http://localhost:8002/index/status`
- Re-index: `curl -X POST http://localhost:8002/index/full`
- Check Qdrant dashboard for vectors

**Out of memory:**
- Reduce batch size in `.env`: `BATCH_SIZE=16`
- Allocate more RAM to Docker

## Next Steps

**Phase 2: AI Orchestrator (LangChain)**
- Workflow orchestration with LangGraph
- Multi-step search workflows
- Enhanced filtering and re-ranking

**Phase 3: API Gateway + Intelligent Routing**
- Unified API entry point
- Ollama integration for LLM-based intent detection
- Natural language request handling

**Phase 4: AI Assistant**
- Product Q&A agent
- FAQ chatbot
- Conversational search

## API Documentation

- **Search Service**: http://localhost:8001/docs
- **Indexer Service**: http://localhost:8002/docs
- **ReDoc**: http://localhost:8001/redoc

## License

Apache 2.0 (matching TeaStore license)
