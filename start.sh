#!/bin/bash

# Make sure the script fails on any error
set -e

# Export environment variables
export PORT="${PORT:-10000}"
export ENVIRONMENT="production"

echo "Starting server on port $PORT"

# Start the server with explicit port binding
python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 1
