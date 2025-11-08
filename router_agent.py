"""
Main Router Agent that orchestrates the entire query routing process.
Integrates intent classification, RAG, and ticket management.
"""

from typing import Dict, List, Optional
from intent_classifier import IntentClassifier
from rag_system import RAGSystem
from ticket_manager import TicketManager
from database import Database
from learning_system import LearningSystem
import json


class RouterAgent:
    def __init__(self):
        """Initialize the Router Agent with all components."""
        self.db = Database()
        self.learning_system = LearningSystem(self.db)
        self.classifier = IntentClassifier(learning_system=self.learning_system)
        self.rag = RAGSystem()
        self.ticket_manager = TicketManager(self.db)
        
        # Define escalation rules
        self.escalation_rules = {
            "critical": {
                "response_time": "immediate",
                "notify": ["team_lead", "manager"],
                "auto_escalate": True
            },
            "high": {
                "response_time": "4 hours",
                "notify": ["team_lead"],
                "auto_escalate": False
            },
            "medium": {
                "response_time": "24 hours",
                "notify": [],
                "auto_escalate": False
            },
            "low": {
                "response_time": "48 hours",
                "notify": [],
                "auto_escalate": False
            }
        }
    
    def process_query(
        self,
        channel: str,
        message: str,
        sender: str = None,
        subject: str = None,
        auto_respond: bool = True,
        extra_metadata: Dict = None
    ) -> Dict:
        """
        Process a customer query through the complete routing pipeline.
        
        Args:
            channel: Source channel (email, chat, form)
            message: Customer query message
            sender: Customer email or identifier
            subject: Optional subject line
            auto_respond: Whether to generate an automatic response
            extra_metadata: Optional dict with channel-specific metadata (attachments, user_id, etc.)
            
        Returns:
            Dict with routing decision, ticket info, and response
        """
        # Step 1: Classify intent and urgency
        classification = self.classifier.classify_intent(message, subject)
        
        intent = classification['intent']
        urgency = classification['urgency']
        assigned_team = classification.get('assigned_team', 'Tech Support')
        confidence = classification.get('confidence', 0.0)
        reasoning = classification.get('reasoning', '')
        key_entities = classification.get('key_entities', [])
        sentiment = classification.get('sentiment', 'neutral')
        
        # Step 2: Determine routing decision first (needed for response generation)
        routing_decision = self._make_routing_decision(
            intent,
            urgency,
            confidence,
            assigned_team,
            sentiment=sentiment,
            key_entities=key_entities
        )
        
        # Step 3: Generate response if requested
        response = None
        response_metadata = {}
        if auto_respond:
            response_data = self.rag.generate_response(
                query=message,
                intent=intent,
                urgency=urgency,
                customer_name=self._extract_name(sender),
                reasoning=reasoning,
                key_entities=key_entities,
                sentiment=sentiment,
                assigned_team=routing_decision['final_team'],
                response_time=routing_decision['response_time']
            )
            response = response_data['response']
            response_metadata = {
                "method": response_data['method'],
                "templates_used": response_data['canned_templates_used']
            }
        
        # Step 4: Create ticket with enhanced NLP metadata
        ticket_metadata = {
            "classification": classification,
            "routing_decision": routing_decision,
            "response_metadata": response_metadata,
            "nlp_insights": {
                "key_entities": key_entities,
                "sentiment": sentiment,
                "reasoning": reasoning
            }
        }
        
        # Merge any extra metadata (channel-specific fields)
        if extra_metadata:
            ticket_metadata.update(extra_metadata)
        
        ticket_id = self.ticket_manager.create_ticket(
            channel=channel,
            message=message,
            intent=intent,
            urgency=urgency,
            assigned_team=routing_decision['final_team'],
            sender=sender,
            subject=subject,
            response=response,
            metadata=ticket_metadata
        )
        
        # Step 5: Handle escalation if needed
        escalation_info = None
        if routing_decision['escalate']:
            escalation_info = self._handle_escalation(
                ticket_id,
                urgency,
                routing_decision
            )
        
        # Step 6: Log the complete routing process
        self.db.log_routing_event(
            ticket_id,
            "routing_completed",
            {
                "classification": classification,
                "routing_decision": routing_decision,
                "auto_respond": auto_respond,
                "escalation": escalation_info
            }
        )
        
        # Step 7: Learn from this ticket (dynamic update)
        try:
            ticket = self.ticket_manager.get_ticket(ticket_id)
            if ticket:
                self.learning_system.learn_from_ticket(ticket)
                # Periodically refresh classifier with learned patterns
                # (every 10 tickets to avoid performance impact)
                if len(self.db.get_all_tickets()) % 10 == 0:
                    self.classifier.update_from_learning()
        except Exception as e:
            print(f"Warning: Learning system error: {e}")
        
        # Return comprehensive result with NLP insights
        return {
            "ticket_id": ticket_id,
            "channel": channel,
            "classification": {
                "intent": intent,
                "urgency": urgency,
                "confidence": confidence,
                "reasoning": reasoning,
                "key_entities": key_entities,
                "sentiment": sentiment
            },
            "routing": routing_decision,
            "response": response,
            "escalation": escalation_info,
            "status": "routed"
        }
    
    def _make_routing_decision(
        self,
        intent: str,
        urgency: str,
        confidence: float,
        assigned_team: str,
        sentiment: str = 'neutral',
        key_entities: list = None
    ) -> Dict:
        """
        Make intelligent routing decisions based on classification and NLP insights.
        
        Returns routing decision with team assignment and escalation rules.
        """
        # Ensure key_entities is a list
        if key_entities is None:
            key_entities = []
        
        # Adjust urgency based on sentiment if needed
        # Urgent sentiment can elevate medium to high
        if sentiment == 'urgent' and urgency == 'medium':
            urgency = 'high'
        # Negative sentiment with high urgency might indicate critical
        elif sentiment == 'negative' and urgency == 'high':
            # Check if there are critical entities (error codes, security terms)
            critical_entities = ['error_', 'security', 'breach', 'down', 'blocked']
            if any(ce in str(key_entities).lower() for ce in critical_entities):
                urgency = 'critical'
        
        # Get escalation rules for this urgency
        escalation = self.escalation_rules.get(urgency, self.escalation_rules['medium'])
        
        # Determine if manual review is needed (low confidence)
        needs_review = confidence < 0.6
        
        # Determine if escalation is needed
        should_escalate = (
            urgency in ['critical', 'high'] or
            needs_review or
            escalation.get('auto_escalate', False)
        )
        
        # Handle multi-team scenarios and special routing rules
        additional_teams = []
        if intent == "technical_support" and urgency == "critical":
            additional_teams.append("Tech Lead")
        elif intent == "compliance_regulatory":
            additional_teams.append("Legal Team")
        
        # Final team assignment with special cases
        final_team = assigned_team
        
        # Billing disputes route to Compliance Team (as per examples)
        if intent == "billing_finance":
            # Check if it's a dispute/discrepancy using NLP insights
            if key_entities and isinstance(key_entities, list):
                dispute_indicators = ['dispute', 'discrepancy', 'wrong', 'incorrect', 'error']
                entities_str = ' '.join(str(e) for e in key_entities).lower()
                if any(indicator in entities_str for indicator in dispute_indicators):
                    final_team = "Compliance Team"
            # Also check sentiment - negative sentiment on billing often indicates dispute
            if sentiment in ['negative', 'urgent']:
                final_team = "Compliance Team"
        
        if needs_review:
            final_team = "Triage Team"  # Route to triage if confidence is low
        
        return {
            "final_team": final_team,
            "primary_team": assigned_team,
            "additional_teams": additional_teams,
            "escalate": should_escalate,
            "needs_review": needs_review,
            "response_time": escalation['response_time'],
            "notify": escalation['notify'],
            "reasoning": self._get_routing_reasoning(
                intent, urgency, confidence, needs_review
            )
        }
    
    def _get_routing_reasoning(
        self,
        intent: str,
        urgency: str,
        confidence: float,
        needs_review: bool
    ) -> str:
        """Generate human-readable reasoning for routing decision."""
        reasons = []
        
        reasons.append(f"Intent classified as '{intent}' with {confidence:.0%} confidence")
        reasons.append(f"Urgency level: {urgency}")
        
        if needs_review:
            reasons.append("Low confidence - routing to triage for manual review")
        
        if urgency == "critical":
            reasons.append("Critical urgency - immediate attention required")
        elif urgency == "high":
            reasons.append("High urgency - priority handling needed")
        
        return ". ".join(reasons)
    
    def _handle_escalation(
        self,
        ticket_id: str,
        urgency: str,
        routing_decision: Dict
    ) -> Dict:
        """Handle ticket escalation based on urgency and rules."""
        escalation_info = {
            "escalated": True,
            "urgency": urgency,
            "notified": routing_decision['notify'],
            "escalation_time": "immediate" if urgency == "critical" else "4 hours"
        }
        
        # Log escalation event
        self.db.log_routing_event(
            ticket_id,
            "ticket_escalated",
            escalation_info
        )
        
        return escalation_info
    
    def _extract_name(self, sender: str) -> Optional[str]:
        """Extract customer name from email address."""
        if not sender:
            return None
        
        # Try to extract name from email (before @)
        if '@' in sender:
            local_part = sender.split('@')[0]
            # Convert john.doe to John Doe
            name_parts = local_part.replace('.', ' ').replace('_', ' ').split()
            return ' '.join(word.capitalize() for word in name_parts)
        
        return None
    
    def batch_process(self, queries: List[Dict]) -> List[Dict]:
        """
        Process multiple queries in batch.
        
        Args:
            queries: List of query dicts with channel, message, sender, subject
            
        Returns:
            List of routing results
        """
        results = []
        
        for query in queries:
            try:
                result = self.process_query(
                    channel=query.get('channel', 'email'),
                    message=query['message'],
                    sender=query.get('sender'),
                    subject=query.get('subject'),
                    auto_respond=query.get('auto_respond', True)
                )
                results.append(result)
            except Exception as e:
                print(f"Error processing query: {e}")
                results.append({
                    "error": str(e),
                    "query": query
                })
        
        return results
    
    def get_ticket_details(self, ticket_id: str) -> Optional[Dict]:
        """Get complete details for a ticket including routing history."""
        ticket = self.ticket_manager.get_ticket(ticket_id)
        if not ticket:
            return None
        
        # Get routing history
        history = self.ticket_manager.get_routing_history(ticket_id)
        
        return {
            "ticket": ticket,
            "routing_history": history
        }
    
    def get_dashboard_stats(self) -> Dict:
        """Get statistics for dashboard display."""
        return self.ticket_manager.get_ticket_stats()
    
    def export_tickets(self, filename: str = None, status: str = None) -> str:
        """Export tickets to CSV."""
        return self.ticket_manager.export_tickets_to_csv(filename, status)


if __name__ == "__main__":
    # Test the router agent
    agent = RouterAgent()
    
    print("=" * 80)
    print("Testing Router Agent")
    print("=" * 80)
    
    # Test with sample queries
    test_queries = [
        {
            "channel": "email",
            "sender": "john.doe@techcorp.com",
            "subject": "Vendor account verification stuck",
            "message": "Hello, we tried adding a new vendor bank account, but the verification is stuck on 'Pending' for 2 days."
        },
        {
            "channel": "form",
            "sender": "dev@merchantpay.com",
            "subject": "API integration error 403",
            "message": "API integration keeps failing with error code 403 when we push payment data."
        },
        {
            "channel": "chat",
            "sender": "billing@acmecorp.com",
            "subject": None,
            "message": "Our monthly invoice for August shows an extra $120 charge. Can you please review it?"
        }
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'=' * 80}")
        print(f"Query {i}: {query['subject'] or 'Chat Message'}")
        print(f"Channel: {query['channel']}")
        print(f"Message: {query['message'][:80]}...")
        print('-' * 80)
        
        result = agent.process_query(
            channel=query['channel'],
            message=query['message'],
            sender=query['sender'],
            subject=query['subject']
        )
        
        print(f"\nRouting Result:")
        print(f"  Ticket ID: {result['ticket_id']}")
        print(f"  Intent: {result['classification']['intent']}")
        print(f"  Urgency: {result['classification']['urgency']}")
        print(f"  Confidence: {result['classification']['confidence']:.2%}")
        print(f"  Assigned Team: {result['routing']['final_team']}")
        print(f"  Response Time: {result['routing']['response_time']}")
        print(f"  Needs Review: {result['routing']['needs_review']}")
        print(f"\nReasoning: {result['routing']['reasoning']}")
        
        if result['response']:
            print(f"\nAuto-Generated Response:")
            print(f"  {result['response'][:200]}...")
    
    # Show statistics
    print(f"\n{'=' * 80}")
    print("Dashboard Statistics:")
    print('=' * 80)
    stats = agent.get_dashboard_stats()
    print(json.dumps(stats, indent=2))

