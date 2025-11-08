"""
Ticket management system for creating, updating, and exporting tickets.
"""

import csv
from datetime import datetime
from typing import Dict, List, Optional
import uuid
from database import Database


class TicketManager:
    def __init__(self, db: Database = None):
        """Initialize ticket manager with database connection."""
        self.db = db or Database()
    
    def create_ticket(
        self,
        channel: str,
        message: str,
        intent: str,
        urgency: str,
        assigned_team: str,
        sender: str = None,
        subject: str = None,
        response: str = None,
        metadata: Dict = None
    ) -> str:
        """
        Create a new ticket.
        
        Args:
            channel: Source channel (email, chat, form)
            message: Customer query message
            intent: Classified intent
            urgency: Urgency level (critical, high, medium, low)
            assigned_team: Team assigned to handle the ticket
            sender: Customer email or identifier
            subject: Optional subject line
            response: Optional auto-generated response
            metadata: Additional metadata
            
        Returns:
            Ticket ID
        """
        # Generate unique ticket ID
        ticket_id = self._generate_ticket_id(channel, urgency)
        
        # Prepare ticket data
        ticket_data = {
            "ticket_id": ticket_id,
            "channel": channel,
            "sender": sender,
            "subject": subject,
            "message": message,
            "intent": intent,
            "urgency": urgency,
            "assigned_team": assigned_team,
            "status": "open",
            "response": response,
            "metadata": metadata or {}
        }
        
        # Create ticket in database
        self.db.create_ticket(ticket_data)
        
        # Log creation event
        self.db.log_routing_event(
            ticket_id,
            "ticket_created",
            {
                "channel": channel,
                "intent": intent,
                "urgency": urgency,
                "assigned_team": assigned_team
            }
        )
        
        return ticket_id
    
    def _generate_ticket_id(self, channel: str, urgency: str) -> str:
        """Generate a unique ticket ID with meaningful prefix."""
        # Prefix based on channel and urgency
        channel_prefix = {
            "email": "EML",
            "chat": "CHT",
            "form": "FRM"
        }.get(channel.lower(), "TKT")
        
        urgency_prefix = {
            "critical": "C",
            "high": "H",
            "medium": "M",
            "low": "L"
        }.get(urgency.lower(), "M")
        
        # Generate unique ID
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        unique_id = str(uuid.uuid4())[:8].upper()
        
        return f"{channel_prefix}-{urgency_prefix}-{timestamp}-{unique_id}"
    
    def get_ticket(self, ticket_id: str) -> Optional[Dict]:
        """Get a ticket by ID."""
        return self.db.get_ticket(ticket_id)
    
    def get_all_tickets(self, status: Optional[str] = None) -> List[Dict]:
        """Get all tickets, optionally filtered by status."""
        return self.db.get_all_tickets(status)
    
    def update_ticket_status(self, ticket_id: str, new_status: str, notes: str = None):
        """Update ticket status."""
        self.db.update_ticket(ticket_id, {"status": new_status})
        
        # Log status change
        self.db.log_routing_event(
            ticket_id,
            "status_changed",
            {
                "new_status": new_status,
                "notes": notes
            }
        )
    
    def assign_ticket(self, ticket_id: str, team: str, reason: str = None):
        """Reassign ticket to a different team."""
        # Get original team before reassignment
        ticket = self.get_ticket(ticket_id)
        original_team = ticket.get('assigned_team') if ticket else None
        original_intent = ticket.get('intent') if ticket else None
        
        self.db.update_ticket(ticket_id, {"assigned_team": team})
        
        # Log reassignment
        self.db.log_routing_event(
            ticket_id,
            "ticket_reassigned",
            {
                "new_team": team,
                "reason": reason
            }
        )
        
        # Learn from reassignment (if learning system is available)
        try:
            from learning_system import LearningSystem
            learning = LearningSystem(self.db)
            learning.learn_from_reassignment(
                ticket_id=ticket_id,
                original_team=original_team or "Unknown",
                new_team=team,
                original_intent=original_intent,
                reason=reason
            )
        except Exception as e:
            print(f"Warning: Could not learn from reassignment: {e}")
    
    def add_response(self, ticket_id: str, response: str):
        """Add a response to a ticket."""
        self.db.update_ticket(ticket_id, {"response": response})
        
        # Log response
        self.db.log_routing_event(
            ticket_id,
            "response_added",
            {
                "response_length": len(response)
            }
        )
    
    def export_tickets_to_csv(
        self,
        filename: str = None,
        status: Optional[str] = None
    ) -> str:
        """
        Export tickets to CSV file.
        
        Args:
            filename: Output filename (default: tickets_TIMESTAMP.csv)
            status: Optional status filter
            
        Returns:
            Path to exported CSV file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"tickets_{timestamp}.csv"
        
        # Get tickets
        tickets = self.get_all_tickets(status)
        
        if not tickets:
            print("No tickets to export")
            return None
        
        # Define CSV columns
        columns = [
            "ticket_id",
            "channel",
            "sender",
            "subject",
            "message",
            "intent",
            "urgency",
            "assigned_team",
            "status",
            "created_at",
            "updated_at"
        ]
        
        # Write to CSV
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=columns)
            writer.writeheader()
            
            for ticket in tickets:
                # Select only relevant columns
                row = {col: ticket.get(col, '') for col in columns}
                writer.writerow(row)
        
        print(f"Exported {len(tickets)} tickets to {filename}")
        return filename
    
    def get_ticket_stats(self) -> Dict:
        """Get statistics about tickets."""
        all_tickets = self.get_all_tickets()
        
        stats = {
            "total_tickets": len(all_tickets),
            "by_status": {},
            "by_urgency": {},
            "by_team": {},
            "by_channel": {},
            "by_intent": {},
            "auto_responses": 0
        }
        
        for ticket in all_tickets:
            # Count by status
            status = ticket.get('status', 'unknown')
            stats['by_status'][status] = stats['by_status'].get(status, 0) + 1
            
            # Count by urgency
            urgency = ticket.get('urgency', 'unknown')
            stats['by_urgency'][urgency] = stats['by_urgency'].get(urgency, 0) + 1
            
            # Count by team
            team = ticket.get('assigned_team', 'unknown')
            stats['by_team'][team] = stats['by_team'].get(team, 0) + 1
            
            # Count by channel
            channel = ticket.get('channel', 'unknown')
            stats['by_channel'][channel] = stats['by_channel'].get(channel, 0) + 1
            
            # Count by intent
            intent = ticket.get('intent', 'unknown')
            stats['by_intent'][intent] = stats['by_intent'].get(intent, 0) + 1
            
            # Count auto-responses (tickets with response field filled)
            if ticket.get('response'):
                stats['auto_responses'] += 1
        
        return stats
    
    def get_routing_history(self, ticket_id: str) -> List[Dict]:
        """Get the complete routing history for a ticket."""
        return self.db.get_routing_events(ticket_id)
    
    def delete_ticket(self, ticket_id: str) -> bool:
        """
        Delete a ticket by ID.
        
        Args:
            ticket_id: The ticket ID to delete
            
        Returns:
            True if ticket was deleted, False if ticket not found
        """
        # Verify ticket exists before deletion
        ticket = self.get_ticket(ticket_id)
        if not ticket:
            return False
        
        # Delete the ticket (this will also delete related routing_log and learning_feedback entries)
        # Note: We don't log deletion events as they would be deleted immediately anyway
        return self.db.delete_ticket(ticket_id)

    def delete_all_tickets(self) -> int:
        """
        Delete all tickets and their related routing logs.
        
        Returns:
            Number of tickets deleted
        """
        return self.db.delete_all_tickets()


if __name__ == "__main__":
    # Test the ticket manager
    tm = TicketManager()
    
    # Create a test ticket
    ticket_id = tm.create_ticket(
        channel="email",
        message="API integration keeps failing with error code 403",
        intent="technical_support",
        urgency="high",
        assigned_team="Tech Support",
        sender="dev@merchantpay.com",
        subject="API Error 403"
    )
    
    print(f"Created ticket: {ticket_id}")
    
    # Get ticket details
    ticket = tm.get_ticket(ticket_id)
    print(f"\nTicket details:")
    for key, value in ticket.items():
        if key != 'metadata':
            print(f"  {key}: {value}")
    
    # Get stats
    print(f"\nTicket Statistics:")
    stats = tm.get_ticket_stats()
    for category, counts in stats.items():
        if category != 'total_tickets':
            print(f"  {category}: {counts}")

