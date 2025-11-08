"""
Configuration settings for the Customer Query Router system.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT", "customer-query-router")

# LangSmith Configuration
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")

# Database Configuration
DATABASE_PATH = "query_router.db"

# Flask Configuration
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5000
FLASK_DEBUG = True

# Team Configuration
TEAMS = {
    "kyc": {
        "name": "KYC Team",
        "email": "kyc@finlink.com",
        "description": "Handles account verification, identity checks, and compliance documentation"
    },
    "tech_support": {
        "name": "Tech Support",
        "email": "tech-support@finlink.com",
        "description": "Handles API issues, technical errors, and integration problems"
    },
    "finance": {
        "name": "Finance Team",
        "email": "finance@finlink.com",
        "description": "Handles billing, invoices, payment processing, and refunds"
    },
    "compliance": {
        "name": "Compliance Team",
        "email": "compliance@finlink.com",
        "description": "Handles regulatory queries, audit requests, and policy questions"
    },
    "sales": {
        "name": "Sales Team",
        "email": "sales@finlink.com",
        "description": "Handles new customer inquiries and business development"
    }
}

# Urgency Levels
URGENCY_LEVELS = {
    "critical": {
        "response_time": "immediate",
        "sla_hours": 1,
        "auto_escalate": True
    },
    "high": {
        "response_time": "4 hours",
        "sla_hours": 4,
        "auto_escalate": False
    },
    "medium": {
        "response_time": "24 hours",
        "sla_hours": 24,
        "auto_escalate": False
    },
    "low": {
        "response_time": "48 hours",
        "sla_hours": 48,
        "auto_escalate": False
    }
}

# Classification Thresholds
CONFIDENCE_THRESHOLD = 0.6  # Below this, route to triage team
HIGH_CONFIDENCE_THRESHOLD = 0.85  # Above this, auto-respond without review

# Response Generation
MAX_RESPONSE_LENGTH = 1000
ENABLE_AUTO_RESPONSE = True

# Ticket Export
EXPORT_DIRECTORY = "."
CSV_ENCODING = "utf-8"
