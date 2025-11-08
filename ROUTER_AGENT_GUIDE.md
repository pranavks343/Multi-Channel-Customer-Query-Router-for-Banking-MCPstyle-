# RouterAgent() - Complete Guide for Automatic Routing

## Overview

`RouterAgent()` is the main class that handles **automatic ticket routing** using NLP. It orchestrates the entire routing pipeline without requiring manual intervention.

## Quick Start

### Basic Usage

```python
from router_agent import RouterAgent

# Initialize RouterAgent()
agent = RouterAgent()

# Route a ticket automatically - that's it!
result = agent.process_query(
    channel="form",
    message="API error 403 blocking our payments",
    sender="support@company.com",
    subject="Urgent: API Issue"
)

# Result contains routing information
print(f"Ticket {result['ticket_id']} routed to {result['routing']['final_team']}")
```

## RouterAgent() Methods

### 1. `process_query()` - Main Routing Method

**Automatically routes a single ticket.**

```python
result = agent.process_query(
    channel="form",              # Source: "email", "chat", or "form"
    message="Customer message",   # Required: The query text
    sender="email@example.com",  # Optional: Customer identifier
    subject="Subject line",      # Optional: Subject/title
    auto_respond=True,            # Optional: Generate auto-response
    extra_metadata={}            # Optional: Additional metadata
)
```

**Returns:**
```python
{
    "ticket_id": "FRM-H-20241108-ABC123",
    "channel": "form",
    "classification": {
        "intent": "technical_support",
        "urgency": "high",
        "confidence": 0.85,
        "reasoning": "Detected API error...",
        "key_entities": ["error_403", "API"],
        "sentiment": "negative"
    },
    "routing": {
        "final_team": "Tech Support",
        "escalate": True,
        "response_time": "4 hours",
        "needs_review": False
    },
    "response": "Auto-generated response...",
    "status": "routed"
}
```

### 2. `batch_process()` - Route Multiple Tickets

**Automatically routes multiple tickets at once.**

```python
tickets = [
    {
        "channel": "email",
        "message": "API error 403",
        "sender": "dev@company.com",
        "subject": "API Issue"
    },
    {
        "channel": "form",
        "message": "Billing dispute",
        "sender": "billing@company.com"
    }
]

results = agent.batch_process(tickets)
# Returns list of routing results
```

### 3. `get_ticket_details()` - Get Ticket Info

**Retrieve complete ticket information including routing history.**

```python
details = agent.get_ticket_details("FRM-H-20241108-ABC123")

print(details['ticket']['assigned_team'])
print(details['routing_history'])  # All routing events
```

### 4. `get_dashboard_stats()` - Get Statistics

**Get routing statistics and analytics.**

```python
stats = agent.get_dashboard_stats()

print(stats['total_tickets'])
print(stats['by_team'])      # Tickets per team
print(stats['by_urgency'])  # Tickets by urgency
print(stats['by_intent'])   # Tickets by intent
```

### 5. `export_tickets()` - Export to CSV

**Export routed tickets to CSV file.**

```python
filename = agent.export_tickets(status="open")
# Returns path to CSV file
```

## Automatic Routing Flow

When you call `RouterAgent().process_query()`, it automatically:

```
1. NLP Classification
   ├─ Analyzes message semantically
   ├─ Extracts intent, urgency, entities, sentiment
   └─ Determines category

2. Routing Decision
   ├─ Assigns team based on intent
   ├─ Applies smart routing rules
   └─ Sets escalation rules

3. Ticket Creation
   ├─ Creates ticket with assigned team
   ├─ Stores NLP insights
   └─ Generates ticket ID

4. Escalation Handling
   ├─ Escalates critical/high urgency
   └─ Logs escalation events

5. Learning
   └─ Learns from ticket for improvements
```

## Examples

### Example 1: Route Technical Support Ticket

```python
from router_agent import RouterAgent

agent = RouterAgent()

result = agent.process_query(
    channel="email",
    message="API integration keeps failing with error code 403",
    sender="dev@merchantpay.com",
    subject="API Error 403"
)

# Automatically routed to Tech Support
assert result['routing']['final_team'] == "Tech Support"
assert result['classification']['intent'] == "technical_support"
```

### Example 2: Route Billing Dispute

```python
result = agent.process_query(
    channel="form",
    message="Our invoice shows an extra $120 charge that we didn't authorize",
    sender="billing@acmecorp.com",
    subject="Billing Dispute"
)

# Automatically routed to Compliance Team (dispute detection)
assert result['routing']['final_team'] == "Compliance Team"
assert result['classification']['urgency'] == "high"
```

### Example 3: Batch Processing

```python
tickets = [
    {"channel": "email", "message": "API error", "sender": "dev@co.com"},
    {"channel": "form", "message": "Verification stuck", "sender": "user@co.com"},
    {"channel": "chat", "message": "Need demo", "sender": "sales@co.com"}
]

results = agent.batch_process(tickets)

for result in results:
    print(f"{result['ticket_id']} → {result['routing']['final_team']}")
```

### Example 4: Get Routing Statistics

```python
stats = agent.get_dashboard_stats()

print(f"Total Tickets: {stats['total_tickets']}")
print(f"By Team: {stats['by_team']}")
print(f"By Urgency: {stats['by_urgency']}")
```

## Integration Examples

### Flask API Integration

```python
from flask import Flask, request, jsonify
from router_agent import RouterAgent

app = Flask(__name__)
agent = RouterAgent()

@app.route('/api/route', methods=['POST'])
def route_ticket():
    data = request.get_json()
    
    # RouterAgent() handles everything automatically
    result = agent.process_query(
        channel=data.get('channel', 'form'),
        message=data['message'],
        sender=data.get('sender'),
        subject=data.get('subject')
    )
    
    return jsonify(result)
```

### Command Line Tool

```python
#!/usr/bin/env python3
from router_agent import RouterAgent
import sys

agent = RouterAgent()

if len(sys.argv) < 2:
    print("Usage: route_ticket.py <message>")
    sys.exit(1)

message = sys.argv[1]
result = agent.process_query(
    channel="form",
    message=message
)

print(f"Ticket {result['ticket_id']} routed to {result['routing']['final_team']}")
```

### Background Worker

```python
from router_agent import RouterAgent
import queue
import threading

agent = RouterAgent()
ticket_queue = queue.Queue()

def worker():
    while True:
        ticket = ticket_queue.get()
        # RouterAgent() automatically routes
        result = agent.process_query(**ticket)
        print(f"Routed: {result['ticket_id']}")
        ticket_queue.task_done()

# Start worker thread
threading.Thread(target=worker, daemon=True).start()

# Add tickets to queue
ticket_queue.put({
    "channel": "email",
    "message": "API error",
    "sender": "dev@co.com"
})
```

## RouterAgent() Features

### ✅ Automatic NLP Classification
- Understands message meaning semantically
- Extracts entities (error codes, amounts, dates)
- Detects sentiment
- Determines urgency based on context

### ✅ Smart Routing Rules
- Routes disputes to Compliance Team
- Routes low confidence to Triage Team
- Applies business logic automatically
- Handles edge cases intelligently

### ✅ Escalation Handling
- Automatically escalates critical/high urgency
- Sets response time expectations
- Notifies appropriate teams
- Logs escalation events

### ✅ Learning System
- Learns from routing decisions
- Improves accuracy over time
- Adapts to patterns
- Updates classification rules

## Best Practices

1. **Always use RouterAgent()** - Don't bypass the routing system
2. **Provide context** - Include subject line when available
3. **Use batch processing** - For multiple tickets, use `batch_process()`
4. **Check confidence** - Low confidence tickets may need review
5. **Monitor statistics** - Use `get_dashboard_stats()` for insights

## Troubleshooting

### Low Confidence Routing
```python
result = agent.process_query(...)
if result['classification']['confidence'] < 0.6:
    # Ticket routed to Triage Team for manual review
    print("Low confidence - needs review")
```

### Check Routing History
```python
details = agent.get_ticket_details(ticket_id)
for event in details['routing_history']:
    print(f"{event['event_type']}: {event['event_data']}")
```

## Summary

**RouterAgent() is your one-stop solution for automatic ticket routing:**

- ✅ Initialize once: `agent = RouterAgent()`
- ✅ Route tickets: `agent.process_query(...)`
- ✅ Everything else is automatic!

No manual routing needed - RouterAgent() handles everything using NLP! 🚀

