# RAG System with HTML Pages Knowledge Base

## Overview

The RAG (Retrieval Augmented Generation) system has been enhanced to use HTML documentation pages from the `pages` folder as its knowledge base. This provides richer context and more comprehensive information for generating accurate, contextual responses.

## How It Works

### 1. **Knowledge Base Loading**

When the RAG system initializes, it:

1. **Scans the `pages` folder** for HTML files (excluding `index.html`)
2. **Parses each HTML page** using BeautifulSoup4 to extract:
   - Category name and code
   - Overview description
   - Keywords
   - Use cases
   - Common scenarios
   - Response template
   - Response approach steps
3. **Builds a vector store** with all extracted content
4. **Indexes for semantic search** using token-based cosine similarity

### 2. **Query Processing Flow**

```
Customer Query
    ↓
NLP Classification (Intent, Urgency, Entities, Sentiment)
    ↓
RAG System.retrieve_response()
    ↓
Semantic Search across HTML pages
    ↓
Retrieve Top 3 Most Relevant Pages
    ↓
Extract Rich Context (Overview, Use Cases, Scenarios, Templates)
    ↓
Build Enhanced Prompt with Context
    ↓
Gemini AI Generates Response
    ↓
Personalized Response Returned
```

### 3. **Context Building**

The system builds rich context from retrieved HTML pages:

```
1. [KYC Pending (kyc_pending)]
   Overview: Handles verification delays and pending account issues
   Use Cases: Vendor account verification stuck; Bank account verification delays
   Common Scenarios: New Account Setup; Document Review; Time-Sensitive
   Template Response: Dear [Customer], thank you for reaching out...
```

### 4. **Enhanced Prompt**

The prompt sent to Gemini AI includes:

- **Customer Query**: The exact message/description
- **Query Analysis**: Intent, urgency, sentiment, entities
- **Knowledge Base Context**: Rich content from relevant HTML pages
- **Guidelines**: Instructions for generating accurate responses

## Key Features

### ✅ **Rich Context from HTML Pages**

The system extracts comprehensive information from each HTML page:
- Overview descriptions
- Use cases and scenarios
- Response templates
- Response approach steps
- Keywords and categories

### ✅ **Semantic Search**

Uses token-based cosine similarity to find the most relevant pages based on:
- Customer query content
- Intent classification
- Keywords matching

### ✅ **Fallback Mechanism**

If HTML pages are not available:
- Falls back to original canned responses from `sample_data.py`
- Ensures system continues to work even if pages folder is missing

### ✅ **BeautifulSoup HTML Parsing**

- Uses BeautifulSoup4 for robust HTML parsing
- Handles malformed HTML gracefully
- More maintainable and readable code
- Industry-standard HTML parsing library
- Better error handling and edge case support

## Installation

Install BeautifulSoup4:

```bash
pip install beautifulsoup4
```

The dependency is already added to `requirements.txt`.

## File Structure

```
pages/
├── index.html                    # Documentation index (excluded from RAG)
├── kyc_pending.html             # KYC Pending template
├── api_error_403.html           # API Error 403 template
├── billing_dispute.html         # Billing Dispute template
├── payment_missing.html          # Payment Missing template
├── api_rate_limit.html          # API Rate Limit template
├── webhook_issue.html           # Webhook Issue template
├── documentation_request.html   # Documentation Request template
├── compliance_request.html      # Compliance Request template
├── refund_request.html         # Refund Request template
├── sales_inquiry.html           # Sales Inquiry template
├── identity_verification.html   # Identity Verification template
└── system_outage.html           # System Outage template
```

## How Responses Are Generated

### Step 1: Query Analysis
- Customer submits query via email channel
- NLP classifies intent, urgency, sentiment, entities

### Step 2: Semantic Retrieval
- RAG system searches all HTML pages
- Finds top 3 most relevant pages based on semantic similarity
- Extracts rich context from each page

### Step 3: Context Building
- Combines overview, use cases, scenarios, and templates
- Builds comprehensive context for Gemini AI

### Step 4: Response Generation
- Gemini AI receives:
  - Customer query
  - Query analysis (intent, urgency, sentiment)
  - Rich context from HTML pages
  - Response guidelines
- Generates personalized, contextual response

### Step 5: Response Return
- Response is returned to customer
- Stored with ticket in database

## Example

**Customer Query:**
```
"API integration keeps failing with error code 403 when we push payment data."
```

**Retrieved HTML Pages:**
1. `api_error_403.html` (highest similarity)
2. `webhook_issue.html` (medium similarity)
3. `system_outage.html` (lower similarity)

**Context Sent to Gemini:**
```
1. [API Error 403 (api_error_403)]
   Overview: This response template provides troubleshooting guidance for HTTP 403 Forbidden errors...
   Use Cases: API requests returning 403 Forbidden status; Authentication token expiration issues
   Common Scenarios: Expired Tokens; Insufficient Permissions; Wrong Environment
   Template Response: Hi [Developer], a 403 error typically occurs when...
```

**Generated Response:**
```
Hi [Developer],

Thank you for reporting the API error 403 issue with your payment integration. 
A 403 error typically occurs when an authentication token has expired or lacks 
proper permissions. 

Please verify: (1) Your API key is active and hasn't expired, (2) Regenerate 
your API key from the dashboard under Settings > API Keys, (3) Ensure you're 
using the correct base URL (sandbox vs production).

Our Tech Support team has been assigned to investigate this immediately. 
If the issue persists after regenerating your key, please share the request ID, 
and we'll investigate further.

Best regards,
FinLink Support Team
```

## Benefits

✅ **Richer Context**: HTML pages provide comprehensive information  
✅ **Better Accuracy**: More detailed context leads to more accurate responses  
✅ **Maintainable**: Update HTML pages to improve responses  
✅ **Scalable**: Easy to add new template pages  
✅ **Documented**: Each template has full documentation  

## Maintenance

To update or add response templates:

1. **Edit HTML pages** in the `pages` folder
2. **Add new pages** following the same structure
3. **Restart the application** to reload the knowledge base

The system automatically rebuilds the vector store on initialization.

## Technical Details

- **Parser**: BeautifulSoup4 for HTML parsing
- **Search**: Token-based cosine similarity
- **AI Model**: Google Gemini 1.5 Flash
- **Context Size**: Top 3 most relevant pages
- **Fallback**: Original canned responses if HTML unavailable

## Summary

The RAG system now uses all HTML pages in the `pages` folder as its knowledge base, providing Gemini AI with rich, contextual information to generate accurate, helpful responses that directly address customer queries based on the comprehensive documentation.

