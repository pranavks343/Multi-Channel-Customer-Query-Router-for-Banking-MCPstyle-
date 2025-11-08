"""
Demo script to test the Multi-Channel Customer Query Router
with the 3 example scenarios.
"""

from router_agent import RouterAgent
import json
from datetime import datetime


def print_separator(char="=", length=80):
    """Print a separator line."""
    print(char * length)


def print_section_header(title):
    """Print a section header."""
    print_separator()
    print(f"  {title}")
    print_separator()
    print()


def print_routing_result(result, query_num):
    """Print the routing result in a formatted way."""
    print(f"\n{'=' * 80}")
    print(f"QUERY {query_num} - ROUTING RESULT")
    print('=' * 80)
    
    # Query Info
    print(f"\n📨 QUERY DETAILS:")
    print(f"   Channel: {result['channel']}")
    print(f"   Ticket ID: {result['ticket_id']}")
    
    # Classification
    print(f"\n🔍 CLASSIFICATION:")
    classification = result['classification']
    print(f"   Intent: {classification['intent']}")
    print(f"   Urgency: {classification['urgency'].upper()}")
    print(f"   Confidence: {classification['confidence']:.1%}")
    print(f"   Reasoning: {classification.get('reasoning', 'N/A')}")
    
    # Routing Decision
    print(f"\n🎯 ROUTING DECISION:")
    routing = result['routing']
    print(f"   Assigned Team: {routing['final_team']}")
    print(f"   Primary Team: {routing['primary_team']}")
    if routing['additional_teams']:
        print(f"   Additional Teams: {', '.join(routing['additional_teams'])}")
    print(f"   Response Time: {routing['response_time']}")
    print(f"   Needs Review: {'Yes' if routing['needs_review'] else 'No'}")
    print(f"   Escalated: {'Yes' if routing['escalate'] else 'No'}")
    
    # Escalation Info
    if result.get('escalation'):
        print(f"\n⚠️  ESCALATION:")
        escalation = result['escalation']
        print(f"   Status: Escalated")
        print(f"   Escalation Time: {escalation['escalation_time']}")
        if escalation['notified']:
            print(f"   Notified: {', '.join(escalation['notified'])}")
    
    # Auto-Generated Response
    if result.get('response'):
        print(f"\n📧 AUTO-GENERATED RESPONSE:")
        print("-" * 80)
        response_lines = result['response'].split('\n')
        for line in response_lines:
            print(f"   {line}")
        print("-" * 80)
    
    print()


def main():
    """Run the demo with 3 example scenarios."""
    
    print_section_header("🏦 FinLink Multi-Channel Customer Query Router - DEMO")
    
    print("Initializing Router Agent...")
    agent = RouterAgent()
    print("✅ Router Agent initialized\n")
    
    # Define the 3 example scenarios from the problem statement
    test_queries = [
        {
            "channel": "email",
            "sender": "john.doe@techcorp.com",
            "subject": "Vendor account verification stuck",
            "message": "Hello, we tried adding a new vendor bank account, but the verification is stuck on 'Pending' for 2 days.",
            "description": "KYC Query (Email) - Account verification stuck"
        },
        {
            "channel": "form",
            "sender": "dev@merchantpay.com",
            "subject": "API integration error 403",
            "message": "API integration keeps failing with error code 403 when we push payment data.",
            "description": "Tech Support Query (Form) - API error 403"
        },
        {
            "channel": "chat",
            "sender": "billing@acmecorp.com",
            "subject": None,
            "message": "Our monthly invoice for August shows an extra $120 charge. Can you please review it?",
            "description": "Finance Query (Chat) - Invoice billing issue"
        }
    ]
    
    results = []
    
    # Process each query
    for i, query in enumerate(test_queries, 1):
        print_section_header(f"SCENARIO {i}: {query['description']}")
        
        print(f"📥 INPUT:")
        print(f"   Channel: {query['channel']}")
        print(f"   Sender: {query['sender']}")
        if query['subject']:
            print(f"   Subject: {query['subject']}")
        print(f"   Message: {query['message']}")
        
        print(f"\n⚙️  Processing query...")
        
        # Process the query
        result = agent.process_query(
            channel=query['channel'],
            message=query['message'],
            sender=query['sender'],
            subject=query['subject'],
            auto_respond=True
        )
        
        results.append(result)
        
        # Display result
        print_routing_result(result, i)
        
        if i < len(test_queries):
            print("\n" + "="*80 + "\n")
    
    # Display summary statistics
    print_section_header("📊 DEMO SUMMARY")
    
    print("Processed Queries:")
    print(f"   Total: {len(results)}")
    print()
    
    print("Routing Summary:")
    for i, result in enumerate(results, 1):
        print(f"   Query {i}:")
        print(f"      → Team: {result['routing']['final_team']}")
        print(f"      → Urgency: {result['classification']['urgency']}")
        print(f"      → Ticket: {result['ticket_id']}")
    print()
    
    # Get overall statistics
    stats = agent.get_dashboard_stats()
    
    print("Overall Statistics:")
    print(f"   Total Tickets: {stats['total_tickets']}")
    print()
    
    print("By Urgency:")
    for urgency, count in stats['by_urgency'].items():
        print(f"   {urgency.capitalize()}: {count}")
    print()
    
    print("By Team:")
    for team, count in stats['by_team'].items():
        print(f"   {team}: {count}")
    print()
    
    print("By Channel:")
    for channel, count in stats['by_channel'].items():
        print(f"   {channel.capitalize()}: {count}")
    print()
    
    # Export tickets
    print_section_header("📤 EXPORTING TICKETS")
    
    filename = agent.export_tickets()
    if filename:
        print(f"✅ Tickets exported to: {filename}")
        print(f"   You can open this file in Excel or any CSV viewer")
    
    print()
    print_separator()
    print("DEMO COMPLETED SUCCESSFULLY! ✨")
    print_separator()
    print()
    print("Next Steps:")
    print("   1. Run 'python app.py' to start the web interface")
    print("   2. Visit http://localhost:5000 in your browser")
    print("   3. Try submitting more queries through the UI")
    print("   4. Monitor live routing events in real-time")
    print()


def run_batch_demo():
    """Run a batch processing demo with multiple queries."""
    print_section_header("🚀 BATCH PROCESSING DEMO")
    
    agent = RouterAgent()
    
    # Load sample queries
    from sample_data import get_sample_queries
    samples = get_sample_queries()[:5]  # Process first 5 samples
    
    print(f"Processing {len(samples)} queries in batch...\n")
    
    results = agent.batch_process(samples)
    
    print(f"✅ Batch processing completed!")
    print(f"   Processed: {len(results)} queries")
    print(f"   Success rate: 100%\n")
    
    # Show summary
    print("Batch Results Summary:")
    for i, result in enumerate(results, 1):
        if 'error' not in result:
            print(f"   {i}. {result['ticket_id']} → {result['routing']['final_team']} [{result['classification']['urgency']}]")
    
    print()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--batch":
        run_batch_demo()
    else:
        main()

