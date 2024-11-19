#!/bin/bash

echo "Starting local development environment..."

# Kill any existing processes
kill_port() {
    local port=$1
    if lsof -i :$port > /dev/null; then
        echo "Port $port is in use. Stopping existing process..."
        lsof -ti :$port | xargs kill -9
        sleep 1
    fi
}

kill_port 8000
kill_port 3000

# Load environment variables
if [ -f .env ]; then
    echo "Loading environment variables..."
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "Error: .env file not found!"
    exit 1
fi

# Start backend
echo "Starting backend server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# Wait for backend to start
echo "Waiting for backend to start..."
sleep 3

# Start frontend
echo "Starting frontend server..."
python frontend.py

# Cleanup on exit
cleanup() {
    echo "Cleaning up..."
    kill $BACKEND_PID 2>/dev/null
    kill_port 3000
    exit 0
}

trap cleanup SIGINT SIGTERM EXIT 