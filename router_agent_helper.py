#!/usr/bin/env python3
"""
RouterAgent() Utility - Automatic Ticket Routing Helper

This script demonstrates how to use RouterAgent() for automatic ticket routing.
RouterAgent() handles the entire routing pipeline automatically.
"""

import json
from typing import Dict, List, Optional

from router_agent import RouterAgent


class AutoRouterHelper:
    """
    Helper class that wraps RouterAgent() for easy automatic routing.
    Provides convenient methods for common routing tasks.
    """

    def __init__(self):
        """Initialize RouterAgent() for automatic routing."""
        self.agent = RouterAgent()
        print("✅ RouterAgent() initialized - ready for automatic routing")

    def route_ticket(
        self,
        message: str,
        sender: str = None,
        subject: str = None,
        channel: str = "form",
        auto_respond: bool = True,
    ) -> Dict:
        """
        Automatically route a ticket using RouterAgent().

        Args:
            message: Customer query message
            sender: Customer email or identifier
            subject: Optional subject line
            channel: Source channel (email, chat, form)
            auto_respond: Whether to generate automatic response

        Returns:
            Dict with routing result including ticket_id, team, urgency, etc.
        """
        print(f"\n🔄 Processing ticket via RouterAgent()...")
        print(f"   Message: {message[:60]}...")

        # RouterAgent() handles everything automatically!
        result = self.agent.process_query(
            channel=channel,
            message=message,
            sender=sender,
            subject=subject,
            auto_respond=auto_respond,
        )

        print(f"✅ Ticket automatically routed!")
        print(f"   Ticket ID: {result['ticket_id']}")
        print(f"   Team: {result['routing']['final_team']}")
        print(f"   Intent: {result['classification']['intent']}")
        print(f"   Urgency: {result['classification']['urgency']}")

        return result

    def route_multiple_tickets(self, tickets: List[Dict]) -> List[Dict]:
        """
        Automatically route multiple tickets using RouterAgent() batch processing.

        Args:
            tickets: List of ticket dicts with 'message', 'sender', 'subject', etc.

        Returns:
            List of routing results
        """
        print(f"\n🔄 Processing {len(tickets)} tickets via RouterAgent()...")

        # RouterAgent() has built-in batch processing
        results = self.agent.batch_process(tickets)

        print(f"✅ {len(results)} tickets automatically routed!")

        return results

    def get_routing_stats(self) -> Dict:
        """Get routing statistics using RouterAgent()."""
        return self.agent.get_dashboard_stats()

    def get_ticket_details(self, ticket_id: str) -> Optional[Dict]:
        """Get ticket details including routing history using RouterAgent()."""
        return self.agent.get_ticket_details(ticket_id)

    def export_routed_tickets(self, status: str = None) -> str:
        """Export routed tickets to CSV using RouterAgent()."""
        return self.agent.export_tickets(status=status)


def demonstrate_router_agent():
    """Demonstrate RouterAgent() automatic routing capabilities."""
    print("=" * 80)
    print("RouterAgent() - Automatic Routing Demonstration")
    print("=" * 80)
    print()
    print("RouterAgent() automatically handles:")
    print("  ✅ NLP classification (intent, urgency, sentiment)")
    print("  ✅ Smart routing decisions")
    print("  ✅ Ticket creation")
    print("  ✅ Escalation handling")
    print("  ✅ Learning from tickets")
    print()

    # Initialize RouterAgent()
    helper = AutoRouterHelper()

    # Example 1: Route a single ticket
    print("\n" + "=" * 80)
    print("Example 1: Route Single Ticket")
    print("=" * 80)

    result1 = helper.route_ticket(
        message="API integration keeps failing with error code 403 when we push payment data.",
        sender="dev@merchantpay.com",
        subject="API Error 403",
        channel="email",
    )

    # Example 2: Route multiple tickets
    print("\n" + "=" * 80)
    print("Example 2: Route Multiple Tickets (Batch)")
    print("=" * 80)

    tickets = [
        {
            "channel": "form",
            "message": "Our monthly invoice shows an extra $120 charge. Can you review it?",
            "sender": "billing@acmecorp.com",
            "subject": "Billing Issue",
        },
        {
            "channel": "email",
            "message": "Vendor account verification stuck on 'Pending' for 2 days.",
            "sender": "john.doe@techcorp.com",
            "subject": "Verification Stuck",
        },
        {
            "channel": "chat",
            "message": "We need SOC 2 certificate for our audit.",
            "sender": "compliance@bigcorp.com",
            "subject": None,
        },
    ]

    results = helper.route_multiple_tickets(tickets)

    # Example 3: Get routing statistics
    print("\n" + "=" * 80)
    print("Example 3: Routing Statistics")
    print("=" * 80)

    stats = helper.get_routing_stats()
    print(json.dumps(stats, indent=2))

    # Example 4: Get ticket details
    print("\n" + "=" * 80)
    print("Example 4: Get Ticket Details")
    print("=" * 80)

    if result1.get("ticket_id"):
        details = helper.get_ticket_details(result1["ticket_id"])
        if details:
            print(f"Ticket: {details['ticket']['ticket_id']}")
            print(f"Team: {details['ticket']['assigned_team']}")
            print(f"Status: {details['ticket']['status']}")
            print(f"Routing Events: {len(details.get('routing_history', []))}")

    print("\n" + "=" * 80)
    print("Summary")
    print("=" * 80)
    print("✅ RouterAgent() successfully routed all tickets automatically")
    print("✅ No manual intervention required")
    print("✅ All routing decisions made using NLP")
    print()


def quick_route_example():
    """Quick example of using RouterAgent() for automatic routing."""
    print("\n" + "=" * 80)
    print("Quick RouterAgent() Usage Example")
    print("=" * 80)
    print()

    # Simple usage - RouterAgent() does everything!
    agent = RouterAgent()

    # Route a ticket - that's it!
    result = agent.process_query(
        channel="form",
        message="API error 403 blocking our payments",
        sender="support@company.com",
        subject="Urgent: API Issue",
    )

    # Result contains everything
    print(
        f"✅ Ticket {result['ticket_id']} automatically routed to {result['routing']['final_team']}"
    )
    print(f"   Intent: {result['classification']['intent']}")
    print(f"   Urgency: {result['classification']['urgency']}")
    print(f"   Confidence: {result['classification']['confidence']:.1%}")

    return result


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        quick_route_example()
    else:
        demonstrate_router_agent()
