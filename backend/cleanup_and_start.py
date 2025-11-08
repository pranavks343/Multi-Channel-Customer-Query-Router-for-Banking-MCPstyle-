#!/usr/bin/env python3
"""
Clean up all running processes and start fresh.
Works on all platforms.
"""
import os
import signal
import socket
import subprocess
import sys
import time


def find_process_on_port(port):
    """Find process ID using a specific port."""
    try:
        # Try using lsof (macOS/Linux)
        result = subprocess.run(
            ["lsof", "-ti", f":{port}"], capture_output=True, text=True
        )
        if result.returncode == 0 and result.stdout.strip():
            return int(result.stdout.strip().split()[0])
    except:
        pass
    return None


def kill_process(pid):
    """Kill a process by PID."""
    try:
        os.kill(pid, signal.SIGTERM)
        time.sleep(1)
        # Check if still running
        try:
            os.kill(pid, 0)
            # Still running, force kill
            os.kill(pid, signal.SIGKILL)
        except OSError:
            pass
        return True
    except Exception as e:
        print(f"  ⚠️  Could not kill PID {pid}: {e}")
        return False


def kill_python_processes():
    """Kill Python processes running the app."""
    killed = []
    try:
        # Find Python processes
        result = subprocess.run(
            ["pgrep", "-f", "python.*(app|start|run_app).py"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            pids = [int(pid) for pid in result.stdout.strip().split() if pid]
            for pid in pids:
                if pid != os.getpid():  # Don't kill ourselves
                    if kill_process(pid):
                        killed.append(pid)
    except Exception as e:
        print(f"  Note: {e}")
    return killed


def is_port_free(port):
    """Check if a port is free."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("localhost", port))
            return True
        except:
            return False


print("=" * 80)
print("🧹 Cleanup and Restart Script")
print("=" * 80)
print()

# Change to script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

print("Step 1: Stopping existing Python processes...")
print()

killed_pids = kill_python_processes()
if killed_pids:
    print(
        f"✓ Stopped {len(killed_pids)} process(es): {', '.join(map(str, killed_pids))}"
    )
else:
    print("  No Python app processes found")

print()
print("Step 2: Checking and clearing ports 8000-8010...")
print()

ports_cleared = []
for port in range(8000, 8011):
    if not is_port_free(port):
        print(f"  Port {port} is in use...")
        pid = find_process_on_port(port)
        if pid:
            print(f"    Found PID {pid}, killing...")
            if kill_process(pid):
                ports_cleared.append(port)
                print(f"    ✓ Cleared port {port}")
            else:
                print(f"    ⚠️  Could not clear port {port}")
        else:
            print(f"    ⚠️  Could not identify process on port {port}")

if ports_cleared:
    print(f"\n✓ Cleared {len(ports_cleared)} port(s)")
else:
    print("  All ports were already free")

# Give processes time to fully terminate
print("\nWaiting for cleanup to complete...")
time.sleep(2)

# Check port 8000 specifically
print("\nVerifying port 8000 is available...")
if is_port_free(8000):
    print("✓ Port 8000 is free and ready")
else:
    print("⚠️  Port 8000 is still in use, trying the next port")

print()
print("=" * 80)
print("🚀 Starting Fresh Server")
print("=" * 80)
print()

# Start the server
try:
    # Import and run start.py logic
    exec(open("start.py").read())
except KeyboardInterrupt:
    print("\n\n✓ Server stopped by user")
except Exception as e:
    print(f"\n❌ Error starting server: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)
