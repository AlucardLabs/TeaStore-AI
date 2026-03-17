#!/bin/bash

set -e

# Colors
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${RED}═══════════════════════════════════════════════════════${NC}"
echo -e "${RED}🛑 TeaStore AI - Full Stack Shutdown${NC}"
echo -e "${RED}═══════════════════════════════════════════════════════${NC}"
echo ""

# Export compose file environment variable
export COMPOSE_FILE="docker-compose.yaml:examples/docker/docker-compose_default.yaml:ai-capabilities/docker-compose.yaml"

# Check for volume cleanup flag
if [ "$1" == "--volumes" ] || [ "$1" == "-v" ]; then
    echo -e "${YELLOW}🗑️  Stopping all services and removing volumes...${NC}"
    docker-compose down -v
    echo ""
    echo -e "${RED}✅ All services stopped and volumes removed${NC}"
    echo -e "${YELLOW}⚠️  All data has been deleted (Qdrant vectors, TeaStore DB, etc.)${NC}"
else
    echo -e "${YELLOW}🛑 Stopping all services...${NC}"
    docker-compose down
    echo ""
    echo -e "${RED}✅ All services stopped${NC}"
    echo ""
    echo -e "${YELLOW}💡 Tip: To remove volumes and clear all data:${NC}"
    echo "   ./stop-full-stack.sh --volumes"
fi

echo ""
