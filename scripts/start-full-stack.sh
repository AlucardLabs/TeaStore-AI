#!/bin/bash

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}🚀 TeaStore AI - Full Stack Startup${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo ""

# Export compose file environment variable
export COMPOSE_FILE="docker-compose.yaml:examples/docker/docker-compose_default.yaml:ai-capabilities/docker-compose.yaml"

echo -e "${BLUE}📦 Starting all services...${NC}"
docker-compose up -d

echo ""
echo -e "${BLUE}⏳ Waiting for services to be healthy...${NC}"

# Wait for AI Gateway
echo -n "  - AI Gateway: "
until curl -s http://localhost:8000/health > /dev/null 2>&1; do
    echo -n "."
    sleep 2
done
echo -e " ${GREEN}✓${NC}"

# Wait for TeaStore WebUI
echo -n "  - TeaStore WebUI: "
until curl -s http://localhost:8080/tools.descartes.teastore.webui/ > /dev/null 2>&1; do
    echo -n "."
    sleep 2
done
echo -e " ${GREEN}✓${NC}"

# Auto-index products
echo ""
echo -e "${BLUE}📚 Indexing products...${NC}"
INDEX_RESULT=$(curl -s -X POST http://localhost:8002/index/full)
INDEXED=$(echo $INDEX_RESULT | grep -o '"indexed_products":[0-9]*' | cut -d':' -f2 || echo "0")
echo -e "  ${GREEN}✓${NC} Indexed ${INDEXED} products"

echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ TeaStore AI Full Stack is Ready!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}🌐 TeaStore Services:${NC}"
echo "   • WebUI:           http://localhost:8080/tools.descartes.teastore.webui/"
echo "   • Semantic Search: http://localhost:8080/tools.descartes.teastore.webui/semanticsearch"
echo ""
echo -e "${YELLOW}🤖 AI Services:${NC}"
echo "   • AI Gateway:      http://localhost:8000/docs"
echo "   • Search Service:  http://localhost:8001/docs"
echo "   • Indexer Service: http://localhost:8002/docs"
echo "   • AI Orchestrator: http://localhost:8003/docs"
echo "   • Qdrant Dashboard: http://localhost:6333/dashboard"
echo ""
echo -e "${YELLOW}📊 Monitoring:${NC}"
echo "   • View logs:       docker-compose logs -f [service-name]"
echo "   • View status:     docker-compose ps"
echo ""
