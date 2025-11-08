"""
System initialization script.
Initializes database, RAG system, and prepares the environment.
"""

import os
import sys

from dotenv import load_dotenv

# Add parent directory to path to import from agents
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.database import Database
from agents.rag_system import RAGSystem


def check_environment():
    """Check if required environment variables are set."""
    load_dotenv()

    print("Checking environment variables...")

    required_vars = ["GOOGLE_API_KEY"]
    missing_vars = []

    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("\nPlease create a .env file with the following variables:")
        for var in missing_vars:
            print(f"   {var}=your_value_here")
        print("\nExample .env file:")
        print("   GOOGLE_API_KEY=your_gemini_api_key_here")
        return False

    print("✅ All required environment variables are set")
    return True


def init_database():
    """Initialize the database."""
    print("\nInitializing database...")

    try:
        db = Database()

        # Test database connection
        teams = db.get_teams()
        print(f"✅ Database initialized with {len(teams)} teams")

        for team in teams:
            print(f"   - {team['team_name']}: {team['team_email']}")

        return True
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False


def init_rag_system():
    """Initialize the RAG system."""
    print("\nInitializing RAG system...")

    try:
        rag = RAGSystem()

        # Test RAG system
        test_query = "API error 403"
        results = rag.retrieve_response(test_query, n_results=1)

        print(f"✅ RAG system initialized with vector database")
        print(f"   Test query: '{test_query}'")
        print(f"   Retrieved {len(results)} response(s)")

        return True
    except Exception as e:
        print(f"❌ RAG system initialization failed: {e}")
        return False


def test_classifier():
    """Test the intent classifier."""
    print("\nTesting intent classifier...")

    try:
        from agents.intent_classifier import IntentClassifier

        classifier = IntentClassifier()

        test_message = "Our API is returning 403 errors"
        result = classifier.classify_intent(test_message)

        print(f"✅ Intent classifier working")
        print(f"   Test message: '{test_message}'")
        print(f"   Classified as: {result['intent']} (urgency: {result['urgency']})")
        print(f"   Assigned team: {result['assigned_team']}")

        return True
    except Exception as e:
        print(f"❌ Intent classifier test failed: {e}")
        return False


def main():
    """Run all initialization steps."""
    print("=" * 80)
    print("  Multi-Channel Customer Query Router - System Initialization")
    print("=" * 80)
    print()

    # Step 1: Check environment
    if not check_environment():
        print("\n❌ Initialization failed: Missing environment variables")
        return False

    # Step 2: Initialize database
    if not init_database():
        print("\n❌ Initialization failed: Database error")
        return False

    # Step 3: Initialize RAG system
    if not init_rag_system():
        print("\n❌ Initialization failed: RAG system error")
        return False

    # Step 4: Test classifier
    if not test_classifier():
        print("\n❌ Initialization failed: Classifier error")
        return False

    # Success!
    print()
    print("=" * 80)
    print("  ✅ SYSTEM INITIALIZATION COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    print()
    print("You can now:")
    print("   1. Run demo: python demo.py")
    print("   2. Start web app: python app.py")
    print("   3. Run batch demo: python demo.py --batch")
    print()

    return True


if __name__ == "__main__":
    import sys

    success = main()
    sys.exit(0 if success else 1)
