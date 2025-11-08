# Dynamic Learning System

The system now dynamically updates itself based on user inputs from any channel (email, chat, form). It learns patterns from tickets and improves routing accuracy over time.

## How It Works

### 1. **Automatic Learning from Each Query**
- When a ticket is created, the system extracts keywords from the message
- It learns associations between:
  - **Intent categories** and **keywords** (what words indicate which intent)
  - **Intent categories** and **teams** (which team handles which intent successfully)

### 2. **Learning from Reassignments**
- When a ticket is reassigned to a different team, the system treats this as feedback
- It learns that the original routing was incorrect
- It strengthens the association between the correct team and the intent

### 3. **Pattern Storage**
- Learned patterns are stored in the `learning_patterns` table
- Each pattern includes:
  - Pattern type (intent_keyword, team_intent)
  - Confidence score (based on frequency)
  - Usage count (how many times it's been seen)

### 4. **Dynamic Updates**
- The Intent Classifier automatically loads learned keywords
- Team mappings are updated based on successful routing patterns
- Updates happen:
  - **Immediately** after each ticket (learns from the ticket)
  - **Periodically** every 10 tickets (refreshes classifier with all learned patterns)

## Database Tables

### `learning_patterns`
Stores learned patterns:
- `pattern_type`: Type of pattern (intent_keyword, team_intent)
- `pattern_key`: The intent or team name
- `pattern_value`: The keyword or associated value
- `confidence`: Confidence score (0.0 to 1.0)
- `usage_count`: How many times this pattern was observed

### `learning_feedback`
Tracks routing corrections:
- Stores reassignment history
- Records original vs corrected routing
- Used to improve future routing decisions

## API Endpoints

### GET `/api/learning/stats`
Get learning system statistics:
```json
{
  "success": true,
  "stats": {
    "total_patterns": 150,
    "pattern_types": {
      "intent_keyword": 120,
      "team_intent": 30
    },
    "total_feedback": 5,
    "reassignments": 5
  }
}
```

### POST `/api/learning/analyze`
Manually trigger learning analysis on all tickets:
```json
{
  "success": true,
  "message": "Learning analysis completed and patterns updated"
}
```

## Integration Points

### Router Agent
- Automatically learns from each processed query
- Refreshes classifier patterns every 10 tickets

### Intent Classifier
- Loads learned keywords on initialization
- Updates team mappings based on learned patterns
- Can be manually refreshed with `update_from_learning()`

### Ticket Manager
- Learns from reassignments automatically
- Captures feedback when tickets are moved between teams

## Example Learning Flow

1. **User submits query**: "API integration keeps failing with error code 403"
2. **System routes** to Tech Support (based on initial rules)
3. **System learns**:
   - Keywords: "api", "integration", "failing", "error", "403" → technical_support
   - Team mapping: technical_support → Tech Support
4. **If reassigned** to Compliance Team:
   - System learns this was incorrect routing
   - Strengthens alternative patterns
5. **Future queries** with similar keywords will benefit from learned patterns

## Benefits

- **Improves over time**: Gets better at routing as it sees more tickets
- **Adapts to your business**: Learns your specific terminology and patterns
- **Self-correcting**: Learns from mistakes (reassignments)
- **Channel-agnostic**: Works with email, chat, and form submissions
- **No manual configuration**: Automatically adapts without intervention

## Manual Learning Analysis

You can trigger a full analysis of all tickets to update patterns:

```python
from router_agent import RouterAgent

router = RouterAgent()
router.learning_system.analyze_and_update_patterns()
router.classifier.update_from_learning()
```

Or via API:
```bash
curl -X POST http://localhost:8000/api/learning/analyze
```

## Monitoring

Check learning progress:
```bash
curl http://localhost:8000/api/learning/stats
```

View learned patterns in database:
```sql
SELECT * FROM learning_patterns ORDER BY usage_count DESC LIMIT 20;
SELECT * FROM learning_feedback ORDER BY timestamp DESC LIMIT 10;
```

