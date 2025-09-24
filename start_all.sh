#!/bin/bash

# Australian Electricity Market Dashboard - Simple Startup Script
# Alternative to systemd services - starts both backend and frontend

set -e

echo "🚀 Starting Australian Electricity Market Dashboard..."

# Check if virtual environment exists
if [[ ! -d "venv" ]]; then
    echo "❌ Error: Virtual environment not found. Please create it first."
    exit 1
fi

# Check if frontend node_modules exists
if [[ ! -d "frontend/node_modules" ]]; then
    echo "❌ Error: Frontend dependencies not found. Please run 'npm install' in frontend directory."
    exit 1
fi

# Function to cleanup background processes on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down services..."
    if [[ ! -z "$BACKEND_PID" ]]; then
        kill $BACKEND_PID 2>/dev/null || true
    fi
    if [[ ! -z "$FRONTEND_PID" ]]; then
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    echo "✅ Services stopped"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Start backend
echo "🔧 Starting backend server..."
source venv/bin/activate
UVICORN_RELOAD=false python start_backend.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Start frontend (production mode)
echo "🌐 Building and serving frontend..."
cd frontend
REACT_APP_API_URL=http://localhost:8000 npm run build
cd ..

# Start nginx to serve the built frontend
echo "🌐 Starting nginx to serve frontend..."
sudo nginx -c /etc/nginx/nginx.conf &
NGINX_PID=$!

echo ""
echo "🎉 Australian Electricity Market Dashboard is starting up!"
echo ""
echo "📊 Backend API:  http://localhost:8000"
echo "🌐 Frontend:     http://localhost (port 80)"
echo "📖 API Docs:     http://localhost:8000/docs"
echo ""
echo "🔄 Press Ctrl+C to stop all services"
echo ""

# Wait for both processes
wait $BACKEND_PID $NGINX_PID
