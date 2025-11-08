"""
RAG (Retrieval Augmented Generation) system for canned responses.
Uses HTML pages from the pages folder as knowledge base for semantic similarity search.
"""
import math
import os
import re
from collections import Counter
from typing import List, Dict, Optional
from pathlib import Path
import google.generativeai as genai
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()


class RAGSystem:
    def __init__(self, persist_directory: str = "./chroma_db"):
        """Initialize the RAG system with an in-memory vector store."""
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        try:
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        except:
            try:
                self.model = genai.GenerativeModel('gemini-pro')
            except:
                self.model = genai.GenerativeModel('gemini-1.5-flash-latest')
        self.vector_store = self._build_vector_store()
        print(f"Initialized RAG system with {len(self.vector_store)} documentation pages loaded from 'pages' folder")
    
    @staticmethod
    def _tokenize(text: str) -> Counter:
        tokens = re.findall(r"\b\w+\b", text.lower())
        return Counter(tokens)
    
    @staticmethod
    def _cosine_similarity(counter_a: Counter, counter_b: Counter) -> float:
        intersection = set(counter_a) & set(counter_b)
        numerator = sum(counter_a[token] * counter_b[token] for token in intersection)
        sum1 = math.sqrt(sum(count * count for count in counter_a.values()))
        sum2 = math.sqrt(sum(count * count for count in counter_b.values()))
        if sum1 == 0 or sum2 == 0:
            return 0.0
        return numerator / (sum1 * sum2)
    
    def _parse_html_page(self, html_file_path: str) -> Dict:
        """Parse an HTML page and extract relevant content using BeautifulSoup."""
        try:
            with open(html_file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extract category name from h1
            h1 = soup.find('h1')
            category_name = h1.get_text(strip=True) if h1 else "Unknown"
            
            # Extract category badge
            badge = soup.find('span', class_='category-badge')
            category_code = badge.get_text(strip=True) if badge else ""
            
            # Extract overview
            overview_section = soup.find('h2', string=re.compile('Overview', re.IGNORECASE))
            overview = ""
            if overview_section:
                overview_p = overview_section.find_next_sibling('p')
                overview = overview_p.get_text(strip=True) if overview_p else ""
            
            # Extract keywords
            keywords_section = soup.find('h2', string=re.compile('Keywords', re.IGNORECASE))
            keywords = []
            if keywords_section:
                keywords_div = keywords_section.find_next_sibling('div', class_='keywords')
                if keywords_div:
                    keyword_spans = keywords_div.find_all('span')
                    keywords = [span.get_text(strip=True) for span in keyword_spans]
            
            # Extract use cases
            use_cases_section = soup.find('h2', string=re.compile('Use Cases', re.IGNORECASE))
            use_cases = []
            if use_cases_section:
                use_cases_ul = use_cases_section.find_next_sibling('ul')
                if use_cases_ul:
                    use_cases = [li.get_text(strip=True) for li in use_cases_ul.find_all('li')]
            
            # Extract common scenarios
            scenarios_section = soup.find('h2', string=re.compile('Common Scenarios', re.IGNORECASE))
            scenarios = []
            if scenarios_section:
                scenarios_ul = scenarios_section.find_next_sibling('ul')
                if scenarios_ul:
                    scenarios = [li.get_text(strip=True) for li in scenarios_ul.find_all('li')]
            
            # Extract template response
            template_section = soup.find('h2', string=re.compile('Response Template', re.IGNORECASE))
            template_response = ""
            if template_section:
                template_box = template_section.find_next_sibling('div', class_='template-box')
                if template_box:
                    template_p = template_box.find('p')
                    template_response = template_p.get_text(strip=True) if template_p else ""
            
            # Extract response approach
            approach_section = soup.find('h2', string=re.compile('Response Approach', re.IGNORECASE))
            approach_steps = []
            if approach_section:
                approach_ol = approach_section.find_next_sibling('ol')
                if approach_ol:
                    approach_steps = [li.get_text(strip=True) for li in approach_ol.find_all('li')]
            
            # Build comprehensive document text for semantic search
            doc_text = f"""
            Category: {category_name} ({category_code})
            Overview: {overview}
            Keywords: {', '.join(keywords)}
            Use Cases: {'; '.join(use_cases[:5])}
            Common Scenarios: {'; '.join(scenarios[:5])}
            Response Template: {template_response}
            Response Approach: {'; '.join(approach_steps[:5])}
            """.strip()
            
            return {
                "category": category_code,
                "category_name": category_name,
                "keywords": keywords,
                "overview": overview,
                "use_cases": use_cases,
                "scenarios": scenarios,
                "template_response": template_response,
                "approach_steps": approach_steps,
                "document": doc_text
            }
        except Exception as e:
            print(f"Error parsing HTML file {html_file_path}: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _build_vector_store(self):
        """Build vector store from HTML pages in the pages folder."""
        vector_store = []
        pages_dir = Path("pages")
        
        if not pages_dir.exists():
            print(f"Warning: Pages directory not found at {pages_dir}. Falling back to canned responses.")
            return self._build_fallback_vector_store()
        
        # Read all HTML files except index.html
        html_files = [f for f in pages_dir.glob("*.html") if f.name != "index.html"]
        
        if not html_files:
            print("Warning: No HTML pages found in pages folder. Falling back to canned responses.")
            return self._build_fallback_vector_store()
        
        for html_file in html_files:
            parsed_data = self._parse_html_page(str(html_file))
            if parsed_data:
                metadata = {
                    "category": parsed_data['category'],
                    "category_name": parsed_data['category_name'],
                    "keywords": ",".join(parsed_data['keywords']),
                    "response": parsed_data['template_response'],
                    "overview": parsed_data['overview'],
                    "use_cases": "; ".join(parsed_data['use_cases'][:3]),
                    "scenarios": "; ".join(parsed_data['scenarios'][:3])
                }
                
                vector_store.append({
                    "id": f"page_{html_file.stem}",
                    "document": parsed_data['document'],
                    "metadata": metadata,
                    "tokens": self._tokenize(parsed_data['document'])
                })
        
        print(f"Built vector store from {len(vector_store)} HTML pages")
        return vector_store
    
    def _build_fallback_vector_store(self):
        """Fallback to original canned responses if HTML pages are not available."""
        vector_store = []
        from sample_data import get_canned_responses
        canned_responses = get_canned_responses()
        for i, response_data in enumerate(canned_responses):
            doc_text = f"""
            Category: {response_data['category']}
            Keywords: {', '.join(response_data['keywords'])}
            Response Template: {response_data['response']}
            """.strip()
            
            metadata = {
                "category": response_data['category'],
                "keywords": ",".join(response_data['keywords']),
                "response": response_data['response']
            }
            
            vector_store.append({
                "id": f"response_{i}",
                "document": doc_text,
                "metadata": metadata,
                "tokens": self._tokenize(doc_text)
            })
        return vector_store
    
    def retrieve_response(
        self, 
        query: str, 
        intent: str = None, 
        n_results: int = 3
    ) -> List[Dict]:
        """
        Retrieve relevant canned responses using semantic similarity search.
        
        Args:
            query: The customer query
            intent: Optional intent category to filter by
            n_results: Number of results to return
            
        Returns:
            List of relevant response documents with metadata
        """
        # Build search query with intent context if available
        search_query = query
        if intent:
            search_query = f"{intent}: {query}"
        
        query_tokens = self._tokenize(search_query)
        
        scored_entries = []
        for entry in self.vector_store:
            similarity = self._cosine_similarity(entry["tokens"], query_tokens)
            if intent and entry["metadata"]["category"].lower() == intent.lower():
                similarity *= 1.1  # boost matching intents slightly
            scored_entries.append((similarity, entry))
        
        scored_entries.sort(key=lambda item: item[0], reverse=True)
        
        # Format results similar to ChromaDB response
        retrieved_responses = []
        for score, entry in scored_entries[:n_results]:
            retrieved_responses.append({
                "document": entry["document"],
                "metadata": entry["metadata"],
                "distance": 1 - score,
                "id": entry["id"]
            })
        
        return retrieved_responses
    
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
        """
        Generate a personalized response using RAG + Gemini.
        Creates relevant, contextual responses based on query analysis.
        
        Args:
            query: The customer query
            intent: The classified intent
            urgency: Urgency level
            customer_name: Optional customer name for personalization
            reasoning: Optional classification reasoning
            key_entities: Optional list of key entities extracted from query
            sentiment: Optional sentiment analysis (positive, neutral, negative, urgent)
            assigned_team: Optional team assigned to handle the query
            response_time: Optional expected response time
            
        Returns:
            Dict with response, canned_templates, and metadata
        """
        # Retrieve relevant canned responses using semantic search
        retrieved = self.retrieve_response(query, intent, n_results=3)
        
        # Build context from retrieved responses with rich content from HTML pages
        context = ""
        if retrieved:
            context = "Relevant response templates and knowledge from documentation pages:\n\n"
            for i, item in enumerate(retrieved, 1):
                metadata = item.get('metadata', {})
                category_name = metadata.get('category_name', '')
                category = metadata.get('category', '')
                overview = metadata.get('overview', '')
                response_text = metadata.get('response', '')
                use_cases = metadata.get('use_cases', '')
                scenarios = metadata.get('scenarios', '')
                
                # Build context entry
                context_entry = f"{i}. [{category_name} ({category})]\n"
                if overview:
                    context_entry += f"   Overview: {overview}\n"
                if use_cases:
                    context_entry += f"   Use Cases: {use_cases}\n"
                if scenarios:
                    context_entry += f"   Common Scenarios: {scenarios}\n"
                if response_text:
                    context_entry += f"   Template Response: {response_text}\n"
                
                # If no metadata fields, use document content
                if not overview and not response_text:
                    doc_content = item.get('document', '')
                    if doc_content:
                        context_entry += f"   Content: {doc_content[:300]}...\n"
                
                context += context_entry + "\n"
        
        # Create prompt for Gemini with enhanced context
        prompt = self._create_response_prompt(
            query, 
            context, 
            intent, 
            urgency, 
            customer_name,
            reasoning,
            key_entities,
            sentiment,
            assigned_team,
            response_time
        )
        
        try:
            # Generate response with Gemini
            response = self.model.generate_content(prompt)
            generated_response = response.text.strip()
            
            # Post-process to ensure proper formatting
            generated_response = self._format_response(generated_response, customer_name)
            
            return {
                "response": generated_response,
                "canned_templates_used": len(retrieved),
                "retrieved_responses": retrieved,
                "method": "rag_generated"
            }
        
        except Exception as e:
            print(f"Error generating response: {e}")
            # Fallback to best canned response
            if retrieved:
                best_response = retrieved[0]['metadata'].get('response', '')
                
                # Personalize the fallback response
                if customer_name:
                    best_response = best_response.replace("[Customer]", customer_name)
                    best_response = best_response.replace("[Developer]", customer_name)
                else:
                    best_response = best_response.replace("[Customer],", "")
                    best_response = best_response.replace("Dear [Customer],", "Hello,")
                    best_response = best_response.replace("Hi [Customer],", "Hello,")
                    best_response = best_response.replace("Hi [Developer],", "Hello,")
                
                return {
                    "response": best_response,
                    "canned_templates_used": 1,
                    "retrieved_responses": retrieved,
                    "method": "canned_fallback"
                }
            else:
                return {
                    "response": "Thank you for contacting FinLink. Your query has been received and assigned to the appropriate team. We will respond within 24 hours.",
                    "canned_templates_used": 0,
                    "retrieved_responses": [],
                    "method": "default_fallback"
                }
    
    def _create_response_prompt(
        self,
        query: str,
        context: str,
        intent: str,
        urgency: str,
        customer_name: str,
        reasoning: str = None,
        key_entities: List[str] = None,
        sentiment: str = None,
        assigned_team: str = None,
        response_time: str = None
    ) -> str:
        """Create an enhanced prompt for generating relevant, contextual responses."""
        # Determine appropriate greeting based on sentiment and intent
        if customer_name:
            if sentiment == "urgent" or urgency == "critical":
                greeting = f"Dear {customer_name},"
            elif intent == "technical_support":
                greeting = f"Hi {customer_name},"
            else:
                greeting = f"Dear {customer_name},"
        else:
            greeting = "Hello," if urgency in ["critical", "high"] else "Hello,"
        
        # Build classification details section
        classification_details = f"""Query Classification:
- Intent: {intent}
- Urgency: {urgency}"""
        
        if reasoning:
            classification_details += f"\n- Analysis: {reasoning}"
        
        if key_entities:
            entities_str = ", ".join(key_entities[:5])  # Limit to top 5 entities
            classification_details += f"\n- Key Details: {entities_str}"
        
        if sentiment and sentiment != "neutral":
            classification_details += f"\n- Sentiment: {sentiment}"
        
        if assigned_team:
            classification_details += f"\n- Assigned Team: {assigned_team}"
        
        if response_time:
            classification_details += f"\n- Expected Response Time: {response_time}"
        
        # Build urgency-specific guidance
        urgency_guidance = ""
        if urgency == "critical":
            urgency_guidance = "\n- This is a CRITICAL issue requiring immediate attention. Express urgency and immediate action."
        elif urgency == "high":
            urgency_guidance = "\n- This is a HIGH priority issue. Emphasize quick resolution and priority handling."
        elif urgency == "low":
            urgency_guidance = "\n- This is a LOW priority issue. Be helpful but acknowledge standard processing time."
        
        # Build sentiment-specific guidance
        sentiment_guidance = ""
        if sentiment == "negative":
            sentiment_guidance = "\n- The customer sentiment is negative. Be empathetic, acknowledge their frustration, and focus on resolution."
        elif sentiment == "urgent":
            sentiment_guidance = "\n- The customer is expressing urgency. Show understanding and provide clear, immediate next steps."
        
        prompt = f"""You are an expert customer support representative for FinLink, a B2B fintech platform specializing in payment processing, KYC verification, and financial services for businesses.

CUSTOMER'S QUERY:
"{query}"

QUERY ANALYSIS:
{classification_details}
{urgency_guidance}
{sentiment_guidance}

KNOWLEDGE BASE CONTEXT (from documentation pages - use this rich context to generate accurate responses):
{context if context else "No specific documentation pages found - generate a professional, helpful response based on FinLink's best practices and your knowledge of customer support."}

YOUR TASK:
Generate a professional, helpful, and personalized response that directly addresses the customer's specific query. The response should be properly formatted with clear paragraphs and line breaks.

RESPONSE FORMAT (CRITICAL - Follow this exact structure):

{greeting}

[Paragraph 1: Acknowledgment]
- Acknowledge their specific issue or question clearly
- If key entities were detected (error codes, amounts, dates, account types), reference them naturally
- Show understanding of their situation

[Paragraph 2: Address the Query]
- Use the knowledge base context above to provide accurate, relevant information
- Reference the overview, use cases, and scenarios from the documentation pages when relevant
- Provide relevant information or next steps based on their specific question
- If it's a technical issue, provide troubleshooting guidance or escalation info
- If it's a billing question, provide relevant details or next steps
- If it's a KYC/verification issue, explain the process or status
- If it's a compliance question, provide appropriate guidance
- If it's a sales inquiry, provide helpful information about products/services

[Paragraph 3: Set Expectations]
- Based on urgency level ({urgency}), set appropriate response time expectations
- If assigned to a team, mention that the appropriate team will handle this
- Provide clear next steps or what they can expect

Best regards,
FinLink Support Team

CRITICAL FORMATTING REQUIREMENTS:
- Use proper line breaks between paragraphs (double line break)
- Each paragraph should be 2-4 sentences
- Use single line breaks within paragraphs for readability
- Keep paragraphs focused and concise
- Use proper email formatting with line breaks
- Do NOT use markdown formatting (no **, no #, no lists with - or *)
- Write in plain text with proper line breaks
- Make it look like a professional email response

CRITICAL GUIDELINES:
- Be SPECIFIC to their exact query - address what they actually asked, not generic information
- Use the KNOWLEDGE BASE CONTEXT above - incorporate information from the documentation pages naturally
- Use a CONVERSATIONAL but PROFESSIONAL tone - friendly but authoritative
- If they mentioned specific details (error codes, amounts, dates), incorporate them naturally
- Match the URGENCY level - critical issues need immediate action language, low priority can be more relaxed
- Show EMPATHY if sentiment is negative or urgent - acknowledge their concern
- Be ACTIONABLE - provide clear next steps or information they can use
- Keep it CONCISE but COMPLETE - typically 3-4 paragraphs, but adjust based on complexity
- PERSONALIZE - use their name if provided, reference their specific situation
- Don't make promises you can't keep - be realistic about timelines and capabilities

RESPONSE STYLE:
- Write naturally, as if you're a real support agent responding to this exact query
- Don't use placeholder text or generic phrases
- Make it feel like a genuine, helpful response tailored to their specific situation
- If the query is urgent or critical, convey urgency appropriately
- If the query is a simple question, provide a direct answer
- Use the knowledge from the documentation pages to ensure accuracy and completeness

Now generate the response following the exact format above with proper line breaks:
"""
        return prompt
    
    def _format_response(self, response: str, customer_name: str = None) -> str:
        """
        Post-process response to ensure proper formatting.
        Ensures consistent email-style formatting with proper line breaks.
        """
        if not response:
            return response
        
        # Remove any markdown formatting
        response = response.replace('**', '').replace('*', '').replace('#', '')
        
        # Ensure proper line breaks between paragraphs
        # Replace multiple spaces with single space
        response = re.sub(r' +', ' ', response)
        
        # Ensure double line breaks between paragraphs
        response = re.sub(r'\n\s*\n\s*\n+', '\n\n', response)
        
        # Ensure single line breaks within paragraphs are preserved
        # But make sure we have proper paragraph separation
        
        # Clean up any trailing whitespace
        response = response.strip()
        
        # Ensure it ends with proper closing
        if not response.endswith('FinLink Support Team'):
            if 'Best regards' not in response and 'Regards' not in response:
                response += '\n\nBest regards,\nFinLink Support Team'
        
        return response
    
    def add_response_template(
        self,
        category: str,
        keywords: List[str],
        response: str
    ) -> str:
        """Add a new canned response template to the system."""
        # Create document
        doc_text = f"""
        Category: {category}
        Keywords: {', '.join(keywords)}
        Response Template: {response}
        """
        
        # Generate unique ID
        response_id = f"response_{self.collection.count()}"
        
        # Add to collection
        self.collection.add(
            documents=[doc_text.strip()],
            metadatas=[{
                "category": category,
                "keywords": ",".join(keywords),
                "response": response
            }],
            ids=[response_id]
        )
        
        return response_id
    
    def search_templates(self, search_term: str, n_results: int = 5) -> List[Dict]:
        """Search for existing templates by keyword or category."""
        return self.retrieve_response(search_term, n_results=n_results)


def generate_quick_response(
    query: str, 
    intent: str = None, 
    urgency: str = "medium",
    customer_name: str = None,
    reasoning: str = None,
    key_entities: List[str] = None,
    sentiment: str = None
) -> str:
    """Quick utility function to generate a response."""
    rag = RAGSystem()
    result = rag.generate_response(
        query, 
        intent, 
        urgency,
        customer_name=customer_name,
        reasoning=reasoning,
        key_entities=key_entities,
        sentiment=sentiment
    )
    return result['response']


if __name__ == "__main__":
    # Test the RAG system
    rag = RAGSystem()
    
    test_queries = [
        {
            "query": "Hello, we tried adding a new vendor bank account, but the verification is stuck on 'Pending' for 2 days.",
            "intent": "kyc_verification",
            "urgency": "medium",
            "customer_name": "John Doe"
        },
        {
            "query": "API integration keeps failing with error code 403 when we push payment data.",
            "intent": "technical_support",
            "urgency": "high",
            "customer_name": None
        },
        {
            "query": "Our monthly invoice for August shows an extra $120 charge. Can you please review it?",
            "intent": "billing_finance",
            "urgency": "medium",
            "customer_name": None
        }
    ]
    
    print("Testing RAG System:\n")
    for i, test in enumerate(test_queries, 1):
        print(f"Query {i}: {test['query']}")
        print(f"Intent: {test['intent']}, Urgency: {test['urgency']}")
        
        result = rag.generate_response(
            test['query'],
            test['intent'],
            test['urgency'],
            test.get('customer_name')
        )
        
        print(f"\nGenerated Response:")
        print(result['response'])
        print(f"\nMethod: {result['method']}")
        print(f"Templates used: {result['canned_templates_used']}")
        print("-" * 80 + "\n")
