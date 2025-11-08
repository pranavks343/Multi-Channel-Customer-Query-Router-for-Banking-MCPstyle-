"""
Intent classification system using Google Gemini API.
Classifies customer queries by intent and urgency level.
"""

import json
import os
import re
from typing import Dict, Tuple

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


class IntentClassifier:
    def __init__(self, learning_system=None):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")

        genai.configure(api_key=api_key)
        try:
            self.model = genai.GenerativeModel("gemini-1.5-flash")
        except:
            try:
                self.model = genai.GenerativeModel("gemini-pro")
            except:
                self.model = genai.GenerativeModel("gemini-1.5-flash-latest")

        self.learning_system = learning_system

        # Define intent categories and their keywords
        self.intent_categories = {
            "kyc_verification": [
                "account verification",
                "identity check",
                "kyc",
                "document upload",
                "verification stuck",
                "pending verification",
                "id verification",
            ],
            "technical_support": [
                "api error",
                "integration",
                "webhook",
                "error code",
                "technical issue",
                "500 error",
                "403 error",
                "404 error",
                "timeout",
                "rate limit",
                "sdk",
            ],
            "billing_finance": [
                "invoice",
                "billing",
                "charge",
                "payment",
                "refund",
                "subscription",
                "pricing",
                "cost",
                "fee",
                "balance",
                "transaction",
            ],
            "compliance_regulatory": [
                "compliance",
                "gdpr",
                "pci dss",
                "soc 2",
                "audit",
                "regulation",
                "data protection",
                "privacy",
                "security certificate",
                "certification",
            ],
            "sales_inquiry": [
                "demo",
                "pricing plan",
                "enterprise",
                "partnership",
                "white label",
                "new customer",
                "signup",
                "trial",
                "features",
            ],
            "general_support": [
                "help",
                "how to",
                "question",
                "information",
                "documentation",
                "guide",
            ],
        }

        # Load learned keywords if learning system is available
        if self.learning_system:
            self._load_learned_keywords()

        # Define team mappings
        self.team_mapping = {
            "kyc_verification": "KYC Team",
            "technical_support": "Tech Support",
            "billing_finance": "Finance Team",
            "compliance_regulatory": "Compliance Team",
            "sales_inquiry": "Sales Team",
            "general_support": "Tech Support",
        }

        # Load learned team mappings if learning system is available
        if self.learning_system:
            self._load_learned_team_mappings()

    def classify_intent(self, message: str, subject: str = None) -> Dict:
        """
        Classify the intent of a customer query using Gemini AI.

        Args:
            message: The customer query message
            subject: Optional subject line

        Returns:
            Dict containing intent, urgency, assigned_team, and confidence
        """
        # Combine subject and message for better context
        full_text = f"{subject or ''}\n{message}".strip()

        # Create prompt for Gemini
        prompt = self._create_classification_prompt(full_text)

        try:
            # Call Gemini API
            response = self.model.generate_content(prompt)
            result = self._parse_gemini_response(response.text)

            # Add team assignment based on intent
            result["assigned_team"] = self.team_mapping.get(
                result["intent"], "Tech Support"
            )

            return result

        except Exception as e:
            print(f"Error in Gemini classification: {e}")
            # Fallback to rule-based classification
            return self._fallback_classification(full_text)

    def _create_classification_prompt(self, text: str) -> str:
        """Create a detailed prompt for Gemini to classify the query with enhanced NLP understanding."""
        prompt = f"""You are an expert NLP classifier for FinLink, a B2B fintech platform. Your task is to deeply understand the semantic meaning, context, and intent of customer messages to route them accurately.

Customer Query:
{text}

ANALYSIS INSTRUCTIONS:
1. Read the entire message carefully and understand the core issue or request
2. Identify key entities: products, services, error codes, dates, amounts, account types
3. Detect sentiment and urgency indicators (urgent words, emotional tone, business impact)
4. Understand context: Is this blocking operations? Is it a question vs. a problem?
5. Consider implicit meanings: "stuck" = blocking issue, "dispute" = needs compliance review

INTENT CATEGORIES (choose ONE that best matches the semantic meaning):

1. kyc_verification
   - Account verification, identity verification, KYC processes
   - Document upload issues, verification status checks
   - Identity checks, background verification
   - Account activation problems related to verification
   - Examples: "verification stuck", "can't verify account", "document rejected", "KYC pending"

2. technical_support
   - API errors, integration problems, technical bugs
   - Webhook failures, SDK issues, authentication errors
   - System errors, timeouts, rate limits, connection issues
   - Code-related problems, developer issues
   - Examples: "API returning 403", "webhook not working", "integration failing", "SDK error"

3. billing_finance
   - Invoice questions, payment processing, charges
   - Refund requests, subscription management, pricing questions
   - Transaction inquiries, balance checks, payment methods
   - Billing discrepancies (but disputes go to compliance)
   - Examples: "invoice incorrect", "payment failed", "refund needed", "subscription renewal"

4. compliance_regulatory
   - GDPR, PCI DSS, SOC 2, regulatory compliance
   - Audit requests, security certifications, data protection
   - Policy questions, regulatory requirements
   - Billing DISPUTES and discrepancies requiring investigation
   - Examples: "need SOC 2 certificate", "GDPR compliance", "audit request", "billing dispute"

5. sales_inquiry
   - Demo requests, pricing inquiries, enterprise plans
   - Partnership opportunities, white-label inquiries
   - New customer onboarding, feature requests for sales
   - Trial requests, signup questions
   - Examples: "want a demo", "enterprise pricing", "partnership opportunity", "new customer"

6. general_support
   - General help, documentation requests, how-to questions
   - Feature explanations, usage questions, tutorials
   - Non-urgent information requests
   - Examples: "how do I...", "where can I find...", "documentation link", "general question"

URGENCY LEVELS (determine based on business impact and blocking nature):

- critical: 
  * System completely down or inaccessible
  * Security breaches or data leaks
  * Payment processing completely blocked
  * Service outages affecting all users
  * Operations completely halted
  * Keywords: "down", "not working at all", "blocked", "emergency", "urgent", "critical"

- high:
  * API errors affecting live operations
  * Verification delays blocking business
  * Billing issues affecting service access
  * Integration problems preventing transactions
  * Time-sensitive issues with business impact
  * Keywords: "error", "failing", "stuck", "delayed", "urgent", "affecting", "blocking"

- medium:
  * Feature requests, minor bugs
  * General inquiries with moderate importance
  * Documentation requests
  * Non-blocking technical questions
  * Standard verification requests
  * Keywords: "question", "request", "information", "how to", "can you"

- low:
  * Information requests, feedback
  * Suggestions, non-urgent questions
  * General inquiries without time pressure
  * Exploratory questions
  * Keywords: "just wondering", "curious", "feedback", "suggestion", "information"

CLASSIFICATION RULES:
- If message mentions "dispute", "discrepancy", "wrong charge", "incorrect billing" → compliance_regulatory (high urgency)
- If message mentions "verification", "verify", "KYC", "document" → kyc_verification
- If message mentions "API", "error code", "integration", "webhook" → technical_support
- If message mentions "demo", "pricing", "enterprise", "partnership" → sales_inquiry
- Consider the PRIMARY concern - what is the customer trying to achieve?
- Look for action verbs: "need", "want", "can't", "stuck", "failing", "request"

Respond ONLY with a JSON object in this exact format:
{{
    "intent": "category_name",
    "urgency": "urgency_level",
    "reasoning": "Detailed explanation: what you understood from the message, key entities detected, why this category and urgency level",
    "confidence": 0.85,
    "key_entities": ["entity1", "entity2"],
    "sentiment": "neutral|positive|negative|urgent"
}}

Important:
- Choose exactly ONE intent category that best matches the semantic meaning
- Urgency should be one of: critical, high, medium, low
- Confidence should be between 0.0 and 1.0 (higher for clear, unambiguous messages)
- Reasoning should explain your understanding (2-3 sentences)
- Extract key entities mentioned (error codes, amounts, dates, account types, etc.)
- Detect sentiment to help with routing priority
"""
        return prompt

    def _parse_gemini_response(self, response_text: str) -> Dict:
        """Parse Gemini's response and extract classification results with enhanced NLP data."""
        try:
            # Try to find JSON in the response (handle nested JSON)
            json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                result = json.loads(json_str)

                # Validate required fields
                if "intent" not in result or "urgency" not in result:
                    raise ValueError("Missing required fields in response")

                # Ensure confidence is present
                if "confidence" not in result:
                    result["confidence"] = 0.8

                # Validate urgency level
                if result["urgency"] not in ["critical", "high", "medium", "low"]:
                    result["urgency"] = "medium"

                # Ensure optional NLP fields are present
                if "key_entities" not in result:
                    result["key_entities"] = []
                if "sentiment" not in result:
                    result["sentiment"] = "neutral"
                if "reasoning" not in result:
                    result["reasoning"] = "Classified based on message content"

                return result
            else:
                raise ValueError("No JSON found in response")

        except Exception as e:
            print(f"Error parsing Gemini response: {e}")
            print(
                f"Response text: {response_text[:500]}..."
            )  # Truncate for readability
            # Return a default classification
            return {
                "intent": "general_support",
                "urgency": "medium",
                "reasoning": "Failed to parse AI response - using fallback classification",
                "confidence": 0.5,
                "key_entities": [],
                "sentiment": "neutral",
            }

    def _fallback_classification(self, text: str) -> Dict:
        """
        Enhanced fallback rule-based classification if Gemini API fails.
        Uses sophisticated keyword matching and pattern recognition.
        """
        text_lower = text.lower()

        # Extract key entities (simple pattern matching)
        key_entities = []

        # Extract error codes (e.g., "403", "500", "404")
        error_codes = re.findall(r"\b\d{3}\b", text)
        key_entities.extend([f"error_{code}" for code in error_codes])

        # Extract amounts (e.g., "$120", "100 dollars")
        amounts = re.findall(r"\$?\d+\.?\d*\s*(?:dollars?|USD)?", text, re.IGNORECASE)
        key_entities.extend(amounts)

        # Extract dates (simple patterns)
        dates = re.findall(
            r"\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{1,2}",
            text_lower,
        )
        key_entities.extend(dates)

        # Detect sentiment
        negative_words = [
            "error",
            "failed",
            "stuck",
            "problem",
            "issue",
            "dispute",
            "wrong",
            "incorrect",
            "can't",
            "unable",
        ]
        urgent_words = [
            "urgent",
            "critical",
            "emergency",
            "immediately",
            "asap",
            "blocked",
            "down",
        ]
        positive_words = ["thanks", "thank you", "great", "helpful", "appreciate"]

        sentiment = "neutral"
        if any(word in text_lower for word in urgent_words):
            sentiment = "urgent"
        elif any(word in text_lower for word in negative_words):
            sentiment = "negative"
        elif any(word in text_lower for word in positive_words):
            sentiment = "positive"

        # Enhanced urgency detection with context understanding
        urgency = "medium"
        urgency_score = 0

        # Critical indicators
        critical_patterns = [
            r"\b(?:down|not working|completely|totally|entirely)\s+(?:down|broken|failed)",
            r"\b(?:emergency|critical|urgent)\s+(?:issue|problem|situation)",
            r"\b(?:security|breach|leak|hack)",
            r"\b(?:blocked|blocking)\s+(?:all|everything|operations|business)",
        ]
        for pattern in critical_patterns:
            if re.search(pattern, text_lower):
                urgency = "critical"
                urgency_score = 3
                break

        if urgency_score == 0:
            # High urgency indicators
            high_patterns = [
                r"\b(?:error|failing|failed|stuck|delayed)\s+(?:for|since)\s+\d+",
                r"\b(?:affecting|blocking|preventing)\s+(?:operations|business|transactions)",
                r"\b(?:dispute|discrepancy|wrong charge|incorrect billing)",
                r"\b(?:can\'t|cannot|unable)\s+(?:process|complete|access|verify)",
            ]
            for pattern in high_patterns:
                if re.search(pattern, text_lower):
                    urgency = "high"
                    urgency_score = 2
                    break

        if urgency_score == 0:
            # Low urgency indicators
            low_patterns = [
                r"\b(?:just wondering|curious|feedback|suggestion)",
                r"\b(?:information|info|question)\s+(?:about|regarding)",
                r"\b(?:how do|where can|can you tell)",
            ]
            for pattern in low_patterns:
                if re.search(pattern, text_lower):
                    urgency = "low"
                    urgency_score = 0
                    break

        # Enhanced intent classification with weighted scoring
        intent_scores = {}

        # Special handling for disputes (should go to compliance)
        if any(
            word in text_lower
            for word in [
                "dispute",
                "discrepancy",
                "wrong charge",
                "incorrect billing",
                "billing error",
            ]
        ):
            intent_scores["compliance_regulatory"] = 10  # High priority
            urgency = "high" if urgency != "critical" else urgency

        # Score each intent category
        for intent, keywords in self.intent_categories.items():
            score = 0
            for keyword in keywords:
                # Exact phrase match gets higher score
                if keyword in text_lower:
                    score += 2
                # Word boundary match
                elif re.search(r"\b" + re.escape(keyword) + r"\b", text_lower):
                    score += 1

            # Boost score for context-specific patterns
            if intent == "kyc_verification":
                if re.search(
                    r"\b(?:verify|verification|kyc|document)\s+(?:stuck|pending|failed|issue)",
                    text_lower,
                ):
                    score += 3
            elif intent == "technical_support":
                if re.search(
                    r"\b(?:api|webhook|integration|sdk)\s+(?:error|failing|not working)",
                    text_lower,
                ):
                    score += 3
            elif intent == "billing_finance":
                if re.search(
                    r"\b(?:invoice|payment|charge|refund|billing)\s+(?:question|issue|problem)",
                    text_lower,
                ):
                    score += 2

            if score > 0:
                intent_scores[intent] = score

        # Get the intent with highest score
        if intent_scores:
            intent = max(intent_scores, key=intent_scores.get)
            max_score = intent_scores[intent]
            # Calculate confidence based on score and clarity
            confidence = min(0.85, 0.5 + (max_score * 0.05))
        else:
            intent = "general_support"
            confidence = 0.5

        # Generate reasoning
        reasoning_parts = []
        reasoning_parts.append(f"Classified as '{intent}' using keyword matching")
        if key_entities:
            reasoning_parts.append(f"Detected entities: {', '.join(key_entities[:3])}")
        reasoning_parts.append(
            f"Sentiment: {sentiment}, Urgency determined by context analysis"
        )
        reasoning = ". ".join(reasoning_parts)

        return {
            "intent": intent,
            "urgency": urgency,
            "reasoning": reasoning,
            "confidence": confidence,
            "assigned_team": self.team_mapping.get(intent, "Tech Support"),
            "key_entities": key_entities[:5],  # Limit to top 5
            "sentiment": sentiment,
        }

    def _load_learned_keywords(self):
        """Load learned keywords from the learning system and update intent categories."""
        if not self.learning_system:
            return

        for intent in self.intent_categories.keys():
            learned_keywords = self.learning_system.get_learned_keywords_for_intent(
                intent
            )
            # Merge learned keywords with existing ones
            existing_keywords = set(self.intent_categories[intent])
            new_keywords = [
                kw for kw in learned_keywords if kw not in existing_keywords
            ]
            self.intent_categories[intent].extend(
                new_keywords[:10]
            )  # Add top 10 learned keywords

    def _load_learned_team_mappings(self):
        """Load learned team mappings from the learning system."""
        if not self.learning_system:
            return

        for intent in self.intent_categories.keys():
            learned_team = self.learning_system.get_learned_team_for_intent(intent)
            if learned_team:
                # Update team mapping if learned team is different and has high confidence
                self.team_mapping[intent] = learned_team

    def update_from_learning(self):
        """Refresh learned patterns from the learning system."""
        self._load_learned_keywords()
        self._load_learned_team_mappings()

    def batch_classify(self, queries: list) -> list:
        """
        Classify multiple queries in batch.

        Args:
            queries: List of dicts with 'message' and optional 'subject'

        Returns:
            List of classification results
        """
        results = []
        for query in queries:
            result = self.classify_intent(
                query.get("message", ""), query.get("subject")
            )
            results.append(result)

        return results


# Utility function for quick classification
def classify_query(message: str, subject: str = None) -> Dict:
    """Quick utility to classify a single query."""
    classifier = IntentClassifier()
    return classifier.classify_intent(message, subject)


if __name__ == "__main__":
    # Test the classifier
    classifier = IntentClassifier()

    test_queries = [
        {
            "subject": "API Error 403",
            "message": "API integration keeps failing with error code 403 when we push payment data.",
        },
        {
            "subject": "Billing Issue",
            "message": "Our monthly invoice for August shows an extra $120 charge. Can you please review it?",
        },
        {
            "subject": "Account Verification",
            "message": "We tried adding a new vendor bank account, but the verification is stuck on 'Pending' for 2 days.",
        },
    ]

    print("Testing Intent Classifier:\n")
    for i, query in enumerate(test_queries, 1):
        print(f"Query {i}: {query['subject']}")
        result = classifier.classify_intent(query["message"], query["subject"])
        print(f"Intent: {result['intent']}")
        print(f"Urgency: {result['urgency']}")
        print(f"Team: {result['assigned_team']}")
        print(f"Confidence: {result['confidence']:.2f}")
        print(f"Reasoning: {result.get('reasoning', 'N/A')}")
        print("-" * 60)
