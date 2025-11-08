# Enhanced NLP Routing System

## Overview
The routing system has been enhanced with advanced Natural Language Processing (NLP) capabilities to better understand customer messages and route them to the appropriate categories and teams.

## Key Enhancements

### 1. **Semantic Understanding**
The system now uses advanced NLP prompts that:
- Understand the **core meaning** of messages, not just keywords
- Identify **implicit meanings** (e.g., "stuck" = blocking issue)
- Consider **context** (is this blocking operations? is it a question vs. problem?)
- Analyze **business impact** to determine urgency

### 2. **Entity Extraction**
The system automatically extracts key entities from messages:
- **Error codes**: "403", "500", "404"
- **Amounts**: "$120", "100 dollars"
- **Dates**: "August", "2 days ago"
- **Account types**: "vendor account", "bank account"
- **Technical terms**: "API", "webhook", "SDK"

These entities help with:
- Better routing decisions
- Faster ticket resolution
- Context-aware responses

### 3. **Sentiment Analysis**
The system detects sentiment from messages:
- **Urgent**: Messages with urgent language
- **Negative**: Problem reports, complaints
- **Positive**: Thank you messages, appreciation
- **Neutral**: Standard inquiries

Sentiment is used to:
- Adjust urgency levels
- Route disputes to compliance
- Prioritize tickets

### 4. **Enhanced Classification Prompt**
The Gemini AI prompt now includes:
- Detailed category descriptions with examples
- Context-aware urgency detection rules
- Classification rules for edge cases
- Instructions for semantic understanding

### 5. **Improved Fallback Classification**
When the AI API is unavailable, the fallback system:
- Uses **pattern matching** with regex
- Extracts entities using pattern recognition
- Detects sentiment from keyword analysis
- Uses **weighted scoring** for intent classification
- Provides detailed reasoning

### 6. **Smart Routing Decisions**
Routing decisions now consider:
- **NLP insights**: Entities and sentiment
- **Context**: Business impact and blocking nature
- **Sentiment-based urgency**: Adjusts urgency based on sentiment
- **Entity-based routing**: Routes disputes based on detected entities

## How It Works

### Classification Process

1. **Message Analysis**
   - Combines subject and message for full context
   - Extracts key entities
   - Detects sentiment
   - Understands semantic meaning

2. **Intent Classification**
   - Uses Gemini AI for semantic understanding
   - Falls back to enhanced keyword matching if needed
   - Considers learned patterns from previous tickets

3. **Urgency Detection**
   - Analyzes business impact
   - Considers blocking nature
   - Adjusts based on sentiment
   - Uses entity patterns (error codes, security terms)

4. **Routing Decision**
   - Assigns team based on intent
   - Considers NLP insights (entities, sentiment)
   - Applies special routing rules (disputes → compliance)
   - Escalates based on urgency and confidence

### Example: Billing Dispute Detection

**Message**: "Our August invoice shows a charge of $500 that we didn't authorize. This is incorrect and we need this resolved immediately."

**NLP Analysis**:
- **Entities**: ["$500", "August", "invoice"]
- **Sentiment**: "negative" (complaint language)
- **Intent**: "billing_finance" → but detects "dispute" → routes to "compliance_regulatory"
- **Urgency**: "high" (immediate resolution needed)

**Routing**: Compliance Team (not Finance Team) because it's a dispute requiring investigation.

## Benefits

1. **More Accurate Routing**: Semantic understanding reduces misrouting
2. **Better Urgency Detection**: Context-aware urgency improves prioritization
3. **Faster Resolution**: Entity extraction helps teams understand issues quickly
4. **Improved Customer Experience**: Better understanding leads to more relevant responses
5. **Learning Capability**: System learns from corrections and improves over time

## Testing

Run the test script to see the NLP capabilities in action:

```bash
python test_nlp_routing.py
```

This will test various scenarios and demonstrate:
- Semantic understanding
- Entity extraction
- Sentiment analysis
- Context-aware routing

## Configuration

The NLP system uses the Google Gemini API. Ensure your `.env` file contains:

```
GOOGLE_API_KEY=your_api_key_here
```

## Categories and Teams

The system routes to these categories:

1. **kyc_verification** → KYC Team
2. **technical_support** → Tech Support
3. **billing_finance** → Finance Team (or Compliance Team for disputes)
4. **compliance_regulatory** → Compliance Team
5. **sales_inquiry** → Sales Team
6. **general_support** → Tech Support

## Future Enhancements

Potential improvements:
- Multi-language support
- Named Entity Recognition (NER) for better entity extraction
- Intent confidence thresholds for auto-escalation
- Custom category training from historical data
- Integration with external NLP services for specialized domains

