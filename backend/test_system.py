"""
Test script to verify all components of the system work correctly.
"""

import sys
from datetime import datetime


def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")

    try:
        import flask
        import google.generativeai
        import pandas

        print("✅ All required packages imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please run: pip install -r requirements.txt")
        return False


def test_database():
    """Test database functionality."""
    print("\nTesting database...")

    try:
        from database import Database

        db = Database("test_router.db")

        # Test teams
        teams = db.get_teams()
        assert len(teams) > 0, "No teams found"

        # Test ticket creation
        ticket_data = {
            "ticket_id": "TEST-001",
            "channel": "email",
            "sender": "test@test.com",
            "subject": "Test",
            "message": "Test message",
            "intent": "technical_support",
            "urgency": "medium",
            "assigned_team": "Tech Support",
            "status": "open",
        }
        db.create_ticket(ticket_data)

        # Test ticket retrieval
        ticket = db.get_ticket("TEST-001")
        assert ticket is not None, "Ticket not found"

        print("✅ Database tests passed")

        # Cleanup
        import os

        os.remove("test_router.db")

        return True
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False


def test_classifier():
    """Test intent classifier."""
    print("\nTesting intent classifier...")

    try:
        from intent_classifier import IntentClassifier

        classifier = IntentClassifier()

        # Test with a simple query
        result = classifier.classify_intent("API returns 403 error", "Technical Issue")

        assert "intent" in result, "Intent not in result"
        assert "urgency" in result, "Urgency not in result"
        assert "assigned_team" in result, "Team not in result"

        print(f"✅ Classifier tests passed")
        print(f"   Sample result: {result['intent']} ({result['urgency']})")

        return True
    except Exception as e:
        print(f"❌ Classifier test failed: {e}")
        print("   Note: This requires GOOGLE_API_KEY in .env")
        return False


def test_rag_system():
    """Test RAG system."""
    print("\nTesting RAG system...")

    try:
        from rag_system import RAGSystem

        rag = RAGSystem()

        # Test retrieval
        results = rag.retrieve_response("API error 403", n_results=1)
        assert len(results) > 0, "No results retrieved"

        print("✅ RAG system tests passed")
        print(f"   Retrieved {len(results)} response(s)")

        return True
    except Exception as e:
        print(f"❌ RAG test failed: {e}")
        return False


def test_ticket_manager():
    """Test ticket manager."""
    print("\nTesting ticket manager...")

    try:
        from database import Database
        from ticket_manager import TicketManager

        db = Database("test_tickets.db")
        tm = TicketManager(db)

        # Create a ticket
        ticket_id = tm.create_ticket(
            channel="email",
            message="Test query",
            intent="technical_support",
            urgency="high",
            assigned_team="Tech Support",
            sender="test@example.com",
            subject="Test",
        )

        assert ticket_id is not None, "Ticket ID is None"

        # Get ticket
        ticket = tm.get_ticket(ticket_id)
        assert ticket is not None, "Ticket not retrieved"

        # Get stats
        stats = tm.get_ticket_stats()
        assert stats["total_tickets"] > 0, "No tickets in stats"

        print("✅ Ticket manager tests passed")
        print(f"   Created ticket: {ticket_id}")

        # Cleanup
        import os

        os.remove("test_tickets.db")

        return True
    except Exception as e:
        print(f"❌ Ticket manager test failed: {e}")
        return False


def test_router_agent():
    """Test the main router agent."""
    print("\nTesting router agent...")

    try:
        import os

        from database import Database
        from router_agent import RouterAgent

        # Use test database
        agent = RouterAgent()

        # Process a query
        result = agent.process_query(
            channel="email",
            message="Our API integration is failing with 403 errors",
            sender="dev@test.com",
            subject="API Error",
            auto_respond=True,
        )

        assert "ticket_id" in result, "No ticket ID in result"
        assert "classification" in result, "No classification in result"
        assert "routing" in result, "No routing in result"

        print("✅ Router agent tests passed")
        print(f"   Ticket: {result['ticket_id']}")
        print(f"   Team: {result['routing']['final_team']}")
        print(f"   Urgency: {result['classification']['urgency']}")

        return True
    except Exception as e:
        print(f"❌ Router agent test failed: {e}")
        return False


def test_sample_data():
    """Test sample data loading."""
    print("\nTesting sample data...")

    try:
        from sample_data import get_canned_responses, get_sample_queries

        queries = get_sample_queries()
        responses = get_canned_responses()

        assert len(queries) > 0, "No sample queries"
        assert len(responses) > 0, "No canned responses"

        print("✅ Sample data tests passed")
        print(f"   Sample queries: {len(queries)}")
        print(f"   Canned responses: {len(responses)}")

        return True
    except Exception as e:
        print(f"❌ Sample data test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 80)
    print("  Multi-Channel Customer Query Router - System Tests")
    print("=" * 80)
    print()

    tests = [
        ("Imports", test_imports),
        ("Sample Data", test_sample_data),
        ("Database", test_database),
        ("Ticket Manager", test_ticket_manager),
        ("Intent Classifier", test_classifier),
        ("RAG System", test_rag_system),
        ("Router Agent", test_router_agent),
    ]

    results = []

    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"❌ Test '{name}' crashed: {e}")
            results.append((name, False))

    # Print summary
    print()
    print("=" * 80)
    print("  TEST SUMMARY")
    print("=" * 80)
    print()

    passed = sum(1 for _, success in results if success)
    total = len(results)

    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {status}: {name}")

    print()
    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print()
        print("🎉 ALL TESTS PASSED! System is ready to use.")
        print()
        print("Next steps:")
        print("   1. Run the demo: python demo.py")
        print("   2. Start the web app: python app.py")
        return True
    else:
        print()
        print("⚠️  Some tests failed. Please review the errors above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
