#!/bin/bash

# Helper script to view logs for the full stack

export COMPOSE_FILE="docker-compose.yaml:examples/docker/docker-compose_default.yaml:ai-capabilities/docker-compose.yaml"

if [ -z "$1" ]; then
    echo "📋 Showing logs for all services (last 50 lines)..."
    echo "💡 Tip: ./logs.sh [service-name] to view specific service"
    echo ""
    docker-compose logs --tail=50
else
    echo "📋 Following logs for: $1"
    docker-compose logs -f "$1"
fi
