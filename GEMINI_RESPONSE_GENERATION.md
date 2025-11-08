# Gemini LLM Response Generation

## Overview

The system uses **Google Gemini AI** to generate intelligent, contextual responses to customer queries. The response generation is powered by a **RAG (Retrieval Augmented Generation)** system that combines semantic search with Gemini's language generation capabilities.

## How It Works

### 1. **Response Generation Flow**

```
Customer Query
    ↓
RouterAgent.process_query()
    ↓
NLP Classification (Intent, Urgency, Entities, Sentiment)
    ↓
RAG System.generate_response()
    ↓
1. Retrieve relevant templates (semantic search)
2. Build enhanced prompt with context
3. Generate response with Gemini AI
    ↓
Personalized Response Returned
```

### 2. **RAG System Components**

The `RAGSystem` class (`rag_system.py`) handles response generation:

- **Vector Store**: Pre-built semantic search index of response templates
- **Semantic Retrieval**: Finds most relevant templates using cosine similarity
- **Gemini AI**: Generates personalized responses using Google's Gemini model
- **Context Building**: Combines query analysis, templates, and metadata

### 3. **Enhanced Prompt Structure**

The system uses an enhanced prompt that includes:

- **Customer Query**: The exact query from the customer
- **Query Analysis**: Intent, urgency, sentiment, key entities
- **Reference Templates**: Relevant response templates from knowledge base
- **Guidelines**: Specific instructions for generating helpful responses

### 4. **Response Features**

Gemini generates responses that:

✅ **Address Specific Queries**: Directly answers what the customer asked  
✅ **Reference Key Entities**: Mentions error codes, amounts, dates naturally  
✅ **Match Urgency Level**: Adjusts tone based on critical/high/medium/low  
✅ **Show Empathy**: Acknowledges frustration for negative sentiment  
✅ **Provide Actionable Steps**: Clear next steps or information  
✅ **Set Expectations**: Realistic response times based on urgency  
✅ **Personalize**: Uses customer name and specific situation  

## Example Response Generation

### Input Query:
```
"API integration keeps failing with error code 403 when we push payment data. 
This is blocking all our transactions."
```

### Classification:
- Intent: `technical_support`
- Urgency: `high`
- Key Entities: `["error_403", "API", "payment"]`
- Sentiment: `urgent`
- Assigned Team: `Tech Support`

### Generated Response (by Gemini):
```
Dear [Customer],

Thank you for reporting the API error 403 issue with your payment integration. 
We understand this is blocking your transactions and affecting your business operations.

Our Tech Support team has been assigned to investigate this issue immediately. 
Error 403 typically indicates an authentication or authorization problem. 
Please ensure your API credentials are valid and have the necessary permissions 
for payment processing.

We'll prioritize this high-urgency issue and aim to resolve it within 4 hours. 
You'll receive updates as we investigate. If you have any additional details 
about when this started occurring, that would be helpful.

Best regards,
FinLink Support Team
```

## Response Generation Code

### In RouterAgent:

```python
# Step 3: Generate response if requested
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
```

### RAG System Method:

```python
def generate_response(
    self,
    query: str,
    intent: str = None,
    urgency: str = "medium",
    customer_name: str = None,
    reasoning: str = None,
    key_entities: List[str] = None,
    sentiment: str = None,
    assigned_team: str = None,
    response_time: str = None
) -> Dict:
    # 1. Retrieve relevant templates
    retrieved = self.retrieve_response(query, intent, n_results=3)
    
    # 2. Build context from templates
    context = build_context_from_templates(retrieved)
    
    # 3. Create enhanced prompt
    prompt = self._create_response_prompt(
        query, context, intent, urgency, 
        customer_name, reasoning, key_entities, 
        sentiment, assigned_team, response_time
    )
    
    # 4. Generate with Gemini AI
    response = self.model.generate_content(prompt)
    
    return {
        "response": response.text.strip(),
        "method": "rag_generated",
        "canned_templates_used": len(retrieved)
    }
```

## Prompt Enhancement

The enhanced prompt includes:

1. **Clear Role Definition**: Expert customer support representative
2. **Structured Sections**: Opening, Acknowledgment, Address Query, Set Expectations, Closing
3. **Specific Guidelines**: Be specific, conversational, actionable, empathetic
4. **Response Style**: Natural, genuine, tailored to situation
5. **Context Integration**: Uses retrieved templates as inspiration

## Response Quality Features

### 1. **Contextual Understanding**
- Analyzes the full query context
- Understands intent and urgency
- Incorporates detected entities

### 2. **Personalization**
- Uses customer name when available
- References specific details from query
- Adapts tone to situation

### 3. **Actionability**
- Provides clear next steps
- Sets realistic expectations
- Offers helpful information

### 4. **Empathy**
- Acknowledges customer concerns
- Shows understanding of urgency
- Maintains professional tone

### 5. **Accuracy**
- References specific error codes, amounts, dates
- Provides relevant technical guidance
- Sets appropriate response times

## Fallback Mechanisms

If Gemini API fails:

1. **Template Fallback**: Uses best matching canned response
2. **Personalization**: Still personalizes with customer name
3. **Default Response**: Generic but professional fallback

## Testing Response Generation

You can test response generation:

```python
from rag_system import RAGSystem

rag = RAGSystem()
result = rag.generate_response(
    query="Your query here",
    intent="technical_support",
    urgency="high",
    customer_name="John Doe"
)

print(result['response'])
```

## Integration Points

- **Email Channel**: Responses sent via `/api/submit_email`
- **Form Channel**: Responses shown in UI after submission
- **Chat Channel**: Responses returned in API response
- **Ticket Storage**: Responses stored in database with tickets

## Benefits

✅ **Intelligent**: Uses AI to understand context and generate relevant responses  
✅ **Consistent**: Maintains professional tone and quality  
✅ **Efficient**: Automatically generates responses without manual work  
✅ **Scalable**: Handles any number of queries automatically  
✅ **Improving**: Learns from templates and improves over time  

## Summary

The system uses **Google Gemini AI** through a **RAG system** to generate intelligent, contextual, and helpful responses to customer queries. The responses are:

- **Specific** to the customer's query
- **Personalized** with their name and situation
- **Actionable** with clear next steps
- **Empathetic** acknowledging their concerns
- **Professional** maintaining FinLink's brand voice

All responses are automatically generated when `auto_respond=True` is set (default), and are stored with tickets in the database.

