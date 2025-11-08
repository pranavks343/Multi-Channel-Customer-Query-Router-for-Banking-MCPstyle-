# SQLite Database Connection - Step-by-Step Guide

## Overview
Your application uses SQLite for data persistence. The database file is `query_router.db` and stores tickets, routing logs, and team information.

---

## Step 1: Understanding Your Database Setup

### File Structure
```
/Users/pranavks/hackathon/
├── query_router.db          # ← Your SQLite database file
├── database.py              # ← Database connection class
├── router_agent.py          # ← Uses the database
├── app.py                   # ← Flask app
└── start.py                 # ← Entry point
```

### How It Works
1. **database.py** contains the `Database` class
2. **router_agent.py** creates a `Database()` instance
3. **app.py** uses the router agent, which uses the database
4. **start.py** launches the Flask app

---

## Step 2: Database Connection Code

### In `database.py` (Lines 11-20)
```python
class Database:
    def __init__(self, db_path: str = "query_router.db"):
        self.db_path = db_path              # Database file path
        self.init_database()                 # Creates tables if needed
    
    def get_connection(self):
        """Get a database connection."""
        conn = sqlite3.connect(self.db_path)  # Connect to SQLite
        conn.row_factory = sqlite3.Row        # Return rows as dicts
        return conn
```

### In `router_agent.py` (Line 17)
```python
self.db = Database()  # Creates database connection
```

### In `app.py` (Line 21)
```python
router = RouterAgent()  # Initializes everything including database
```

---

## Step 3: Database Tables

Your database has **3 tables**:

### 1. **tickets** Table
Stores all customer queries/support tickets.

| Column         | Type      | Description                          |
|----------------|-----------|--------------------------------------|
| id             | INTEGER   | Primary key (auto-increment)         |
| ticket_id      | TEXT      | Unique ticket identifier             |
| channel        | TEXT      | Source (email, chat, form)           |
| sender         | TEXT      | Customer email/ID                    |
| subject        | TEXT      | Query subject line                   |
| message        | TEXT      | Customer message                     |
| intent         | TEXT      | Classified intent                    |
| urgency        | TEXT      | Priority level                       |
| assigned_team  | TEXT      | Team handling the ticket             |
| status         | TEXT      | open/closed/pending                  |
| response       | TEXT      | Auto-generated response              |
| created_at     | TIMESTAMP | When ticket was created              |
| updated_at     | TIMESTAMP | Last update time                     |
| metadata       | TEXT      | Additional JSON data                 |

### 2. **routing_log** Table
Tracks routing events and history.

| Column      | Type      | Description                     |
|-------------|-----------|---------------------------------|
| id          | INTEGER   | Primary key                     |
| ticket_id   | TEXT      | Related ticket                  |
| event_type  | TEXT      | Type of event                   |
| event_data  | TEXT      | Event details (JSON)            |
| timestamp   | TIMESTAMP | When event occurred             |

### 3. **teams** Table
Stores team information.

| Column      | Type    | Description                        |
|-------------|---------|------------------------------------|
| id          | INTEGER | Primary key                        |
| team_name   | TEXT    | Team name                          |
| team_email  | TEXT    | Team contact email                 |
| description | TEXT    | What the team handles              |
| active      | BOOLEAN | Whether team is active             |

---

## Step 4: View Your Database

### Option A: Use the Provided Script
```bash
# View all data
python view_database.py

# View schema only
python view_database.py schema

# Run custom SQL query
python view_database.py query "SELECT * FROM tickets WHERE urgency='critical'"
```

### Option B: Use SQLite Command Line
```bash
# Open database
sqlite3 query_router.db

# View tables
.tables

# View schema
.schema tickets

# Query data
SELECT * FROM tickets LIMIT 5;

# Count tickets by team
SELECT assigned_team, COUNT(*) FROM tickets GROUP BY assigned_team;

# Exit
.exit
```

### Option C: Use Python Directly
```python
import sqlite3

# Connect
conn = sqlite3.connect('query_router.db')
cursor = conn.cursor()

# Query
cursor.execute("SELECT * FROM tickets")
tickets = cursor.fetchall()

# Print results
for ticket in tickets:
    print(ticket)

# Close
conn.close()
```

### Option D: Use DB Browser for SQLite (GUI)
1. Download from: https://sqlitebrowser.org/
2. Open `query_router.db`
3. Browse tables visually

---

## Step 5: Common Database Operations

### Create a Ticket (Automated by the app)
```python
from database import Database

db = Database()
ticket_data = {
    "ticket_id": "EML-H-20251108-ABC123",
    "channel": "email",
    "sender": "customer@example.com",
    "subject": "Need help",
    "message": "I have a problem...",
    "intent": "technical_support",
    "urgency": "high",
    "assigned_team": "Tech Support",
    "status": "open",
    "response": "Thank you for contacting us...",
    "metadata": {}
}
db.create_ticket(ticket_data)
```

### Get All Tickets
```python
from database import Database

db = Database()
tickets = db.get_all_tickets()

# Filter by status
open_tickets = db.get_all_tickets(status="open")
```

### Get Specific Ticket
```python
from database import Database

db = Database()
ticket = db.get_ticket("EML-H-20251108-ABC123")
print(ticket)
```

### Update Ticket Status
```python
from database import Database

db = Database()
db.update_ticket("EML-H-20251108-ABC123", {
    "status": "closed"
})
```

### Log Routing Event
```python
from database import Database

db = Database()
db.log_routing_event(
    ticket_id="EML-H-20251108-ABC123",
    event_type="ticket_escalated",
    event_data={"reason": "High urgency", "team": "Tech Lead"}
)
```

---

## Step 6: Changing Database Location

If you want to use a different database file:

### Method 1: Modify database.py
```python
# In database.py, line 12
def __init__(self, db_path: str = "/path/to/your/database.db"):
```

### Method 2: Modify router_agent.py
```python
# In router_agent.py, line 17
self.db = Database(db_path="/path/to/your/database.db")
```

### Method 3: Use Environment Variable
```python
# In database.py
import os

def __init__(self, db_path: str = None):
    if db_path is None:
        db_path = os.getenv('DATABASE_PATH', 'query_router.db')
    self.db_path = db_path
    self.init_database()
```

Then in `.env`:
```
DATABASE_PATH=/Users/pranavks/hackathon/my_custom.db
```

---

## Step 7: Current Database Status

Your current database has:
- ✅ **14 tickets** created
- ✅ **5 teams** configured
- ✅ **37 routing log entries**

### Tickets by Team:
- Compliance Team: 2 tickets
- Finance Team: 1 ticket
- KYC Team: 5 tickets
- Tech Support: 5 tickets
- Triage Team: 1 ticket

### All tickets are currently: **open**

---

## Step 8: Backup Your Database

### Option 1: Simple Copy
```bash
cp query_router.db query_router_backup_$(date +%Y%m%d).db
```

### Option 2: SQLite Backup Command
```bash
sqlite3 query_router.db ".backup query_router_backup.db"
```

### Option 3: Export to SQL
```bash
sqlite3 query_router.db .dump > backup.sql
```

### Option 4: Automated Backup Script
```python
import shutil
from datetime import datetime

# Backup with timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy('query_router.db', f'backup_query_router_{timestamp}.db')
print(f"Backup created: backup_query_router_{timestamp}.db")
```

---

## Step 9: Reset/Clear Database

### Option 1: Delete Specific Data
```bash
sqlite3 query_router.db "DELETE FROM tickets WHERE status='closed'"
```

### Option 2: Clear All Tickets
```bash
sqlite3 query_router.db "DELETE FROM tickets"
sqlite3 query_router.db "DELETE FROM routing_log"
```

### Option 3: Delete Database File
```bash
rm query_router.db
# Next time you run the app, it will create a fresh database
```

### Option 4: Use Python
```python
import sqlite3

conn = sqlite3.connect('query_router.db')
cursor = conn.cursor()

# Clear tickets
cursor.execute("DELETE FROM tickets")
cursor.execute("DELETE FROM routing_log")

conn.commit()
conn.close()
```

---

## Step 10: Testing Database Connection

Create a simple test script:

```python
# test_db_connection.py
from database import Database

print("Testing database connection...")

# Initialize database
db = Database()
print("✓ Database initialized")

# Get teams
teams = db.get_teams()
print(f"✓ Found {len(teams)} teams")

# Get tickets
tickets = db.get_all_tickets()
print(f"✓ Found {len(tickets)} tickets")

print("\nDatabase connection working perfectly! ✓")
```

Run it:
```bash
python test_db_connection.py
```

---

## Troubleshooting

### Problem: "database is locked"
**Solution:** Close any other connections to the database
```python
conn.close()  # Always close connections when done
```

### Problem: "no such table: tickets"
**Solution:** Database not initialized. Run:
```python
from database import Database
db = Database()  # This will create tables
```

### Problem: "unable to open database file"
**Solution:** Check file permissions
```bash
ls -la query_router.db
chmod 644 query_router.db  # If needed
```

### Problem: Want to see SQL queries being executed
**Solution:** Enable logging
```python
import sqlite3

sqlite3.enable_callback_tracebacks(True)
conn = sqlite3.connect('query_router.db')
conn.set_trace_callback(print)  # Print all SQL queries
```

---

## Quick Reference

### Connection Flow
```
start.py 
  → app.py 
    → router_agent.py 
      → database.py 
        → query_router.db (SQLite file)
```

### Key Files
- **database.py** - Database class and operations
- **query_router.db** - SQLite database file
- **view_database.py** - View database contents

### Common Commands
```bash
# View data
python view_database.py

# View schema
python view_database.py schema

# Backup database
cp query_router.db backup.db

# Open in SQLite CLI
sqlite3 query_router.db
```

---

## Summary

✅ **Your database is already connected and working!**

- Database file: `/Users/pranavks/hackathon/query_router.db`
- Connection: Automatic when app starts
- Tables: tickets, routing_log, teams
- Current data: 14 tickets, 5 teams, 37 log entries

You don't need to do anything special - it's all configured and running!

