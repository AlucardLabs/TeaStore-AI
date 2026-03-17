FROM python:3.11-slim

WORKDIR /app

# Install curl for health checks
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy shared modules
COPY shared/ /app/shared/

# Copy service-specific requirements and install dependencies
COPY services/ai-gateway/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy service code
COPY services/ai-gateway/ /app/

# Expose port
EXPOSE 8000

# Run the service
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
