# TeaStore AI Capabilities

Complete AI integration for TeaStore featuring semantic search, conversational AI, and intelligent request routing using vector embeddings, LLMs, and open-source models.

## Implemented Features

This release includes:
- ✅ **Search Service**: Embedding generation using sentence-transformers and vector search with Qdrant
- ✅ **Indexer Service**: Product indexing with mock data generator (50+ tea products)
- ✅ **Qdrant Vector Database**: Production-ready vector storage
- ✅ **AI Orchestrator**: LangChain/LangGraph workflows for multi-step reasoning
- ✅ **AI Gateway**: Unified API with Track 1 (direct) and Track 2 (intelligent) endpoints
- ✅ **Ollama Integration**: Local LLM (llama3.2) for intent detection
- ✅ **WebUI Integration**: Two servlets for semantic search and conversational AI
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

## WebUI Integration

TeaStore WebUI includes two AI-powered features accessible from the category sidebar:

### 1. Semantic Search (`/semanticsearch`)
- **Track 1**: Direct semantic search using vector embeddings
- **Endpoint**: `http://host.docker.internal:8000/api/v1/search`
- **Technology**: Java servlet → AI Gateway → Search Service → Qdrant
- **Features**:
  - Vector-based product search
  - Configurable result limit
  - Product images and "Add to Cart" functionality
  - Displays semantic similarity scores

### 2. AI Chat Assistant (`/aichat`)
- **Track 2**: Intelligent conversational interface with intent detection
- **Endpoint**: `http://host.docker.internal:8000/api/v1/intelligent`
- **Technology**: Java servlet → AI Gateway → Ollama (LLM) → AI Orchestrator → Search Service
- **Features**:
  - Natural language understanding
  - Intent detection (SEARCH, GENERAL, etc.)
  - Real-time chat interface with AJAX
  - Product recommendations with images
  - Conversational responses
  - Loading indicators and error handling
- **Frontend**: Vanilla JavaScript with Fetch API (`chat.js`)
- **Styling**: Custom chat CSS with message bubbles and product cards

**Example Conversations:**
```
User: "Show me organic green teas"
AI: "Here are 4 organic green tea products I found:"
    [Product cards with images and Add to Cart buttons]

User: "I want something relaxing for bedtime"
AI: "I found some great relaxing teas perfect for bedtime:"
    [Chamomile, Lavender, and other herbal teas]

User: "What's the price of Earl Grey?"
AI: "I found several Earl Grey teas. Here are the options:"
    [Earl Grey products with prices]
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    TeaStore WebUI (Java)                     │
│  ┌──────────────────────┐     ┌──────────────────────────┐  │
│  │ SemanticSearchServlet│     │    AIChatServlet         │  │
│  │   (Track 1)          │     │    (Track 2)             │  │
│  └──────────────────────┘     └──────────────────────────┘  │
└────────────┬──────────────────────────────┬─────────────────┘
             │                              │
             │ /api/v1/search               │ /api/v1/intelligent
             ↓                              ↓
    ┌────────────────────────────────────────────────────────┐
    │              AI Gateway (Port 8000)                     │
    │  ┌─────────────────┐      ┌──────────────────────────┐ │
    │  │ Track 1: Direct │      │ Track 2: Intelligent     │ │
    │  │ Search          │      │ (Intent Detection)       │ │
    │  └─────────────────┘      └──────────────────────────┘ │
    └────────┬────────────────────────────┬──────────────────┘
             │                            │
             │                            ↓
             │                   ┌─────────────────┐
             │                   │ Ollama (LLM)    │
             │                   │ llama3.2        │
             │                   │ Intent: SEARCH  │
             │                   └─────────────────┘
             │                            │
             │                            ↓
             │                   ┌─────────────────────┐
             │                   │ AI Orchestrator     │
             │                   │ (LangChain/Graph)   │
             │                   └─────────────────────┘
             │                            │
             └────────────────────────────┘
                              │
                              ↓
             ┌────────────────────────────────────┐
             │       Search Service (8001)        │
             │  - Embeddings (sentence-trans.)    │
             │  - Vector Search                   │
             └────────────────────────────────────┘
                              │
                              ↓
             ┌────────────────────────────────────┐
             │       Qdrant Vector DB (6333)      │
             │  - 384-dim vectors                 │
             │  - Cosine similarity               │
             └────────────────────────────────────┘
                              ↑
                              │
             ┌────────────────────────────────────┐
             │      Indexer Service (8002)        │
             │  - Mock Data (50 products)         │
             │  - Batch Processing                │
             └────────────────────────────────────┘
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

### AI Gateway (`:8000`)

**Endpoints:**
- `POST /api/v1/search` - Track 1: Direct semantic search
- `POST /api/v1/intelligent` - Track 2: Intelligent routing with intent detection
- `GET /health` - Health check
- `GET /docs` - Swagger UI

**Technology:**
- FastAPI for REST API
- Orchestrates calls to AI Orchestrator and Search Service
- Handles both direct and intelligent request routing

**Track 1 vs Track 2:**
- **Track 1**: Direct pass-through to Search Service (fast, deterministic)
- **Track 2**: LLM-powered intent detection → orchestrated workflow (intelligent, conversational)

### AI Orchestrator (`:8003`)

**Endpoints:**
- `POST /orchestrate` - Execute LangChain workflow
- `GET /health` - Health check

**Technology:**
- LangChain/LangGraph for workflow orchestration
- Multi-step reasoning and decision making
- Integrates with Search Service for data retrieval

### Ollama (`:11434`)

**Features:**
- Local LLM server (llama3.2 model)
- Intent detection and classification
- Natural language understanding
- No external API dependencies

**Model:**
- `llama3.2` (3B parameters, optimized for chat)
- Runs on CPU or GPU
- Automatic model download on first start

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

## Testing the AI Features

### Via WebUI (Recommended)

1. Start the full stack:
   ```bash
   scripts/start-full-stack.sh
   ```

2. **Test Semantic Search:**
   - Navigate to: http://localhost:8080/tools.descartes.teastore.webui/semanticsearch
   - Try: "organic green tea", "relaxing herbal blend"

3. **Test AI Chat Assistant:**
   - Navigate to: http://localhost:8080/tools.descartes.teastore.webui/aichat
   - Chat naturally: "Show me organic green teas", "I want something relaxing"

### Via API (Direct)

```bash
# Track 1: Direct Search
curl -X POST http://localhost:8000/api/v1/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "organic green tea",
    "limit": 5
  }'

# Track 2: Intelligent Chat
curl -X POST http://localhost:8000/api/v1/intelligent \
  -H "Content-Type: application/json" \
  -d '{
    "request": "Show me cheap herbal teas under $15"
  }'
```

## Implementation Status

- ✅ **Phase 1: Foundation Services** - Search, Indexer, Qdrant, Mock Data
- ✅ **Phase 2: AI Orchestrator** - LangChain/LangGraph workflows
- ✅ **Phase 3: API Gateway + Intelligent Routing** - Ollama, Intent Detection, Track 1/2
- ✅ **Phase 4: AI Assistant** - Conversational interface, Product Q&A, Natural language search

## Future Enhancements

- **Advanced Filtering**: Multi-faceted search with price ranges, ratings, availability
- **Personalization**: User preference learning and personalized recommendations
- **Multi-language Support**: Intent detection and search in multiple languages
- **Voice Interface**: Voice-to-text for hands-free interaction
- **Real-time Indexing**: Automatic product indexing on database changes
- **A/B Testing**: Compare Track 1 vs Track 2 performance and user satisfaction

## API Documentation

- **AI Gateway**: http://localhost:8000/docs (Main entry point)
- **Search Service**: http://localhost:8001/docs
- **Indexer Service**: http://localhost:8002/docs
- **AI Orchestrator**: http://localhost:8003/docs
- **Qdrant Dashboard**: http://localhost:6333/dashboard
- **ReDoc**: http://localhost:8000/redoc

## Configuration

### WebUI AI Integration

Configured in `services/tools.descartes.teastore.webui/src/main/webapp/WEB-INF/web.xml`:

```xml
<!-- Track 1: Direct semantic search -->
<env-entry>
  <env-entry-name>aiGatewayURL</env-entry-name>
  <env-entry-type>java.lang.String</env-entry-type>
  <env-entry-value>http://host.docker.internal:8000/api/v1/search</env-entry-value>
</env-entry>

<!-- Track 2: Intelligent conversational interface -->
<env-entry>
  <env-entry-name>intelligentGatewayURL</env-entry-name>
  <env-entry-type>java.lang.String</env-entry-type>
  <env-entry-value>http://host.docker.internal:8000/api/v1/intelligent</env-entry-value>
</env-entry>
```

**Network Notes:**
- `host.docker.internal` - Use on Mac/Windows Docker Desktop
- `172.17.0.1` - Use on Linux hosts
- Configured in WebUI's Dockerfile or docker-compose extra_hosts

## License

Apache 2.0 (matching TeaStore license)
