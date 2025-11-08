#!/usr/bin/env python3
"""
Robust startup script with error handling and diagnostics.
"""
import os
import socket
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
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

print("=" * 80)
print("🚀 Multi-Channel Customer Query Router - Startup")
print("=" * 80)
print()

# Check Python version
print(f"✓ Python version: {sys.version.split()[0]}")
print(f"✓ Working directory: {os.getcwd()}")
print()

# Check for required files
required_files = ["app.py"]
missing_files = [f for f in required_files if not os.path.exists(f)]

if missing_files:
    print(f"❌ Missing required files: {', '.join(missing_files)}")
    print("   Please ensure you're running from the backend directory")
    sys.exit(1)

print("✓ All required files present")

# Check environment variables
try:
    from dotenv import load_dotenv

    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or api_key == "your_actual_api_key_here":
        print("⚠️  Warning: GOOGLE_API_KEY not properly configured in .env")
        print("   The app will start but AI features may not work")
    else:
        print("✓ GOOGLE_API_KEY configured")
except Exception as e:
    print(f"⚠️  Warning: Could not load environment: {e}")

print()

# Check port availability
if is_port_in_use(5000):
    print("⚠️  Port 5000 is in use (macOS Control Center/AirPlay)")
    print("   Using alternative port...")

if is_port_in_use(8000):
    print("⚠️  Preferred port 8000 is already in use")
    print("   Searching for the next available port...")

port = find_available_port(8000)
if not port:
    print("❌ Could not find an available port!")
    sys.exit(1)

print(f"✓ Using port: {port}")
print()
print("=" * 80)
print(f"🌐 Starting Flask server on http://localhost:{port}")
print("=" * 80)
print()
print("   Press CTRL+C to stop the server")
print()

# Import and run the Flask app
try:
    # Set the port in environment so app.py can use it
    os.environ["FLASK_PORT"] = str(port)

    # Import the Flask app
    sys.path.insert(0, script_dir)
    from app import app

    # Run the app
    app.run(debug=True, host="0.0.0.0", port=port, threaded=True)

except KeyboardInterrupt:
    print("\n\n✓ Server stopped by user")
except ImportError as e:
    print(f"\n❌ Import Error: {e}")
    print("\nMake sure you've installed dependencies:")
    print("   pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ Error starting server: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)
