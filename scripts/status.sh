#!/bin/bash

# Show status of all services

export COMPOSE_FILE="docker-compose.yaml:examples/docker/docker-compose_default.yaml:ai-capabilities/docker-compose.yaml"

echo "📊 TeaStore AI - Full Stack Status"
echo "═══════════════════════════════════════════════════════"
echo ""

docker-compose ps

echo ""
echo "💡 Quick health checks:"
echo ""

# Check AI Gateway
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ AI Gateway:      http://localhost:8000"
else
    echo "❌ AI Gateway:      Not responding"
fi

# Check TeaStore WebUI
if curl -s http://localhost:8080/tools.descartes.teastore.webui/ > /dev/null 2>&1; then
    echo "✅ TeaStore WebUI:  http://localhost:8080/tools.descartes.teastore.webui/"
else
    echo "❌ TeaStore WebUI:  Not responding"
fi

# Check Qdrant
if curl -s http://localhost:6333/health > /dev/null 2>&1; then
    echo "✅ Qdrant:          http://localhost:6333/dashboard"
else
    echo "❌ Qdrant:          Not responding"
fi

echo ""
