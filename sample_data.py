"""
Sample banking and fintech queries dataset for training and testing.
"""

SAMPLE_QUERIES = [
    # KYC / Compliance queries
    {
        "channel": "email",
        "sender": "john.doe@techcorp.com",
        "subject": "Vendor account verification stuck",
        "message": "Hello, we tried adding a new vendor bank account, but the verification is stuck on 'Pending' for 2 days.",
        "expected_team": "KYC Team",
        "expected_urgency": "high",
    },
    {
        "channel": "chat",
        "sender": "sarah.wilson@startupxyz.com",
        "subject": None,
        "message": "We need to update our company registration documents. The current ones expire next month. What's the process?",
        "expected_team": "KYC Team",
        "expected_urgency": "medium",
    },
    {
        "channel": "form",
        "sender": "compliance@globalfinance.com",
        "subject": "KYC documentation request",
        "message": "Our audit team needs all KYC documentation for transactions made in Q3 2024. Can you provide this?",
        "expected_team": "KYC Team",
        "expected_urgency": "high",
    },
    {
        "channel": "form",
        "sender": "tech@merchantpay.com",
        "subject": "API integration error 403",
        "message": "API integration keeps failing with error code 403 when we push payment data. We've checked our API keys and they seem correct.",
        "expected_team": "Tech Support",
        "expected_urgency": "high",
    },
    {
        "channel": "form",
        "sender": "billing@acmecorp.com",
        "subject": "Invoice discrepancy inquiry",
        "message": "Our monthly invoice for August shows an extra $120 charge. Can you please review and clarify this discrepancy?",
        "expected_team": "Finance Team",
        "expected_urgency": "medium",
    },
    {
        "channel": "form",
        "sender": "legal@corporate-client.com",
        "subject": "GDPR data export request",
        "message": "We need to export all data you have on our users for GDPR compliance. How do we initiate this request?",
        "expected_team": "Compliance Team",
        "expected_urgency": "high",
    },
    {
        "channel": "form",
        "sender": "inquiry@new-startup.com",
        "subject": "Enterprise plan pricing inquiry",
        "message": "We're interested in the enterprise plan for our 50-person team. Can we schedule a demo and get pricing information?",
        "expected_team": "Sales Team",
        "expected_urgency": "medium",
    },
    {
        "channel": "form",
        "sender": "support@tech-firm.com",
        "subject": "General documentation question",
        "message": "Where can I find the API documentation for retrieving transaction history? I've looked but couldn't locate it.",
        "expected_team": "General Support",
        "expected_urgency": "low",
    },
    {
        "channel": "email",
        "sender": "admin@retailbank.com",
        "subject": "Identity verification failing",
        "message": "Several of our customers are reporting that identity verification keeps failing even with correct documents. This is blocking new account creation.",
        "expected_team": "KYC Team",
        "expected_urgency": "critical",
    },
    # Tech Support queries
    {
        "channel": "form",
        "sender": "dev@merchantpay.com",
        "subject": "API integration error 403",
        "message": "API integration keeps failing with error code 403 when we push payment data. We've checked our API keys and they seem correct.",
        "expected_team": "Tech Support",
        "expected_urgency": "high",
    },
    {
        "channel": "email",
        "sender": "it@ecommerce-platform.com",
        "subject": "Webhook not receiving events",
        "message": "Our webhook endpoint stopped receiving payment confirmation events since yesterday. No recent changes on our end.",
        "expected_team": "Tech Support",
        "expected_urgency": "critical",
    },
    {
        "channel": "chat",
        "sender": "developer@fintech-startup.com",
        "subject": None,
        "message": "Is there an API endpoint to retrieve historical transaction data? I can't find it in the documentation.",
        "expected_team": "Tech Support",
        "expected_urgency": "low",
    },
    {
        "channel": "form",
        "sender": "tech@paymentpro.com",
        "subject": "Rate limiting issues",
        "message": "We're getting rate limit errors (429) during peak hours even though we're within our plan limits. Can you investigate?",
        "expected_team": "Tech Support",
        "expected_urgency": "high",
    },
    {
        "channel": "email",
        "sender": "sysadmin@enterprise-client.com",
        "subject": "Sandbox environment not working",
        "message": "The sandbox environment has been returning 500 errors for the past 3 hours. We need to test before deployment today.",
        "expected_team": "Tech Support",
        "expected_urgency": "critical",
    },
    # Finance queries
    {
        "channel": "chat",
        "sender": "billing@acmecorp.com",
        "subject": None,
        "message": "Our monthly invoice for August shows an extra $120 charge. Can you please review it?",
        "expected_team": "Finance Team",
        "expected_urgency": "medium",
    },
    {
        "channel": "email",
        "sender": "finance@retailchain.com",
        "subject": "Payment not processed",
        "message": "We sent a wire transfer of $45,000 three days ago but it's not showing in our account balance. Transaction ref: TXN-45329",
        "expected_team": "Finance Team",
        "expected_urgency": "critical",
    },
    {
        "channel": "form",
        "sender": "accounts@supplier-network.com",
        "subject": "Request invoice copy",
        "message": "Could you please send us a copy of invoice #INV-2024-08-1523? We need it for our accounting records.",
        "expected_team": "Finance Team",
        "expected_urgency": "low",
    },
    {
        "channel": "email",
        "sender": "cfo@midsize-business.com",
        "subject": "Refund request",
        "message": "We were charged twice for September subscription. Please refund the duplicate charge of $299.",
        "expected_team": "Finance Team",
        "expected_urgency": "high",
    },
    {
        "channel": "chat",
        "sender": "accounting@tech-firm.com",
        "subject": None,
        "message": "What payment methods do you accept for enterprise plans? We prefer ACH transfers.",
        "expected_team": "Finance Team",
        "expected_urgency": "low",
    },
    # Compliance queries
    {
        "channel": "email",
        "sender": "legal@corporate-client.com",
        "subject": "GDPR data request",
        "message": "We need to export all data you have on our users for GDPR compliance. How do we initiate this request?",
        "expected_team": "Compliance Team",
        "expected_urgency": "high",
    },
    {
        "channel": "form",
        "sender": "compliance@financial-services.com",
        "subject": "Regulatory compliance question",
        "message": "Are your services compliant with PCI DSS Level 1? We need documentation for our compliance audit.",
        "expected_team": "Compliance Team",
        "expected_urgency": "high",
    },
    {
        "channel": "email",
        "sender": "audit@banking-corp.com",
        "subject": "SOC 2 certification",
        "message": "Can you provide your latest SOC 2 Type II report? Our security team needs to review it.",
        "expected_team": "Compliance Team",
        "expected_urgency": "medium",
    },
    # Sales queries
    {
        "channel": "form",
        "sender": "inquiry@new-startup.com",
        "subject": "Enterprise plan pricing",
        "message": "We're interested in the enterprise plan for our 50-person team. Can we schedule a demo?",
        "expected_team": "Sales Team",
        "expected_urgency": "medium",
    },
    {
        "channel": "email",
        "sender": "partnerships@fintech-company.com",
        "subject": "Partnership opportunity",
        "message": "We'd like to explore a partnership opportunity. Do you have white-label solutions?",
        "expected_team": "Sales Team",
        "expected_urgency": "low",
    },
    # Mixed/Complex queries
    {
        "channel": "email",
        "sender": "director@multi-branch-bank.com",
        "subject": "Multiple issues",
        "message": "We're experiencing API timeouts (error 504) and also need clarification on last month's invoice which seems higher than usual. Additionally, can someone help expedite KYC verification for our new branch?",
        "expected_team": "Tech Support",  # Most urgent issue
        "expected_urgency": "critical",
    },
]

# Canned responses for RAG system
CANNED_RESPONSES = [
    {
        "category": "kyc_pending",
        "keywords": [
            "verification stuck",
            "pending",
            "account verification",
            "kyc pending",
            "vendor account",
            "bank account verification",
        ],
        "response": "Dear [Customer], thank you for reaching out. Your vendor's account verification is under review. Our KYC team will complete it within 24 hours. If you haven't already, please ensure all required documents are uploaded: (1) Company registration certificate, (2) Tax ID/PAN, (3) Bank statement, and (4) Authorized signatory ID. We'll notify you once verification is complete. Best regards, FinLink Support Team",
    },
    {
        "category": "api_error_403",
        "keywords": [
            "403",
            "forbidden",
            "api error",
            "authentication failed",
            "api integration",
            "payment data",
        ],
        "response": "Hi [Developer], a 403 error typically occurs when an authentication token has expired or lacks proper permissions. Please verify: (1) Your API key is active and hasn't expired, (2) Regenerate your API key from the dashboard under Settings > API Keys, (3) Ensure you're using the correct base URL (sandbox vs production). If the issue persists after regenerating your key, please share the request ID with our Tech Support team, and we'll investigate further. Best regards, FinLink Support Team",
    },
    {
        "category": "billing_dispute",
        "keywords": [
            "invoice",
            "charge",
            "billing",
            "extra charge",
            "overcharge",
            "monthly invoice",
            "discrepancy",
        ],
        "response": "Hi [Customer], thanks for bringing this to our attention. We're reviewing your invoice to check the discrepancy you mentioned. Our Compliance team will verify the charges against your transaction records and confirm within 1 business day. If there's a billing error, we'll issue a correction immediately. Please provide the invoice number if you haven't already. Best regards, FinLink Support Team",
    },
    {
        "category": "payment_missing",
        "keywords": [
            "payment not received",
            "transfer not showing",
            "missing payment",
            "balance not updated",
        ],
        "response": "We apologize for any concern. Payment processing can take 2-5 business days depending on the method. Please provide: (1) Transaction reference number, (2) Payment amount, (3) Date of payment, (4) Payment method used. Our Finance team will trace the transaction and update you within 24 hours.",
    },
    {
        "category": "api_rate_limit",
        "keywords": ["rate limit", "429", "too many requests", "throttling"],
        "response": "Rate limits are in place to ensure system stability. Your current plan allows X requests per minute. If you're hitting limits during normal usage: (1) Consider implementing exponential backoff, (2) Cache responses when possible, (3) Review if you need to upgrade your plan. Our Tech Support team can analyze your usage patterns and recommend the appropriate plan.",
    },
    {
        "category": "webhook_issue",
        "keywords": [
            "webhook",
            "callback",
            "notification not received",
            "event not triggering",
        ],
        "response": "Webhook delivery issues can occur due to several reasons: (1) Verify your endpoint is publicly accessible, (2) Check if your endpoint returns a 200 status code, (3) Ensure SSL certificate is valid. You can view webhook delivery logs in your dashboard under Developers > Webhooks. Our Tech Support team will check our delivery logs and help debug the issue.",
    },
    {
        "category": "documentation_request",
        "keywords": ["documentation", "how to", "guide", "tutorial", "api docs"],
        "response": "Our comprehensive documentation is available at docs.finlink.com. You can find: (1) API reference, (2) Integration guides, (3) Code samples, (4) Best practices. If you need specific guidance, please let us know what you're trying to accomplish and our Tech Support team can provide targeted assistance.",
    },
    {
        "category": "compliance_request",
        "keywords": [
            "compliance",
            "gdpr",
            "pci dss",
            "soc 2",
            "audit",
            "certification",
        ],
        "response": "We take compliance very seriously. Our platform is certified for: PCI DSS Level 1, SOC 2 Type II, GDPR compliant. Documentation is available in the Trust Center section of our website. For specific compliance questions or to request reports, our Compliance team will assist you directly.",
    },
    {
        "category": "refund_request",
        "keywords": ["refund", "duplicate charge", "charged twice", "incorrect charge"],
        "response": "We apologize for the billing error. To process your refund: (1) Confirm the transaction ID or invoice number, (2) Specify the amount to be refunded, (3) Preferred refund method. Refunds are typically processed within 5-7 business days. Our Finance team will initiate this immediately and send you confirmation.",
    },
    {
        "category": "sales_inquiry",
        "keywords": [
            "demo",
            "pricing",
            "enterprise plan",
            "partnership",
            "white label",
        ],
        "response": "Thank you for your interest in FinLink! We'd be happy to discuss how our platform can meet your needs. Our Sales team will reach out within 24 hours to schedule a demo and discuss pricing options tailored to your requirements. In the meantime, you can view our plans at finlink.com/pricing.",
    },
    {
        "category": "identity_verification",
        "keywords": [
            "identity verification",
            "id verification",
            "document verification",
            "verification failing",
        ],
        "response": "Identity verification requires clear, legible documents. Common reasons for failure: (1) Blurry or cropped images, (2) Expired documents, (3) Name mismatch between documents, (4) Unsupported document types. Please ensure: Valid government-issued ID, Clear photo/scan, All corners visible. If issues persist, our KYC team can review manually.",
    },
    {
        "category": "system_outage",
        "keywords": [
            "down",
            "not working",
            "500 error",
            "504 error",
            "timeout",
            "outage",
        ],
        "response": "We apologize for the service disruption. Our team has been notified and is investigating. You can check real-time status at status.finlink.com. For critical issues affecting operations, our Tech Support team will prioritize your case and provide updates every hour until resolved.",
    },
]


def get_sample_queries():
    """Return all sample queries."""
    return SAMPLE_QUERIES


def get_canned_responses():
    """Return all canned responses."""
    return CANNED_RESPONSES


def get_queries_by_channel(channel: str):
    """Get sample queries filtered by channel."""
    return [q for q in SAMPLE_QUERIES if q["channel"] == channel]


def get_queries_by_team(team: str):
    """Get sample queries filtered by expected team."""
    return [q for q in SAMPLE_QUERIES if q["expected_team"] == team]
