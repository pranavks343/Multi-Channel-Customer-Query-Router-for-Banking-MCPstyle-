# How to Open Your Database in DB Browser for SQLite

## 📍 Your Database File Location
```
/Users/pranavks/hackathon/query_router.db
```

---

## 🚀 Step-by-Step Instructions

### Step 1: Open DB Browser for SQLite

**Option A: If Already Installed**
- Open **DB Browser for SQLite** from Applications or Spotlight

**Option B: If Not Installed**
1. Download from: https://sqlitebrowser.org/dl/
2. Install the application
3. Open **DB Browser for SQLite**

---

### Step 2: Open Your Database File

1. Click **"Open Database"** button (top left) or press `Cmd+O`
2. Navigate to: `/Users/pranavks/hackathon/`
3. Select file: **`query_router.db`**
4. Click **"Open"**

**OR** drag and drop `query_router.db` onto the DB Browser window

---

### Step 3: View Your Tables

Once opened, you should see **5 tables** in the left sidebar:

1. ✅ **tickets** - Customer queries/tickets
2. ✅ **routing_log** - Routing event history
3. ✅ **teams** - Team information
4. ✅ **learning_patterns** - Learning data
5. ✅ **learning_feedback** - Feedback data

---

## 📊 What You Should See

### In the Left Sidebar (Database Structure):
```
📁 query_router.db
  ├── 📋 tickets
  ├── 📋 routing_log
  ├── 📋 teams
  ├── 📋 learning_patterns
  └── 📋 learning_feedback
```

### When You Click on Each Table:

#### 1. **tickets** Table
**Columns:**
- `id` (INTEGER, Primary Key)
- `ticket_id` (TEXT, Unique)
- `channel` (TEXT)
- `sender` (TEXT)
- `subject` (TEXT)
- `message` (TEXT)
- `intent` (TEXT)
- `urgency` (TEXT)
- `assigned_team` (TEXT)
- `status` (TEXT, Default: 'open')
- `response` (TEXT)
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)
- `metadata` (TEXT)

**Current Data:** ~14 tickets

#### 2. **routing_log** Table
**Columns:**
- `id` (INTEGER, Primary Key)
- `ticket_id` (TEXT)
- `event_type` (TEXT)
- `event_data` (TEXT)
- `timestamp` (TIMESTAMP)

**Current Data:** ~37 log entries

#### 3. **teams** Table
**Columns:**
- `id` (INTEGER, Primary Key)
- `team_name` (TEXT, Unique)
- `team_email` (TEXT)
- `description` (TEXT)
- `active` (BOOLEAN, Default: 1)

**Current Data:** 5 teams

#### 4. **learning_patterns** Table
**Columns:**
- `id` (INTEGER, Primary Key)
- `pattern_type` (TEXT)
- `pattern_key` (TEXT)
- `pattern_value` (TEXT)
- `confidence` (REAL)
- `usage_count` (INTEGER)
- `last_used` (TIMESTAMP)
- `created_at` (TIMESTAMP)

#### 5. **learning_feedback** Table
**Columns:**
- `id` (INTEGER, Primary Key)
- `ticket_id` (TEXT)
- `original_intent` (TEXT)
- `corrected_intent` (TEXT)
- `original_team` (TEXT)
- `corrected_team` (TEXT)
- (and more columns...)

---

## 🔍 How to Browse Your Data

### View Table Data:
1. Click on a table name (e.g., **tickets**) in the left sidebar
2. Click the **"Browse Data"** tab at the top
3. You'll see all rows in that table

### View Table Structure:
1. Click on a table name
2. Click the **"Database Structure"** tab
3. You'll see columns, data types, and constraints

### Run SQL Queries:
1. Click the **"Execute SQL"** tab
2. Type your SQL query, for example:
```sql
SELECT * FROM tickets WHERE urgency = 'critical';
```
3. Click **"Execute SQL"** (or press `Cmd+Enter`)

---

## 🎯 Quick Actions in DB Browser

### View All Tickets:
1. Click **tickets** table
2. Click **"Browse Data"** tab
3. See all 14 tickets!

### View Teams:
1. Click **teams** table
2. Click **"Browse Data"** tab
3. See all 5 teams!

### Count Tickets by Status:
1. Click **"Execute SQL"** tab
2. Run:
```sql
SELECT status, COUNT(*) as count 
FROM tickets 
GROUP BY status;
```

### View Recent Tickets:
1. Click **"Execute SQL"** tab
2. Run:
```sql
SELECT ticket_id, subject, urgency, assigned_team, created_at
FROM tickets
ORDER BY created_at DESC
LIMIT 10;
```

---

## 🛠️ Troubleshooting

### Problem: "File not found" or can't see the database
**Solution:**
- Make sure you're navigating to: `/Users/pranavks/hackathon/`
- The file is named exactly: `query_router.db`
- Check if file exists: `ls -lh /Users/pranavks/hackathon/query_router.db`

### Problem: Database appears empty or locked
**Solution:**
- Make sure your Flask app is not running (it locks the database)
- Close any other programs accessing the database
- Try opening it again

### Problem: Can't see tables
**Solution:**
- Click the **"Database Structure"** tab
- Expand the database tree in the left sidebar
- Tables should be listed under the database name

### Problem: DB Browser not installed
**Solution:**
1. Visit: https://sqlitebrowser.org/dl/
2. Download for macOS
3. Install and open
4. Follow Step 2 above

---

## 📸 What It Should Look Like

When you open the database, you should see:

**Left Sidebar:**
```
📁 query_router.db
  📋 tickets (14 rows)
  📋 routing_log (37 rows)
  📋 teams (5 rows)
  📋 learning_patterns
  📋 learning_feedback
```

**Main Window (Browse Data tab):**
- A table view with all columns and rows
- You can sort by clicking column headers
- You can filter using the search box

---

## ✅ Quick Verification Checklist

After opening in DB Browser, verify:

- [ ] Database file opens without errors
- [ ] Can see 5 tables in left sidebar
- [ ] **tickets** table shows ~14 rows
- [ ] **teams** table shows 5 rows
- [ ] **routing_log** table shows ~37 rows
- [ ] Can browse data by clicking tables
- [ ] Can run SQL queries in "Execute SQL" tab

---

## 🎓 Pro Tips

1. **Export Data:** Right-click table → Export → CSV
2. **Search:** Use the filter box in Browse Data tab
3. **Sort:** Click column headers to sort
4. **Edit:** Click "Edit" button to modify data (be careful!)
5. **Backup:** File → Export → Database to SQL file

---

## 🚀 Quick Command to Open (if DB Browser is installed)

You can also open it from terminal:
```bash
open -a "DB Browser for SQLite" /Users/pranavks/hackathon/query_router.db
```

---

**That's it! You should now see all 5 tables in DB Browser for SQLite!** ✨

