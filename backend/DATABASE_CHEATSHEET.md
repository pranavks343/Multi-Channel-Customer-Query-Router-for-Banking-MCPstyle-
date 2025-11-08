# SQLite Database Cheat Sheet

## 🎯 One-Liner Commands

```bash
# View database
python view_database.py

# Interactive menu
python db_helper.py

# Open SQLite CLI
sqlite3 query_router.db

# Backup database
cp query_router.db backup_$(date +%Y%m%d).db

# Count tickets
sqlite3 query_router.db "SELECT COUNT(*) FROM tickets"

# View schema
python view_database.py schema
```

---

## 📊 Quick SQL Queries

```sql
-- All tickets
SELECT * FROM tickets ORDER BY created_at DESC;

-- Open tickets only
SELECT * FROM tickets WHERE status = 'open';

-- Critical/High urgency
SELECT * FROM tickets WHERE urgency IN ('critical', 'high');

-- Tickets by team
SELECT assigned_team, COUNT(*) FROM tickets GROUP BY assigned_team;

-- Recent tickets (today)
SELECT * FROM tickets WHERE date(created_at) = date('now');

-- Search by keyword
SELECT * FROM tickets WHERE message LIKE '%API%';

-- Tickets with responses
SELECT * FROM tickets WHERE response IS NOT NULL;

-- Routing history for ticket
SELECT * FROM routing_log WHERE ticket_id = 'YOUR-TICKET-ID';
```

---

## 🐍 Python Quick Code

```python
# Basic connection
from database import Database
db = Database()

# Get all tickets
tickets = db.get_all_tickets()

# Get open tickets only
open_tickets = db.get_all_tickets(status="open")

# Get specific ticket
ticket = db.get_ticket("EML-H-20251108-ABC123")

# Get all teams
teams = db.get_teams()

# Get routing events for ticket
events = db.get_routing_events("EML-H-20251108-ABC123")

# Update ticket status
db.update_ticket("TICKET-ID", {"status": "closed"})

# Create new ticket (normally done by RouterAgent)
db.create_ticket({
    "ticket_id": "TEST-001",
    "channel": "email",
    "message": "Test message",
    "intent": "technical_support",
    "urgency": "medium",
    "assigned_team": "Tech Support",
    "status": "open"
})
```

---

## 🔧 SQLite CLI Commands

```bash
# Open database
sqlite3 query_router.db

# Inside SQLite CLI:
.tables                    # List all tables
.schema tickets            # Show table structure
.mode column              # Format output as columns
.headers on               # Show column headers
.quit                     # Exit

# Execute query
SELECT * FROM tickets LIMIT 5;
```

---

## 📍 File Locations

```
Database File:    /Users/pranavks/hackathon/query_router.db
Connection Code:  /Users/pranavks/hackathon/database.py
Router Agent:     /Users/pranavks/hackathon/router_agent.py
Flask App:        /Users/pranavks/hackathon/app.py
```

---

## 🔗 Connection Code Locations

```python
# database.py (Line 12-18)
class Database:
    def __init__(self, db_path: str = "query_router.db"):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        return conn

# router_agent.py (Line 17)
self.db = Database()

# app.py (Line 21)
router = RouterAgent()
```

---

## 📋 Table Columns Quick Reference

### tickets
- ticket_id, channel, sender, subject, message
- intent, urgency, assigned_team, status
- response, created_at, updated_at, metadata

### routing_log
- ticket_id, event_type, event_data, timestamp

### teams
- team_name, team_email, description, active

---

## 🚀 API Endpoints (Database Related)

```bash
# Get all tickets
curl http://localhost:8000/api/tickets

# Get open tickets only
curl http://localhost:8000/api/tickets?status=open

# Get specific ticket
curl http://localhost:8000/api/tickets/TICKET-ID

# Get statistics
curl http://localhost:8000/api/stats

# Export tickets
curl http://localhost:8000/api/export_tickets > tickets.csv

# Get teams
curl http://localhost:8000/api/teams
```

---

## 🛠️ Common Tasks

### Export Data
```bash
# Via Python script
python db_helper.py  # Choose option 9

# Via API
curl http://localhost:8000/api/export_tickets -o tickets.csv

# Via SQLite
sqlite3 query_router.db -header -csv "SELECT * FROM tickets" > tickets.csv
```

### Backup
```bash
# Simple copy
cp query_router.db backup.db

# With timestamp
cp query_router.db backup_$(date +%Y%m%d_%H%M%S).db

# SQLite backup command
sqlite3 query_router.db ".backup backup.db"
```

### Reset Database
```bash
# Delete database file
rm query_router.db

# Clear all data but keep structure
sqlite3 query_router.db "DELETE FROM tickets"
sqlite3 query_router.db "DELETE FROM routing_log"
```

---

## 📈 Statistics Queries

```sql
-- Total tickets
SELECT COUNT(*) FROM tickets;

-- By status
SELECT status, COUNT(*) FROM tickets GROUP BY status;

-- By urgency
SELECT urgency, COUNT(*) FROM tickets GROUP BY urgency;

-- By team
SELECT assigned_team, COUNT(*) FROM tickets GROUP BY assigned_team;

-- By channel
SELECT channel, COUNT(*) FROM tickets GROUP BY channel;

-- Today's tickets
SELECT COUNT(*) FROM tickets WHERE date(created_at) = date('now');

-- This week's tickets
SELECT COUNT(*) FROM tickets WHERE created_at >= date('now', '-7 days');
```

---

## 🔍 Advanced Queries

```sql
-- Tickets with no response
SELECT * FROM tickets WHERE response IS NULL;

-- Oldest open tickets
SELECT * FROM tickets 
WHERE status = 'open' 
ORDER BY created_at ASC 
LIMIT 10;

-- Most active teams
SELECT assigned_team, COUNT(*) as count 
FROM tickets 
GROUP BY assigned_team 
ORDER BY count DESC;

-- Critical tickets still open
SELECT * FROM tickets 
WHERE urgency = 'critical' AND status = 'open'
ORDER BY created_at;

-- Tickets by hour of day
SELECT strftime('%H', created_at) as hour, COUNT(*) 
FROM tickets 
GROUP BY hour 
ORDER BY hour;

-- Average response time (if tracking response times)
SELECT AVG(julianday(updated_at) - julianday(created_at)) * 24 as avg_hours
FROM tickets 
WHERE response IS NOT NULL;
```

---

## 💡 Tips & Tricks

### 1. Pretty Print in SQLite CLI
```sql
.mode column
.headers on
.width 15 30 10 10
SELECT ticket_id, subject, urgency, status FROM tickets LIMIT 5;
```

### 2. Count Multiple Things at Once
```sql
SELECT 
    COUNT(*) as total,
    SUM(CASE WHEN status = 'open' THEN 1 ELSE 0 END) as open,
    SUM(CASE WHEN urgency = 'critical' THEN 1 ELSE 0 END) as critical
FROM tickets;
```

### 3. Find Tickets Without Responses
```python
from database import Database
db = Database()
conn = db.get_connection()
cursor = conn.cursor()
cursor.execute("SELECT * FROM tickets WHERE response IS NULL")
no_response = cursor.fetchall()
print(f"Tickets without responses: {len(no_response)}")
conn.close()
```

### 4. Quick Data Validation
```sql
-- Check for tickets without teams
SELECT * FROM tickets WHERE assigned_team IS NULL;

-- Check for orphaned routing logs
SELECT r.* FROM routing_log r 
LEFT JOIN tickets t ON r.ticket_id = t.ticket_id 
WHERE t.ticket_id IS NULL;
```

---

## 🎓 Documentation Files

- **QUICK_START_DATABASE.md** - Quick reference
- **SQLITE_CONNECTION_GUIDE.md** - Complete guide
- **DATABASE_FLOW.md** - Visual diagrams
- **DATABASE_CHEATSHEET.md** - This file!

---

## ⚡ Emergency Commands

```bash
# Check if database is corrupted
sqlite3 query_router.db "PRAGMA integrity_check"

# Rebuild database (fixes corruption)
sqlite3 query_router.db ".dump" | sqlite3 new_database.db

# Check database size
ls -lh query_router.db

# Vacuum database (optimize space)
sqlite3 query_router.db "VACUUM"
```

---

**Remember: Your database is already working! This is just for reference.** ✨

