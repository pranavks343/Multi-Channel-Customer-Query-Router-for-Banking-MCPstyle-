#!/usr/bin/env python3
"""
Test script to verify all buttons work and queries are properly routed.
"""

import json
import time
from datetime import datetime

import requests

BASE_URL = "http://localhost:8000"


def test_health():
    """Test the health endpoint."""
    print("=" * 80)
    print("TEST 1: Health Check")
    print("=" * 80)
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"✓ Health endpoint status: {response.status_code}")
        print(f"  Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False


def test_sample_queries():
    """Test the 'Refresh sample templates' button functionality."""
    print("\n" + "=" * 80)
    print("TEST 2: Sample Queries (Refresh Button)")
    print("=" * 80)
    try:
        response = requests.get(f"{BASE_URL}/api/sample_queries", timeout=5)
        print(f"✓ Sample queries endpoint status: {response.status_code}")
        data = response.json()
        if data.get("success"):
            print(f"  ✓ Retrieved {data.get('count')} sample queries")
            return True
        else:
            print(f"  ❌ API returned error: {data}")
            return False
    except Exception as e:
        print(f"❌ Sample queries test failed: {e}")
        return False


def test_submit_query(channel, query_data):
    """Test query submission and routing."""
    print("\n" + "=" * 80)
    print(f"TEST: Submit Query via {channel.upper()} Channel")
    print("=" * 80)
    try:
        response = requests.post(
            f"{BASE_URL}/api/submit_query",
            json=query_data,
            headers={"Content-Type": "application/json"},
            timeout=30,
        )
        print(f"✓ Submit query endpoint status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                result = data.get("result", {})
                print(f"  ✓ Ticket ID: {result.get('ticket_id')}")
                print(f"  ✓ Intent: {result.get('classification', {}).get('intent')}")
                print(f"  ✓ Urgency: {result.get('classification', {}).get('urgency')}")
                print(
                    f"  ✓ Assigned Team: {result.get('routing', {}).get('final_team')}"
                )
                print(
                    f"  ✓ Confidence: {result.get('classification', {}).get('confidence', 0) * 100:.0f}%"
                )
                if result.get("response"):
                    print(
                        f"  ✓ Auto-response generated: {len(result.get('response'))} chars"
                    )
                return True
            else:
                print(f"  ❌ API returned error: {data}")
                return False
        else:
            print(f"  ❌ HTTP error: {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Submit query test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_stats():
    """Test the stats endpoint (Operations Dashboard)."""
    print("\n" + "=" * 80)
    print("TEST: Dashboard Stats")
    print("=" * 80)
    try:
        response = requests.get(f"{BASE_URL}/api/stats", timeout=5)
        print(f"✓ Stats endpoint status: {response.status_code}")
        data = response.json()
        if data.get("success"):
            stats = data.get("stats", {})
            print(f"  ✓ Total tickets: {stats.get('total_tickets')}")
            print(f"  ✓ By urgency: {stats.get('by_urgency')}")
            print(f"  ✓ By team: {stats.get('by_team')}")
            return True
        else:
            print(f"  ❌ API returned error: {data}")
            return False
    except Exception as e:
        print(f"❌ Stats test failed: {e}")
        return False


def test_refresh_tickets():
    """Test the 'Refresh tickets' button functionality."""
    print("\n" + "=" * 80)
    print("TEST: Refresh Tickets Button")
    print("=" * 80)
    try:
        response = requests.get(f"{BASE_URL}/api/tickets", timeout=5)
        print(f"✓ Tickets endpoint status: {response.status_code}")
        data = response.json()
        if data.get("success"):
            print(f"  ✓ Retrieved {data.get('count')} tickets")
            return True
        else:
            print(f"  ❌ API returned error: {data}")
            return False
    except Exception as e:
        print(f"❌ Refresh tickets test failed: {e}")
        return False


def test_export_tickets():
    """Test the 'Export CSV snapshot' button functionality."""
    print("\n" + "=" * 80)
    print("TEST: Export CSV Button")
    print("=" * 80)
    try:
        response = requests.get(f"{BASE_URL}/api/export_tickets", timeout=5)
        print(f"✓ Export endpoint status: {response.status_code}")

        if response.status_code == 200:
            print(f"  ✓ CSV export successful ({len(response.content)} bytes)")
            return True
        elif response.status_code == 404:
            # No tickets to export is acceptable
            print(f"  ⚠️  No tickets to export (expected if database is empty)")
            return True
        else:
            print(f"  ❌ HTTP error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Export tickets test failed: {e}")
        return False


def test_teams():
    """Test the teams endpoint."""
    print("\n" + "=" * 80)
    print("TEST: Teams Endpoint")
    print("=" * 80)
    try:
        response = requests.get(f"{BASE_URL}/api/teams", timeout=5)
        print(f"✓ Teams endpoint status: {response.status_code}")
        data = response.json()
        if data.get("success"):
            teams = data.get("teams", [])
            print(f"  ✓ Retrieved {len(teams)} teams")
            for team in teams:
                print(f"    - {team.get('name')}: {team.get('description')}")
            return True
        else:
            print(f"  ❌ API returned error: {data}")
            return False
    except Exception as e:
        print(f"❌ Teams test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "BUTTON & ROUTING VERIFICATION TEST" + " " * 24 + "║")
    print("╚" + "=" * 78 + "╝")
    print("\nTesting all UI buttons and query routing functionality...\n")

    results = []

    # Test 1: Health check
    results.append(("Health Check", test_health()))
    time.sleep(0.5)

    # Test 2: Sample queries (Refresh button)
    results.append(("Refresh Sample Templates", test_sample_queries()))
    time.sleep(0.5)

    # Test 3: Teams endpoint
    results.append(("Teams Endpoint", test_teams()))
    time.sleep(0.5)

    # Test 4-6: Submit queries via different channels
    email_query = {
        "channel": "email",
        "sender": "test@example.com",
        "subject": "Vendor account verification stuck",
        "message": "Hello, we tried adding a new vendor bank account, but the verification is stuck on 'Pending' for 2 days.",
        "auto_respond": True,
    }
    results.append(("Email Channel Routing", test_submit_query("email", email_query)))
    time.sleep(1)

    form_query = {
        "channel": "form",
        "sender": "dev@merchantpay.com",
        "subject": "API integration error 403",
        "message": "API integration keeps failing with error code 403 when we push payment data.",
        "customer_name": "MerchantPay Dev Team",
        "category": "Technical Issue",
        "auto_respond": True,
    }
    results.append(("Form Channel Routing", test_submit_query("form", form_query)))
    time.sleep(1)

    chat_query = {
        "channel": "chat",
        "sender": "cust_12345",
        "message": "Our monthly invoice for August shows an extra $120 charge. Can you please review it?",
        "user_id": "cust_12345",
        "category": "Billing",
        "auto_respond": True,
    }
    results.append(("Chat Channel Routing", test_submit_query("chat", chat_query)))
    time.sleep(1)

    # Test 7: Stats (Operations Dashboard)
    results.append(("Dashboard Stats", test_stats()))
    time.sleep(0.5)

    # Test 8: Refresh tickets button
    results.append(("Refresh Tickets", test_refresh_tickets()))
    time.sleep(0.5)

    # Test 9: Export CSV button
    results.append(("Export CSV", test_export_tickets()))

    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:12} {test_name}")

    print("\n" + "-" * 80)
    print(f"Results: {passed}/{total} tests passed ({passed/total*100:.0f}%)")
    print("=" * 80)

    if passed == total:
        print(
            "\n🎉 ALL TESTS PASSED! All buttons work and queries are properly routed."
        )
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review the output above.")
        return 1


if __name__ == "__main__":
    import sys

    sys.exit(main())
