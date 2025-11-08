# SQLite Database - Quick Start Guide

## 🚀 TL;DR - Your Database is Already Working!

Your app is **already connected** to SQLite. The database file is `query_router.db` in your project folder.

---

## 📁 Where Is My Database?

```
/Users/pranavks/hackathon/query_router.db
```

---

## 🎯 Quick Commands

### View Your Database
```bash
# Option 1: Interactive menu (easiest)
python db_helper.py

# Option 2: Quick view
python view_database.py

# Option 3: See just the schema
python view_database.py schema

# Option 4: Direct SQLite CLI
sqlite3 query_router.db
```

### Backup Your Database
```bash
cp query_router.db backup_$(date +%Y%m%d).db
```

### Clear All Data (Fresh Start)
```bash
rm query_router.db
# Next time you run the app, it will create a fresh database
```

---

## 📊 Current Database Status

Your database currently has:
- **14 tickets** stored
- **5 teams** configured
- **37 routing log entries**

### Teams:
1. KYC Team (5 tickets)
2. Tech Support (5 tickets)
3. Finance Team (1 ticket)
4. Compliance Team (2 tickets)
5. Sales Team (0 tickets)

### All tickets are currently: **open**

---

## 🔧 How It Works

### The Connection Chain:
```
start.py → app.py → router_agent.py → database.py → query_router.db
```

### When You Submit a Query:
1. Customer sends query through web UI
2. App classifies the query (intent & urgency)
3. Creates a ticket in the database
4. Assigns to appropriate team
5. Logs the routing event
6. Returns response to customer

**All database operations happen automatically!**

---

## 📖 Files You Created

### 1. `view_database.py` - View Database Contents
```bash
python view_database.py           # View all data
python view_database.py schema    # View table structure
python view_database.py query "SELECT * FROM tickets WHERE urgency='critical'"
```

### 2. `db_helper.py` - Interactive Database Tool
```bash
python db_helper.py
```
Then choose from menu:
- View tickets by status/team
- Search tickets
- Export to CSV
- Backup database
- Run custom SQL queries
- And more!

### 3. `SQLITE_CONNECTION_GUIDE.md` - Complete Documentation
Full guide with all database operations and examples.

### 4. `DATABASE_FLOW.md` - Visual Diagrams
Detailed flow charts showing how everything connects.

---

## 💡 Common Tasks

### 1. View All Open Tickets
```bash
python db_helper.py
# Choose option 2, then type "open"
```

Or in Python:
```python
from database import Database
db = Database()
tickets = db.get_all_tickets(status="open")
for ticket in tickets:
    print(ticket['ticket_id'], ticket['subject'])
```

### 2. Check Ticket Count
```bash
sqlite3 query_router.db "SELECT COUNT(*) FROM tickets"
```

### 3. Export Tickets to CSV
```bash
python db_helper.py
# Choose option 9
```

Or use the API:
```bash
curl http://localhost:8000/api/export_tickets
```

### 4. View Specific Ticket Details
```bash
python db_helper.py
# Choose option 4
# Enter ticket ID: EML-H-20251108121714-6B45C631
```

### 5. See Statistics
```bash
python db_helper.py
# Choose option 8
```

Or via API:
```bash
curl http://localhost:8000/api/stats
```

---

## 🔍 Sample SQL Queries

```sql
-- View all critical tickets
SELECT * FROM tickets WHERE urgency = 'critical';

-- Count tickets by team
SELECT assigned_team, COUNT(*) as count 
FROM tickets 
GROUP BY assigned_team;

-- Recent tickets (last 24 hours)
SELECT * FROM tickets 
WHERE created_at >= datetime('now', '-1 day')
ORDER BY created_at DESC;

-- Find tickets by keyword
SELECT * FROM tickets 
WHERE message LIKE '%API%' OR subject LIKE '%API%';

-- Tickets needing attention
SELECT * FROM tickets 
WHERE status = 'open' AND urgency IN ('critical', 'high')
ORDER BY created_at;
```

---

## 🛠️ Troubleshooting

### "Database is locked"
**Cause:** Another process is writing to the database.
**Solution:** Wait a moment and try again, or close other connections.

### "No such table: tickets"
**Cause:** Database not initialized.
**Solution:** Just run the app once - it will create tables automatically.

### Can't find database file
**Cause:** Running commands from wrong directory.
**Solution:** 
```bash
cd /Users/pranavks/hackathon
python view_database.py
```

### Want to reset everything
**Solution:**
```bash
rm query_router.db
python start.py  # Will create fresh database
```

---

## 📚 Documentation Files

1. **QUICK_START_DATABASE.md** (this file) - Quick reference
2. **SQLITE_CONNECTION_GUIDE.md** - Complete step-by-step guide
3. **DATABASE_FLOW.md** - Visual flow diagrams
4. **view_database.py** - Database viewer script
5. **db_helper.py** - Interactive database tool

---

## 🎓 Learn More

### About SQLite
- Homepage: https://sqlite.org/
- Tutorial: https://www.sqlitetutorial.net/

### GUI Tools
- **DB Browser for SQLite**: https://sqlitebrowser.org/
  - Free, open-source
  - Visual table editor
  - SQL query builder

### Python sqlite3 Module
- Docs: https://docs.python.org/3/library/sqlite3.html

---

## ⚡ Quick Reference

| Task | Command |
|------|---------|
| View data | `python view_database.py` |
| Interactive tool | `python db_helper.py` |
| SQL CLI | `sqlite3 query_router.db` |
| Backup | `cp query_router.db backup.db` |
| Reset | `rm query_router.db` |
| Export tickets | API: `/api/export_tickets` |
| Get stats | API: `/api/stats` |

---

## ✅ Summary

Your SQLite database:
- ✅ Is already connected and working
- ✅ Stores all tickets automatically
- ✅ Tracks routing history
- ✅ Manages team data
- ✅ Located at: `/Users/pranavks/hackathon/query_router.db`

**You don't need to configure anything - it just works!**

---

Need help? Check the full guide: `SQLITE_CONNECTION_GUIDE.md`

