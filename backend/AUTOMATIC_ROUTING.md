# Automatic Ticket Routing - How It Works

## ✅ YES - Tickets Are Automatically Routed!

When a customer submits a query, the system **automatically** routes it to the appropriate team **without any manual intervention**.

## Automatic Routing Flow (Using RouterAgent())

**RouterAgent() handles all automatic routing!**

```
┌─────────────────────────────────────────────────────────────┐
│  Customer Submits Query via Web Form / API                  │
│  POST /api/submit_query                                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  RouterAgent().process_query() - ONE METHOD CALL!          │
│                                                              │
│  This single method automatically handles everything:        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 1: NLP Classification (AUTOMATIC)                    │
│  • Analyzes message semantically                            │
│  • Extracts intent, urgency, entities, sentiment            │
│  • Determines category (kyc, technical, billing, etc.)       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 2: Routing Decision (AUTOMATIC)                      │
│  • Assigns team based on intent                             │
│  • Applies smart routing rules                               │
│  • Uses NLP insights (entities, sentiment)                   │
│  • Sets escalation rules                                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 3: Ticket Creation (AUTOMATIC)                       │
│  • Creates ticket with assigned team                         │
│  • Stores all NLP insights                                   │
│  • Generates unique ticket ID                                │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 4: Escalation Handling (AUTOMATIC)                    │
│  • Escalates critical/high urgency tickets                   │
│  • Logs escalation events                                    │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 5: Learning (AUTOMATIC)                               │
│  • Learns from ticket for future improvements                │
│  • Updates classification patterns                           │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  Returns Complete Routing Result                            │
│  • ticket_id, team, intent, urgency, response              │
└─────────────────────────────────────────────────────────────┘
```

### Code Example

```python
from router_agent import RouterAgent

# Initialize RouterAgent() - handles everything!
agent = RouterAgent()

# Route ticket automatically - ONE METHOD CALL!
result = agent.process_query(
    channel="form",
    message="API error 403 blocking payments",
    sender="dev@company.com",
    subject="Urgent: API Issue"
)

# That's it! Ticket is automatically routed
print(f"Ticket {result['ticket_id']} → {result['routing']['final_team']}")
```

## Example: Automatic Routing in Action

### Input:
```json
{
  "message": "API integration keeps failing with error code 403",
  "sender": "dev@company.com",
  "subject": "API Error"
}
```

### Automatic Processing:
1. **NLP Analysis** (automatic):
   - Intent: `technical_support`
   - Urgency: `high`
   - Entities: `["error_403", "API", "integration"]`
   - Sentiment: `negative`

2. **Routing Decision** (automatic):
   - Team: `Tech Support`
   - Escalation: `Yes` (high urgency)
   - Response Time: `4 hours`

3. **Ticket Created** (automatic):
   - Ticket ID: `FRM-H-20241108-ABC123`
   - Status: `open`
   - Assigned Team: `Tech Support`
   - All metadata stored automatically

### Result:
✅ **Ticket automatically routed to Tech Support team**
✅ **No manual intervention required**
✅ **Routing happens instantly**

## Routing Rules (Applied Automatically)

| Message Type | Intent | Auto-Routed To |
|-------------|--------|----------------|
| API errors, technical issues | `technical_support` | Tech Support |
| Verification stuck, KYC issues | `kyc_verification` | KYC Team |
| Billing disputes, wrong charges | `billing_finance` → detects dispute | Compliance Team |
| Standard billing questions | `billing_finance` | Finance Team |
| Compliance certificates, audits | `compliance_regulatory` | Compliance Team |
| Demo requests, pricing | `sales_inquiry` | Sales Team |
| General questions | `general_support` | Tech Support |
| Low confidence (<60%) | Any | Triage Team |

## How to Verify Automatic Routing

### Method 1: Via Web UI
1. Go to `http://localhost:8000`
2. Submit a query through the form
3. Check the tickets panel - you'll see it automatically routed

### Method 2: Via API
```bash
curl -X POST http://localhost:8000/api/submit_query \
  -H "Content-Type: application/json" \
  -d '{
    "message": "API error 403",
    "sender": "test@example.com"
  }'
```

Response will show:
```json
{
  "success": true,
  "result": {
    "ticket_id": "FRM-H-...",
    "routing": {
      "final_team": "Tech Support",  // ← Automatically assigned!
      "escalate": true
    },
    "classification": {
      "intent": "technical_support",
      "urgency": "high"
    }
  }
}
```

### Method 3: Check Database
```bash
python -c "from database import Database; db = Database(); tickets = db.get_all_tickets(); print([t['assigned_team'] for t in tickets])"
```

## Key Features

✅ **Fully Automatic** - No manual routing needed
✅ **RouterAgent() Powered** - One method call handles everything
✅ **NLP-Powered** - Understands message meaning semantically
✅ **Smart Rules** - Applies business logic automatically
✅ **Instant** - Routing happens in milliseconds
✅ **Learning** - Improves over time automatically
✅ **Escalation** - Handles urgent tickets automatically
✅ **Batch Processing** - Route multiple tickets at once

## What Happens Automatically (via RouterAgent())

When you call `RouterAgent().process_query()`:

1. ✅ Message is analyzed using NLP
2. ✅ Intent and urgency are classified
3. ✅ Team is assigned automatically
4. ✅ Ticket is created with routing info
5. ✅ Escalation is handled if needed
6. ✅ System learns from the routing

**All handled by RouterAgent() - No manual steps required!** 🎉

## Using RouterAgent() in Your Code

### In Flask App (app.py)
```python
from router_agent import RouterAgent

router = RouterAgent()  # Initialize once

@app.route('/api/submit_query', methods=['POST'])
def submit_query():
    data = request.get_json()
    
    # RouterAgent() automatically routes!
    result = router.process_query(
        channel='form',
        message=data['message'],
        sender=data.get('sender'),
        subject=data.get('subject')
    )
    
    return jsonify(result)
```

### Standalone Script
```python
from router_agent import RouterAgent

agent = RouterAgent()

# Route tickets automatically
result = agent.process_query(
    channel="email",
    message="API error 403",
    sender="dev@company.com"
)

print(f"Routed to: {result['routing']['final_team']}")
```

### Batch Processing
```python
from router_agent import RouterAgent

agent = RouterAgent()

tickets = [
    {"channel": "email", "message": "API error", "sender": "dev@co.com"},
    {"channel": "form", "message": "Billing issue", "sender": "billing@co.com"}
]

# RouterAgent() routes all automatically
results = agent.batch_process(tickets)
```

**See `ROUTER_AGENT_GUIDE.md` for complete RouterAgent() documentation!**

