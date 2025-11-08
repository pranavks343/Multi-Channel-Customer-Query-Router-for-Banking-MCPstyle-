#!/usr/bin/env python3
"""
Simple launcher script for the Flask application.
This script ensures the app runs on an available port.
"""
import os
import socket
import subprocess
import sys


def is_port_in_use(port):
    """Check if a port is already in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) == 0


def find_available_port(start_port=8000, max_attempts=10):
    """Find an available port starting from start_port."""
    for port in range(start_port, start_port + max_attempts):
        if not is_port_in_use(port):
            return port
    return None


# Change to the script's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("=" * 80)
print("🚀 Starting Multi-Channel Customer Query Router")
print("=" * 80)

# Check port 5000
if is_port_in_use(5000):
    print("⚠️  Port 5000 is in use (possibly by macOS Control Center)")
    print("   Finding alternative port...")

# Warn if preferred port already taken
if is_port_in_use(8000):
    print("⚠️  Port 8000 is in use")
    print("   Searching for the next available port...")

# Find available port
port = find_available_port(8000)
if not port:
    print("❌ Could not find an available port!")
    sys.exit(1)

print(f"✅ Using port {port}")
print(f"🌐 Starting server...")
print("=" * 80)

# Run the Flask app
try:
    # Use exec to replace this process with the Flask app
    os.execl(sys.executable, sys.executable, "app.py", str(port))
except Exception as e:
    print(f"❌ Error starting application: {e}")
    sys.exit(1)
