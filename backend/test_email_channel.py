#!/usr/bin/env python3
"""
Test script for Email Channel with NLP Classification

This script demonstrates how to use the new email channel endpoint
that automatically classifies emails using NLP based on the subject
and message body.
"""

import json
from datetime import datetime

import requests

BASE_URL = "http://localhost:8000"


def test_email_classification():
    """Test email channel with various types of emails to demonstrate NLP classification."""

    test_emails = [
        {
            "name": "Technical Support Email",
            "from": "dev@company.com",
            "subject": "API Error 403 - Payment Integration Failing",
            "body": "Our payment integration is failing with error code 403. This is blocking all our transactions and affecting our business operations. We need immediate assistance.",
            "expected_category": "technical_support",
            "expected_urgency": "high",
        },
        {
            "name": "KYC Verification Email",
            "from": "customer@business.com",
            "subject": "Account Verification Stuck",
            "body": "We submitted our KYC documents 3 days ago but the verification is still pending. We can't process any payments until our account is verified. Please help us resolve this urgently.",
            "expected_category": "kyc_verification",
            "expected_urgency": "high",
        },
        {
            "name": "Billing Dispute Email",
            "from": "finance@company.com",
            "subject": "Billing Dispute - Incorrect Charge",
            "body": "Our August invoice shows a charge of $500 that we didn't authorize. This is incorrect and we need this resolved immediately. We dispute this charge.",
            "expected_category": "compliance_regulatory",  # Disputes go to compliance
            "expected_urgency": "high",
        },
        {
            "name": "Sales Inquiry Email",
            "from": "prospect@enterprise.com",
            "subject": "Enterprise Pricing Inquiry",
            "body": "We're interested in your enterprise plan and would like to schedule a demo. Can you provide pricing information for 500+ users?",
            "expected_category": "sales_inquiry",
            "expected_urgency": "medium",
        },
        {
            "name": "General Support Email",
            "from": "user@company.com",
            "subject": "How to use webhooks?",
            "body": "I'm trying to set up webhooks for our integration. Can you point me to the documentation or provide some guidance?",
            "expected_category": "general_support",
            "expected_urgency": "low",
        },
    ]

    print("=" * 80)
    print("Email Channel NLP Classification Test")
    print("=" * 80)
    print(f"Testing endpoint: {BASE_URL}/api/submit_email\n")

    results = []

    for i, email in enumerate(test_emails, 1):
        print(f"\n{'='*80}")
        print(f"Test {i}: {email['name']}")
        print(f"{'='*80}")
        print(f"From: {email['from']}")
        print(f"Subject: {email['subject']}")
        print(f"Body: {email['body'][:100]}...")
        print()

        try:
            # Submit email via the email channel endpoint
            response = requests.post(
                f"{BASE_URL}/api/submit_email",
                json={
                    "from": email["from"],
                    "subject": email["subject"],
                    "body": email["body"],
                    "auto_respond": True,
                },
                headers={"Content-Type": "application/json"},
            )

            if response.status_code == 200:
                data = response.json()
                result = data.get("result", {})
                classification = result.get("classification", {})
                routing = result.get("routing", {})

                # Display results
                print("✅ Email processed successfully!")
                print(f"\nNLP Classification Results:")
                print(f"  Category/Intent: {classification.get('category', 'N/A')}")
                print(f"  Urgency: {classification.get('urgency', 'N/A')}")
                print(f"  Confidence: {classification.get('confidence', 0):.2%}")
                print(f"  Sentiment: {classification.get('sentiment', 'N/A')}")
                print(
                    f"  Key Entities: {', '.join(classification.get('key_entities', []))}"
                )
                print(f"  Reasoning: {classification.get('reasoning', 'N/A')[:150]}...")

                print(f"\nRouting Decision:")
                print(f"  Assigned Team: {routing.get('assigned_team', 'N/A')}")
                print(f"  Escalate: {routing.get('escalate', False)}")

                print(f"\nTicket Info:")
                print(f"  Ticket ID: {result.get('ticket_id', 'N/A')}")

                # Verify expectations
                actual_category = classification.get("category", "")
                actual_urgency = classification.get("urgency", "")

                category_match = actual_category == email["expected_category"]
                urgency_match = actual_urgency == email["expected_urgency"]

                if category_match and urgency_match:
                    print(f"\n✅ Classification matches expectations!")
                else:
                    print(f"\n⚠️  Classification differs:")
                    if not category_match:
                        print(
                            f"   Expected category: {email['expected_category']}, Got: {actual_category}"
                        )
                    if not urgency_match:
                        print(
                            f"   Expected urgency: {email['expected_urgency']}, Got: {actual_urgency}"
                        )

                results.append(
                    {
                        "test": email["name"],
                        "success": True,
                        "category": actual_category,
                        "urgency": actual_urgency,
                        "ticket_id": result.get("ticket_id"),
                    }
                )
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Response: {response.text}")
                results.append(
                    {"test": email["name"], "success": False, "error": response.text}
                )

        except Exception as e:
            print(f"❌ Exception: {str(e)}")
            results.append({"test": email["name"], "success": False, "error": str(e)})

    # Summary
    print(f"\n\n{'='*80}")
    print("Test Summary")
    print(f"{'='*80}")
    successful = sum(1 for r in results if r.get("success"))
    print(f"Successful: {successful}/{len(results)}")

    for result in results:
        status = "✅" if result.get("success") else "❌"
        print(f"{status} {result['test']}")
        if result.get("success"):
            print(
                f"   → Category: {result.get('category')}, Urgency: {result.get('urgency')}"
            )

    return results


if __name__ == "__main__":
    print("\nMake sure the Flask app is running on port 8000")
    print("Start it with: python app.py 8000\n")

    try:
        # Check if server is running
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        if response.status_code == 200:
            test_email_classification()
        else:
            print(f"❌ Server health check failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to {BASE_URL}")
        print("Please make sure the Flask app is running:")
        print("  python app.py 8000")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
