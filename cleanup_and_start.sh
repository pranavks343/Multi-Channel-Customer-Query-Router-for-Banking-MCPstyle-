#!/bin/bash

echo "========================================"
echo "🧹 Cleaning up processes..."
echo "========================================"
echo ""

# Kill any Python processes running app.py, start.py, or run_app.py
echo "Stopping Flask/Python processes..."
pkill -f "python.*app.py" 2>/dev/null && echo "✓ Stopped app.py processes" || echo "  No app.py processes found"
pkill -f "python.*start.py" 2>/dev/null && echo "✓ Stopped start.py processes" || echo "  No start.py processes found"
pkill -f "python.*run_app.py" 2>/dev/null && echo "✓ Stopped run_app.py processes" || echo "  No run_app.py processes found"

# Wait a moment for processes to fully terminate
sleep 2

echo ""
echo "Checking ports..."

# Check if ports 5000 and 8000-8010 are still in use
for port in 5000 {8000..8010}; do
    if lsof -ti:$port >/dev/null 2>&1; then
        pid=$(lsof -ti:$port)
        echo "  Port $port in use by PID $pid"
        if [[ $port != 5000 ]]; then
            echo "  Killing process on port $port..."
            kill -9 $pid 2>/dev/null && echo "  ✓ Killed PID $pid" || echo "  ⚠️  Could not kill PID $pid"
        else
            echo "  (Port 5000 is macOS Control Center - leaving it alone)"
        fi
    fi
done

sleep 1

echo ""
echo "========================================"
echo "🚀 Starting fresh server..."
echo "========================================"
echo ""

# Change to script directory
cd "$(dirname "$0")"

# Activate virtual environment and start
source venv/bin/activate
python start.py

