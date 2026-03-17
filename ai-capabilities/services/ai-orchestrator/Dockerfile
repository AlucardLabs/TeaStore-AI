FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy shared modules
COPY shared/ /app/shared/

# Copy service files
COPY services/ai-orchestrator/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY services/ai-orchestrator/ /app/

# Expose port
EXPOSE 8003

# Run the service
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003"]
