#!/usr/bin/env python3
"""
Verification and fix script to ensure all buttons work and queries route properly.
"""

import os
import sys
import sqlite3
from dotenv import load_dotenv

def check_environment():
    """Check environment setup."""
    print("=" * 80)
    print("1. Checking Environment Setup")
    print("=" * 80)
    
    load_dotenv()
    
    # Check .env file
    if not os.path.exists('.env'):
        print("❌ .env file not found")
        return False
    
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key or api_key == 'your_actual_api_key_here':
        print("❌ GOOGLE_API_KEY not properly configured in .env")
        return False
    
    print(f"✓ GOOGLE_API_KEY configured: {api_key[:10]}...")
    return True

def check_database():
    """Check database setup."""
    print("\n" + "=" * 80)
    print("2. Checking Database")
    print("=" * 80)
    
    if not os.path.exists('query_router.db'):
        print("❌ Database not found. Creating...")
        try:
            from database import Database
            db = Database()
            print("✓ Database created successfully")
        except Exception as e:
            print(f"❌ Failed to create database: {e}")
            return False
    
    try:
        conn = sqlite3.connect('query_router.db')
        cursor = conn.cursor()
        
        # Check for required tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        required_tables = ['tickets', 'routing_log', 'teams']
        missing_tables = [t for t in required_tables if t not in tables]
        
        if missing_tables:
            print(f"⚠️  Missing tables: {', '.join(missing_tables)}")
            print("   Reinitializing database...")
            conn.close()
            
            from database import Database
            db = Database()
            print("✓ Database reinitialized")
        else:
            print(f"✓ All required tables present: {', '.join(tables)}")
            conn.close()
        
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def check_imports():
    """Check if all required imports work."""
    print("\n" + "=" * 80)
    print("3. Checking Required Imports")
    print("=" * 80)
    
    imports = [
        ('flask', 'Flask'),
        ('google.generativeai', 'Gemini AI'),
        ('dotenv', 'python-dotenv'),
    ]
    
    all_good = True
    for module, name in imports:
        try:
            __import__(module.split('.')[0])
            print(f"✓ {name} imported successfully")
        except ImportError as e:
            print(f"❌ {name} import failed: {e}")
            all_good = False
    
    return all_good

def check_components():
    """Check if all system components can be initialized."""
    print("\n" + "=" * 80)
    print("4. Checking System Components")
    print("=" * 80)
    
    try:
        from intent_classifier import IntentClassifier
        classifier = IntentClassifier()
        print("✓ IntentClassifier initialized")
    except Exception as e:
        print(f"❌ IntentClassifier failed: {e}")
        return False
    
    try:
        from rag_system import RAGSystem
        rag = RAGSystem()
        print("✓ RAGSystem initialized")
    except Exception as e:
        print(f"❌ RAGSystem failed: {e}")
        return False
    
    try:
        from ticket_manager import TicketManager
        from database import Database
        db = Database()
        tm = TicketManager(db)
        print("✓ TicketManager initialized")
    except Exception as e:
        print(f"❌ TicketManager failed: {e}")
        return False
    
    try:
        from router_agent import RouterAgent
        router = RouterAgent()
        print("✓ RouterAgent initialized")
    except Exception as e:
        print(f"❌ RouterAgent failed: {e}")
        return False
    
    return True

def test_routing():
    """Test the routing functionality."""
    print("\n" + "=" * 80)
    print("5. Testing Query Routing")
    print("=" * 80)
    
    try:
        from router_agent import RouterAgent
        router = RouterAgent()
        
        # Test query
        test_query = {
            "channel": "email",
            "message": "API integration keeps failing with error code 403",
            "sender": "test@example.com",
            "subject": "API Error 403"
        }
        
        result = router.process_query(
            channel=test_query['channel'],
            message=test_query['message'],
            sender=test_query['sender'],
            subject=test_query['subject'],
            auto_respond=True
        )
        
        print(f"✓ Test query routed successfully")
        print(f"  - Ticket ID: {result['ticket_id']}")
        print(f"  - Intent: {result['classification']['intent']}")
        print(f"  - Urgency: {result['classification']['urgency']}")
        print(f"  - Team: {result['routing']['final_team']}")
        print(f"  - Auto-response: {'Yes' if result.get('response') else 'No'}")
        
        return True
    except Exception as e:
        print(f"❌ Routing test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_api_endpoints():
    """Check that all API endpoints are defined in app.py."""
    print("\n" + "=" * 80)
    print("6. Checking API Endpoints")
    print("=" * 80)
    
    required_endpoints = [
        ('/', 'index'),
        ('/api/submit_query', 'submit_query'),
        ('/api/tickets', 'get_tickets'),
        ('/api/stats', 'get_stats'),
        ('/api/export_tickets', 'export_tickets'),
        ('/api/sample_queries', 'get_samples'),
        ('/api/teams', 'get_teams'),
        ('/api/stream_events', 'stream_events'),
        ('/health', 'health'),
    ]
    
    try:
        with open('app.py', 'r') as f:
            content = f.read()
        
        all_present = True
        for route, name in required_endpoints:
            if f"@app.route('{route}'" in content or f'@app.route("{route}"' in content:
                print(f"✓ {route} endpoint defined")
            else:
                print(f"❌ {route} endpoint missing")
                all_present = False
        
        return all_present
    except Exception as e:
        print(f"❌ Failed to check endpoints: {e}")
        return False

def check_html_buttons():
    """Check that all buttons in HTML have proper event handlers."""
    print("\n" + "=" * 80)
    print("7. Checking HTML Buttons and Event Handlers")
    print("=" * 80)
    
    try:
        with open('templates/index.html', 'r') as f:
            content = f.read()
        
        buttons = [
            ('Submit & Route', 'type="submit"'),
            ('Refresh sample templates', 'loadSamples()'),
            ('Refresh tickets', 'loadTickets()'),
            ('Export CSV snapshot', 'exportTickets()'),
            ('Query Intake', 'showSection'),
            ('Live Operations', 'showSection'),
            ('Insights & Trends', 'showSection'),
        ]
        
        all_present = True
        for button_text, handler in buttons:
            if button_text in content and handler in content:
                print(f"✓ '{button_text}' button with handler '{handler}'")
            else:
                print(f"⚠️  '{button_text}' button or handler may be missing")
        
        # Check JavaScript functions
        js_functions = [
            'loadSamples',
            'loadTickets',
            'loadStats',
            'exportTickets',
            'showSection',
            'fillSample',
            'updateFormFields',
            'normalizeFormData',
            'displayResult',
            'displayTickets',
            'addEvent'
        ]
        
        print("\nChecking JavaScript functions:")
        for func in js_functions:
            if f"function {func}" in content or f"async function {func}" in content:
                print(f"✓ {func}() defined")
            else:
                print(f"⚠️  {func}() may be missing")
        
        return True
    except Exception as e:
        print(f"❌ Failed to check HTML: {e}")
        return False

def main():
    """Run all checks."""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "SYSTEM VERIFICATION & FIX SCRIPT" + " " * 26 + "║")
    print("╚" + "=" * 78 + "╝")
    print()
    
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print(f"Working directory: {os.getcwd()}\n")
    
    checks = [
        ("Environment Setup", check_environment),
        ("Database", check_database),
        ("Required Imports", check_imports),
        ("System Components", check_components),
        ("Query Routing", test_routing),
        ("API Endpoints", check_api_endpoints),
        ("HTML Buttons", check_html_buttons),
    ]
    
    results = []
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"\n❌ {check_name} check crashed: {e}")
            import traceback
            traceback.print_exc()
            results.append((check_name, False))
    
    # Summary
    print("\n" + "=" * 80)
    print("VERIFICATION SUMMARY")
    print("=" * 80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:12} {check_name}")
    
    print("\n" + "-" * 80)
    print(f"Results: {passed}/{total} checks passed ({passed/total*100:.0f}%)")
    print("=" * 80)
    
    if passed == total:
        print("\n🎉 ALL CHECKS PASSED!")
        print("\nYour system is ready. You can now:")
        print("  1. Start the server: python app.py 8001")
        print("  2. Open browser: http://localhost:8001")
        print("  3. Run tests: python test_buttons_routing.py")
        return 0
    else:
        print(f"\n⚠️  {total - passed} check(s) failed.")
        print("Please review the output above and fix any issues.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

