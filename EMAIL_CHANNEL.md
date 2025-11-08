# Email Channel with NLP Classification

## Overview

The Email Channel endpoint (`/api/submit_email`) is a dedicated endpoint for processing email inputs that automatically uses Natural Language Processing (NLP) to classify emails into categories based on the email subject and message body.

## Features

- **Automatic NLP Classification**: Uses Google Gemini AI to analyze email content semantically
- **Category Detection**: Automatically determines intent category (kyc_verification, technical_support, billing_finance, compliance_regulatory, sales_inquiry, general_support)
- **Urgency Assessment**: Classifies urgency level (critical, high, medium, low) based on business impact
- **Entity Extraction**: Identifies key entities like error codes, amounts, dates, account types
- **Sentiment Analysis**: Detects sentiment (urgent, negative, positive, neutral)
- **Automatic Routing**: Routes emails to appropriate teams based on classification
- **Auto-Response Generation**: Generates personalized responses using RAG system

## API Endpoint

### POST `/api/submit_email`

Submit an email for processing and routing with NLP classification.

#### Request Body

```json
{
  "from": "sender@example.com",
  "subject": "Email subject line",
  "body": "Email message body",
  "timestamp": "2025-11-08T12:00:00",  // optional
  "attachments": ["file1.pdf"],  // optional
  "auto_respond": true  // optional, default: true
}
```

#### Required Fields

- Either `body` or `subject` must be provided (at least one)

#### Optional Fields

- `from` or `sender`: Email sender address
- `timestamp`: Email timestamp (ISO format)
- `attachments`: Array of attachment filenames
- `auto_respond`: Whether to generate automatic response (default: true)

#### Response

```json
{
  "success": true,
  "message": "Email processed and routed using NLP classification",
  "result": {
    "ticket_id": "EML-H-20251108-ABC123",
    "classification": {
      "intent": "technical_support",
      "category": "technical_support",
      "urgency": "high",
      "confidence": 0.85,
      "reasoning": "Message mentions API error 403 and blocking operations...",
      "key_entities": ["error_403", "API", "payment"],
      "sentiment": "urgent"
    },
    "routing": {
      "assigned_team": "Tech Support",
      "escalate": true
    },
    "response": {
      "text": "Thank you for contacting us...",
      "generated_at": "2025-11-08T12:00:00"
    },
    "metadata": {
      "channel_type": "email",
      "email_from": "sender@example.com",
      "email_subject": "Email subject line",
      "email_body": "Email message body",
      "attachments": []
    }
  }
}
```

## Example Usage

### Python Example

```python
import requests

url = "http://localhost:8000/api/submit_email"

email_data = {
    "from": "customer@company.com",
    "subject": "API Error 403 - Payment Integration Failing",
    "body": "Our payment integration is failing with error code 403. This is blocking all our transactions.",
    "auto_respond": True
}

response = requests.post(url, json=email_data)
result = response.json()

if result['success']:
    classification = result['result']['classification']
    print(f"Category: {classification['category']}")
    print(f"Urgency: {classification['urgency']}")
    print(f"Assigned Team: {result['result']['routing']['assigned_team']}")
```

### cURL Example

```bash
curl -X POST http://localhost:8000/api/submit_email \
  -H "Content-Type: application/json" \
  -d '{
    "from": "customer@company.com",
    "subject": "API Error 403",
    "body": "Our payment integration is failing with error code 403."
  }'
```

## NLP Classification Categories

The system classifies emails into the following categories:

1. **kyc_verification**: Account verification, identity checks, KYC processes
2. **technical_support**: API errors, integration problems, technical bugs
3. **billing_finance**: Invoice questions, payment processing, charges
4. **compliance_regulatory**: GDPR, PCI DSS, SOC 2, regulatory compliance, billing disputes
5. **sales_inquiry**: Demo requests, pricing inquiries, enterprise plans
6. **general_support**: General help, documentation requests, how-to questions

## Urgency Levels

- **critical**: System down, security breaches, complete service outages
- **high**: API errors affecting operations, verification delays, billing issues
- **medium**: Feature requests, general inquiries, documentation requests
- **low**: Information requests, feedback, non-urgent questions

## Testing

Run the test script to see NLP classification in action:

```bash
python test_email_channel.py
```

This will test various email types and show how the NLP system classifies them.

## Integration with Existing System

The email channel integrates seamlessly with the existing routing system:

- Uses the same `RouterAgent` for processing
- Leverages the same `IntentClassifier` for NLP classification
- Creates tickets in the same database
- Supports the same auto-response generation
- Works with the same dashboard and analytics

## Error Handling

If classification fails (e.g., API unavailable), the system falls back to:
- Enhanced keyword matching
- Pattern recognition
- Rule-based classification
- Default routing to Triage Team

## Notes

- The NLP classifier analyzes both subject and body together for better context
- Disputes are automatically routed to Compliance Team (not Finance)
- Low confidence classifications (<60%) are routed to Triage Team for manual review
- The system learns from previous classifications to improve accuracy over time

