#!/bin/bash
# Use PORT from environment variable if set, otherwise default to 8000
export PORT="${PORT:-8000}"
uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 1
