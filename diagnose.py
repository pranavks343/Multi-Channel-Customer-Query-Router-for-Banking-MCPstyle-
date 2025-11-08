#!/usr/bin/env python3
"""
Comprehensive diagnostics to find why the server won't start.
"""
import os
import sys

print("=" * 80)
print("🔍 DIAGNOSTIC REPORT")
print("=" * 80)
print()

# 1. Check Python version
print("1. Python Environment:")
print(f"   Version: {sys.version}")
print(f"   Executable: {sys.executable}")
print()

# 2. Check current directory
print("2. Working Directory:")
print(f"   Current: {os.getcwd()}")
print()

# 3. Check for required files
print("3. Required Files:")
required_files = [
    'app.py',
    'router_agent.py',
    'database.py',
    'query_router.db',
    '.env',
    'requirements.txt'
]

for file in required_files:
    exists = "✓" if os.path.exists(file) else "❌"
    print(f"   {exists} {file}")
print()

# 4. Check imports
print("4. Testing Imports:")
imports_to_test = [
    ('flask', 'Flask'),
    ('dotenv', 'python-dotenv'),
    ('google.generativeai', 'google-generativeai'),
    ('langchain', 'langchain'),
    ('pandas', 'pandas'),
]

for module, package in imports_to_test:
    try:
        __import__(module.split('.')[0])
        print(f"   ✓ {package}")
    except ImportError as e:
        print(f"   ❌ {package} - {e}")
print()

# 5. Check environment variables
print("5. Environment Variables:")
try:
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv('GOOGLE_API_KEY')
    if api_key:
        masked = api_key[:10] + "..." if len(api_key) > 10 else "***"
        print(f"   ✓ GOOGLE_API_KEY: {masked}")
    else:
        print(f"   ❌ GOOGLE_API_KEY: Not set")
except Exception as e:
    print(f"   ❌ Error loading .env: {e}")
print()

# 6. Test basic Flask import and app creation
print("6. Testing Flask App Creation:")
try:
    from flask import Flask
    test_app = Flask(__name__)
    print(f"   ✓ Flask app created successfully")
except Exception as e:
    print(f"   ❌ Error creating Flask app: {e}")
    import traceback
    traceback.print_exc()
print()

# 7. Try importing the actual app
print("7. Testing Main App Import:")
try:
    sys.path.insert(0, os.getcwd())
    from app import app as main_app
    print(f"   ✓ Main app imported successfully")
    print(f"   ✓ App name: {main_app.name}")
except Exception as e:
    print(f"   ❌ Error importing app: {e}")
    print()
    print("   Full traceback:")
    import traceback
    traceback.print_exc()
print()

# 8. Check port availability
print("8. Port Availability:")
import socket

ports_to_check = [5000, 5001, 5002, 8080]
for port in ports_to_check:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    status = "❌ In Use" if result == 0 else "✓ Available"
    print(f"   {status} - Port {port}")
print()

# 9. Check database
print("9. Database Check:")
if os.path.exists('query_router.db'):
    import sqlite3
    try:
        conn = sqlite3.connect('query_router.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"   ✓ Database accessible")
        print(f"   ✓ Tables found: {len(tables)}")
        for table in tables:
            print(f"      - {table[0]}")
        conn.close()
    except Exception as e:
        print(f"   ❌ Database error: {e}")
else:
    print(f"   ❌ Database file not found")
print()

# 10. Summary
print("=" * 80)
print("📋 SUMMARY")
print("=" * 80)
print()

if not os.path.exists('app.py'):
    print("❌ CRITICAL: app.py not found!")
    print("   Solution: Make sure you're in /Users/pranavks/hackathon")
elif not os.path.exists('.env'):
    print("⚠️  WARNING: .env file not found")
    print("   Solution: Create .env with GOOGLE_API_KEY")
else:
    print("Ready to try starting the server!")
    print()
    print("Next step: python app.py 5001")

print()
print("=" * 80)

