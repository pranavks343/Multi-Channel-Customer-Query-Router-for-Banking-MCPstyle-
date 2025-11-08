"""
Learning System for dynamic adaptation based on user inputs.
Analyzes tickets, learns patterns, and updates classification/routing rules.
"""

import re
from collections import Counter, defaultdict
from typing import Dict, List, Optional

from database import Database


class LearningSystem:
    def __init__(self, db: Database = None):
        """Initialize the learning system."""
        self.db = db or Database()
        self.min_pattern_confidence = 0.6
        self.min_pattern_usage = 2  # Minimum times a pattern must appear to be learned

    def learn_from_ticket(self, ticket: Dict):
        """
        Learn from a single ticket - extract patterns and update knowledge.

        Args:
            ticket: Ticket dictionary with message, intent, urgency, assigned_team, etc.
        """
        message = ticket.get("message", "").lower()
        subject = ticket.get("subject", "").lower()
        intent = ticket.get("intent")
        team = ticket.get("assigned_team")

        # Extract keywords from message
        keywords = self._extract_keywords(message + " " + subject)

        # Learn intent-keyword associations
        for keyword in keywords:
            if len(keyword) > 3:  # Only meaningful keywords
                self.db.save_learning_pattern(
                    pattern_type="intent_keyword",
                    pattern_key=intent,
                    pattern_value=keyword,
                    confidence=1.0,
                )

        # Learn team-intent associations (successful routing)
        if intent and team:
            self.db.save_learning_pattern(
                pattern_type="team_intent",
                pattern_key=team,
                pattern_value=intent,
                confidence=1.0,
            )

    def learn_from_reassignment(
        self,
        ticket_id: str,
        original_team: str,
        new_team: str,
        original_intent: str = None,
        reason: str = None,
    ):
        """
        Learn from ticket reassignments - this is negative feedback.

        Args:
            ticket_id: Ticket ID
            original_team: Originally assigned team
            new_team: Team it was reassigned to
            original_intent: Original intent classification
            reason: Reason for reassignment
        """
        # Save feedback
        self.db.save_feedback(
            ticket_id=ticket_id,
            original_team=original_team,
            corrected_team=new_team,
            original_intent=original_intent,
            feedback_type="reassignment",
            feedback_data={"reason": reason},
        )

        # Get the ticket to learn from
        ticket = self.db.get_ticket(ticket_id)
        if ticket:
            # Learn what the correct team should be
            intent = ticket.get("intent")
            if intent and new_team:
                # Increase confidence for correct team-intent mapping
                self.db.save_learning_pattern(
                    pattern_type="team_intent",
                    pattern_key=new_team,
                    pattern_value=intent,
                    confidence=1.0,
                )

    def analyze_and_update_patterns(self):
        """
        Analyze all tickets and update learning patterns.
        This should be called periodically to refresh patterns.
        """
        # Get all tickets
        tickets = self.db.get_all_tickets()

        # Count successful routing patterns
        intent_team_counts = defaultdict(lambda: defaultdict(int))
        intent_keyword_counts = defaultdict(lambda: defaultdict(int))

        for ticket in tickets:
            intent = ticket.get("intent")
            team = ticket.get("assigned_team")
            message = ticket.get("message", "").lower()
            subject = ticket.get("subject", "").lower()

            # Check if ticket was reassigned (negative feedback)
            routing_events = self.db.get_routing_events(ticket["ticket_id"])
            was_reassigned = any(
                event.get("event_type") == "ticket_reassigned"
                for event in routing_events
            )

            # Only learn from successful routings (not reassigned)
            if not was_reassigned and intent and team:
                intent_team_counts[intent][team] += 1

            # Extract keywords for intent
            if intent:
                keywords = self._extract_keywords(message + " " + subject)
                for keyword in keywords:
                    if len(keyword) > 3:
                        intent_keyword_counts[intent][keyword] += 1

        # Update patterns based on frequency
        for intent, team_counts in intent_team_counts.items():
            if team_counts:
                # Most common team for this intent
                most_common_team = max(team_counts.items(), key=lambda x: x[1])
                team_name, count = most_common_team

                if count >= self.min_pattern_usage:
                    confidence = min(1.0, count / 10.0)  # Confidence based on frequency
                    self.db.save_learning_pattern(
                        pattern_type="team_intent",
                        pattern_key=team_name,
                        pattern_value=intent,
                        confidence=confidence,
                    )

        # Update keyword patterns
        for intent, keyword_counts in intent_keyword_counts.items():
            for keyword, count in keyword_counts.items():
                if count >= self.min_pattern_usage:
                    confidence = min(1.0, count / 5.0)
                    self.db.save_learning_pattern(
                        pattern_type="intent_keyword",
                        pattern_key=intent,
                        pattern_value=keyword,
                        confidence=confidence,
                    )

    def get_learned_keywords_for_intent(self, intent: str) -> List[str]:
        """Get learned keywords for a specific intent."""
        patterns = self.db.get_learning_patterns("intent_keyword")

        keywords = [
            p["pattern_value"]
            for p in patterns
            if p["pattern_key"] == intent
            and p["confidence"] >= self.min_pattern_confidence
        ]

        # Sort by usage count
        keyword_usage = {
            p["pattern_value"]: p["usage_count"]
            for p in patterns
            if p["pattern_key"] == intent
        }
        keywords.sort(key=lambda k: keyword_usage.get(k, 0), reverse=True)

        return keywords[:20]  # Return top 20 keywords

    def get_learned_team_for_intent(self, intent: str) -> Optional[str]:
        """Get the most likely team for an intent based on learned patterns."""
        patterns = self.db.get_learning_patterns("team_intent")

        # Find patterns matching this intent
        matching_patterns = [
            p
            for p in patterns
            if p["pattern_value"] == intent
            and p["confidence"] >= self.min_pattern_confidence
        ]

        if matching_patterns:
            # Return team with highest confidence and usage
            best_pattern = max(
                matching_patterns, key=lambda p: (p["confidence"], p["usage_count"])
            )
            return best_pattern["pattern_key"]

        return None

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract meaningful keywords from text."""
        # Remove common stop words
        stop_words = {
            "the",
            "a",
            "an",
            "and",
            "or",
            "but",
            "in",
            "on",
            "at",
            "to",
            "for",
            "of",
            "with",
            "by",
            "from",
            "as",
            "is",
            "was",
            "are",
            "were",
            "been",
            "be",
            "have",
            "has",
            "had",
            "do",
            "does",
            "did",
            "will",
            "would",
            "should",
            "could",
            "may",
            "might",
            "must",
            "can",
            "this",
            "that",
            "these",
            "those",
            "i",
            "you",
            "he",
            "she",
            "it",
            "we",
            "they",
            "what",
            "which",
            "who",
            "whom",
            "whose",
            "where",
            "when",
            "why",
            "how",
            "all",
            "each",
            "every",
            "both",
            "few",
            "more",
            "most",
            "other",
            "some",
            "such",
            "no",
            "nor",
            "not",
            "only",
            "own",
            "same",
            "so",
            "than",
            "too",
            "very",
            "just",
            "now",
        }

        # Extract words
        words = re.findall(r"\b[a-z]{3,}\b", text.lower())

        # Filter stop words
        keywords = [w for w in words if w not in stop_words]

        return keywords

    def get_learning_stats(self) -> Dict:
        """Get statistics about the learning system."""
        patterns = self.db.get_learning_patterns()
        feedback = self.db.get_feedback_history(limit=1000)

        pattern_types = Counter(p["pattern_type"] for p in patterns)

        return {
            "total_patterns": len(patterns),
            "pattern_types": dict(pattern_types),
            "total_feedback": len(feedback),
            "reassignments": sum(
                1 for f in feedback if f["feedback_type"] == "reassignment"
            ),
            "top_learned_intents": self._get_top_learned_intents(patterns),
        }

    def _get_top_learned_intents(self, patterns: List[Dict]) -> Dict[str, int]:
        """Get top learned intents by pattern count."""
        intent_counts = Counter()
        for p in patterns:
            if p["pattern_type"] == "intent_keyword":
                intent_counts[p["pattern_key"]] += 1

        return dict(intent_counts.most_common(10))


if __name__ == "__main__":
    # Test the learning system
    learning = LearningSystem()

    print("=" * 80)
    print("Learning System Test")
    print("=" * 80)

    # Analyze existing tickets
    print("\nAnalyzing tickets and learning patterns...")
    learning.analyze_and_update_patterns()

    # Show learning stats
    stats = learning.get_learning_stats()
    print(f"\nLearning Statistics:")
    print(f"  Total patterns learned: {stats['total_patterns']}")
    print(f"  Pattern types: {stats['pattern_types']}")
    print(f"  Total feedback: {stats['total_feedback']}")

    # Test getting learned keywords
    print("\nLearned keywords for 'technical_support':")
    keywords = learning.get_learned_keywords_for_intent("technical_support")
    print(f"  {', '.join(keywords[:10])}")
