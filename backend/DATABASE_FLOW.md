# Database Connection Flow Diagram

## Visual Flow Chart

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER STARTS APP                           │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  start.py    │
                    │  (Line 91)   │
                    └──────┬───────┘
                           │ imports & runs
                           ▼
                    ┌──────────────┐
                    │   app.py     │
                    │  (Line 21)   │
                    └──────┬───────┘
                           │ router = RouterAgent()
                           ▼
                    ┌──────────────────┐
                    │ router_agent.py  │
                    │   (Line 17)      │
                    │                  │
                    │ self.db = DB()   │
                    └──────┬───────────┘
                           │
                           ▼
                    ┌─────────────────────┐
                    │   database.py       │
                    │   (Line 12-14)      │
                    │                     │
                    │ __init__():         │
                    │  - Set db_path      │
                    │  - init_database()  │
                    └──────┬──────────────┘
                           │
                           ▼
                    ┌─────────────────────┐
                    │ sqlite3.connect()   │
                    │   (Line 18)         │
                    └──────┬──────────────┘
                           │
                           ▼
              ┌────────────────────────────┐
              │   query_router.db          │
              │   (SQLite Database File)   │
              │                            │
              │  Tables:                   │
              │   • tickets                │
              │   • routing_log            │
              │   • teams                  │
              └────────────────────────────┘
```

## Detailed Connection Steps

### Step 1: Application Starts
```python
# start.py (Line 91)
from app import app
app.run(debug=True, host='0.0.0.0', port=port, threaded=True)
```

### Step 2: Flask App Initializes
```python
# app.py (Line 21)
router = RouterAgent()
```

### Step 3: Router Agent Creates Database Connection
```python
# router_agent.py (Line 15-20)
class RouterAgent:
    def __init__(self):
        self.db = Database()                    # ← Database connection created here
        self.classifier = IntentClassifier()
        self.rag = RAGSystem()
        self.ticket_manager = TicketManager(self.db)
```

### Step 4: Database Class Connects to SQLite
```python
# database.py (Line 11-20)
class Database:
    def __init__(self, db_path: str = "query_router.db"):
        self.db_path = db_path                  # ← Database file path
        self.init_database()                     # ← Create tables if needed
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)    # ← Actual SQLite connection
        conn.row_factory = sqlite3.Row
        return conn
```

### Step 5: Tables Are Created (If Needed)
```python
# database.py (Line 22-71)
def init_database(self):
    conn = self.get_connection()
    cursor = conn.cursor()
    
    # Create tickets table
    cursor.execute("CREATE TABLE IF NOT EXISTS tickets (...)")
    
    # Create routing_log table
    cursor.execute("CREATE TABLE IF NOT EXISTS routing_log (...)")
    
    # Create teams table
    cursor.execute("CREATE TABLE IF NOT EXISTS teams (...)")
    
    conn.commit()
    conn.close()
```

## Data Flow: Customer Query to Database

```
   Customer Submits Query
            │
            ▼
   ┌─────────────────────┐
   │  Web UI / API       │
   │  (POST request)     │
   └──────────┬──────────┘
              │
              ▼
   ┌─────────────────────┐
   │  app.py             │
   │  /api/submit_query  │
   └──────────┬──────────┘
              │ router.process_query()
              ▼
   ┌─────────────────────────────┐
   │  router_agent.py            │
   │  process_query()            │
   │                             │
   │  1. Classify intent         │
   │  2. Generate response       │
   │  3. Create ticket           │
   └──────────┬──────────────────┘
              │ ticket_manager.create_ticket()
              ▼
   ┌─────────────────────────────┐
   │  ticket_manager.py          │
   │  create_ticket()            │
   └──────────┬──────────────────┘
              │ db.create_ticket()
              ▼
   ┌─────────────────────────────┐
   │  database.py                │
   │  create_ticket()            │
   │                             │
   │  INSERT INTO tickets...     │
   └──────────┬──────────────────┘
              │
              ▼
   ┌─────────────────────────────┐
   │  query_router.db            │
   │  (SQLite file)              │
   │                             │
   │  ✓ Ticket saved             │
   └─────────────────────────────┘
```

## Key Connection Points

### 1. Database Path Configuration
```
Location: database.py, Line 12
Default: "query_router.db"
Full path: /Users/pranavks/hackathon/query_router.db
```

### 2. Connection Creation
```
Location: database.py, Line 18
Method: sqlite3.connect(self.db_path)
Type: SQLite3 connection object
```

### 3. Row Factory
```
Location: database.py, Line 19
Setting: conn.row_factory = sqlite3.Row
Purpose: Returns rows as dict-like objects instead of tuples
```

## How Different Components Use the Database

```
┌─────────────────────────────────────────────────────────────────┐
│                        Database (db)                             │
│                    query_router.db                               │
└─────┬──────────────────┬─────────────────┬──────────────────────┘
      │                  │                 │
      │                  │                 │
      ▼                  ▼                 ▼
┌─────────────┐   ┌──────────────┐  ┌──────────────┐
│RouterAgent  │   │TicketManager │  │   app.py     │
│             │   │              │  │              │
│ self.db     │   │ self.db      │  │ router.db    │
│             │   │              │  │              │
│ • get teams │   │ • create     │  │ • get stats  │
│ • log events│   │ • get ticket │  │ • get all    │
│             │   │ • update     │  │ • export     │
└─────────────┘   └──────────────┘  └──────────────┘
```

## Database Operations Map

### Reading Data
```python
# Get all tickets
router.ticket_manager.get_all_tickets()
  └─> db.get_all_tickets()
    └─> SELECT * FROM tickets

# Get specific ticket
router.get_ticket_details(ticket_id)
  └─> ticket_manager.get_ticket(ticket_id)
    └─> db.get_ticket(ticket_id)
      └─> SELECT * FROM tickets WHERE ticket_id = ?

# Get teams
router.db.get_teams()
  └─> SELECT * FROM teams WHERE active = 1
```

### Writing Data
```python
# Create ticket
router.process_query(...)
  └─> ticket_manager.create_ticket(...)
    └─> db.create_ticket(ticket_data)
      └─> INSERT INTO tickets VALUES (...)

# Log routing event
router.db.log_routing_event(ticket_id, event_type, data)
  └─> INSERT INTO routing_log VALUES (...)

# Update ticket
ticket_manager.update_ticket_status(ticket_id, status)
  └─> db.update_ticket(ticket_id, {"status": status})
    └─> UPDATE tickets SET status = ? WHERE ticket_id = ?
```

## Connection Lifecycle

```
1. Application Start
   └─> RouterAgent.__init__()
       └─> Database.__init__()
           └─> init_database()
               └─> get_connection()  [Creates connection #1]
                   └─> CREATE TABLES IF NOT EXISTS
                   └─> conn.close()  [Closes connection #1]

2. Each API Request
   └─> process_query() or get_tickets() etc.
       └─> database operation (create_ticket, get_all_tickets, etc.)
           └─> get_connection()  [Creates connection #2]
               └─> Execute SQL
               └─> conn.close()  [Closes connection #2]

3. Application Continues Running
   └─> Multiple requests
       └─> Each request opens and closes its own connection
           └─> SQLite handles file locking automatically
```

## Important Notes

### ✅ Connection Pattern: Create → Use → Close
Each database operation:
1. Opens a new connection
2. Executes the SQL
3. Immediately closes the connection

### ✅ Thread Safety
- SQLite connections are NOT shared between threads
- Each operation creates its own connection
- Flask's `threaded=True` mode works safely

### ✅ Auto-Initialization
- Database file is created automatically if it doesn't exist
- Tables are created automatically on first run
- Default teams are inserted automatically

### ⚠️  No Connection Pool
- Each operation opens/closes connection
- For high-traffic apps, consider connection pooling
- Current design is fine for moderate usage

### 🔒 File Locking
- SQLite uses file-level locking
- Only one writer at a time
- Multiple readers allowed
- "Database is locked" error means write conflict

## Summary

**Your database connection flow:**

1. **start.py** launches the app
2. **app.py** creates RouterAgent
3. **router_agent.py** creates Database instance
4. **database.py** connects to SQLite file `query_router.db`
5. Tables are created if they don't exist
6. App is ready to handle requests!

**Each request:**
- Opens connection
- Executes SQL
- Closes connection
- Returns data to user

**It's all automatic!** ✨

