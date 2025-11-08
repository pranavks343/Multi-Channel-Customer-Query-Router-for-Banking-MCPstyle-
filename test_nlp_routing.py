#!/usr/bin/env python3
"""
Test script to demonstrate enhanced NLP routing capabilities.
Shows how the system understands messages semantically and routes them accurately.
"""

from router_agent import RouterAgent
import json

def test_nlp_routing():
    """Test the enhanced NLP routing system."""
    print("=" * 80)
    print("Enhanced NLP Routing Test")
    print("=" * 80)
    print()
    
    agent = RouterAgent()
    
    # Test cases that demonstrate semantic understanding
    test_cases = [
        {
            "name": "Billing Dispute Detection",
            "channel": "email",
            "sender": "billing@acmecorp.com",
            "subject": "Incorrect charge on invoice",
            "message": "Our August invoice shows a charge of $500 that we didn't authorize. This is incorrect and we need this resolved immediately.",
            "expected_intent": "compliance_regulatory",  # Disputes go to compliance
            "expected_urgency": "high"
        },
        {
            "name": "Technical API Error",
            "channel": "form",
            "sender": "dev@merchantpay.com",
            "subject": "API integration error 403",
            "message": "Our payment integration is failing with error code 403. This is blocking all our transactions and affecting our business operations.",
            "expected_intent": "technical_support",
            "expected_urgency": "high"
        },
        {
            "name": "Verification Stuck",
            "channel": "email",
            "sender": "john.doe@techcorp.com",
            "subject": "Vendor account verification stuck",
            "message": "We tried adding a new vendor bank account, but the verification has been stuck on 'Pending' for 2 days. This is blocking our payment processing.",
            "expected_intent": "kyc_verification",
            "expected_urgency": "high"
        },
        {
            "name": "General Information Request",
            "channel": "chat",
            "sender": "info@startup.com",
            "subject": None,
            "message": "Hi, I'm just wondering how your API rate limits work. Can you provide some information?",
            "expected_intent": "general_support",
            "expected_urgency": "low"
        },
        {
            "name": "Sales Inquiry",
            "channel": "form",
            "sender": "ceo@enterprise.com",
            "subject": "Enterprise pricing inquiry",
            "message": "We're interested in your enterprise plan and would like to schedule a demo. We're a large company with 500+ employees.",
            "expected_intent": "sales_inquiry",
            "expected_urgency": "medium"
        },
        {
            "name": "Compliance Certificate Request",
            "channel": "email",
            "sender": "compliance@bigcorp.com",
            "subject": "SOC 2 certificate needed",
            "message": "We need your SOC 2 Type II certificate for our annual audit. This is required for our compliance review.",
            "expected_intent": "compliance_regulatory",
            "expected_urgency": "medium"
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'=' * 80}")
        print(f"Test {i}: {test_case['name']}")
        print('-' * 80)
        print(f"Message: {test_case['message'][:100]}...")
        print()
        
        # Process the query
        result = agent.process_query(
            channel=test_case['channel'],
            message=test_case['message'],
            sender=test_case['sender'],
            subject=test_case['subject'],
            auto_respond=False  # Skip response generation for testing
        )
        
        # Display results
        classification = result['classification']
        routing = result['routing']
        
        print(f"✓ Intent: {classification['intent']}")
        print(f"  Expected: {test_case['expected_intent']}")
        print(f"  Match: {'✅' if classification['intent'] == test_case['expected_intent'] else '❌'}")
        
        print(f"\n✓ Urgency: {classification['urgency']}")
        print(f"  Expected: {test_case['expected_urgency']}")
        print(f"  Match: {'✅' if classification['urgency'] == test_case['expected_urgency'] else '❌'}")
        
        print(f"\n✓ Confidence: {classification['confidence']:.2%}")
        print(f"✓ Sentiment: {classification.get('sentiment', 'N/A')}")
        print(f"✓ Key Entities: {classification.get('key_entities', [])}")
        print(f"✓ Assigned Team: {routing['final_team']}")
        print(f"✓ Reasoning: {classification.get('reasoning', 'N/A')[:150]}...")
        
        # Store result
        results.append({
            "test": test_case['name'],
            "intent_match": classification['intent'] == test_case['expected_intent'],
            "urgency_match": classification['urgency'] == test_case['expected_urgency'],
            "confidence": classification['confidence'],
            "sentiment": classification.get('sentiment'),
            "key_entities": classification.get('key_entities', [])
        })
    
    # Summary
    print(f"\n{'=' * 80}")
    print("Test Summary")
    print('=' * 80)
    
    intent_matches = sum(1 for r in results if r['intent_match'])
    urgency_matches = sum(1 for r in results if r['urgency_match'])
    
    print(f"Intent Accuracy: {intent_matches}/{len(results)} ({intent_matches/len(results)*100:.1f}%)")
    print(f"Urgency Accuracy: {urgency_matches}/{len(results)} ({urgency_matches/len(results)*100:.1f}%)")
    print(f"Average Confidence: {sum(r['confidence'] for r in results)/len(results):.2%}")
    
    print("\nNLP Features Demonstrated:")
    print("  ✓ Semantic understanding of messages")
    print("  ✓ Entity extraction (error codes, amounts, dates)")
    print("  ✓ Sentiment analysis")
    print("  ✓ Context-aware urgency detection")
    print("  ✓ Intelligent routing based on NLP insights")
    
    return results

if __name__ == "__main__":
    test_nlp_routing()

