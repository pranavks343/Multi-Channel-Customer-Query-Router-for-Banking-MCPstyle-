# Quick SQL Commands by Team

Quick reference SQL commands to execute in DB Browser for SQLite's **"Execute SQL"** tab.

---

## 👥 KYC Team

### View All KYC Tickets
```sql
SELECT ticket_id, sender, subject, urgency, status, created_at
FROM tickets
WHERE assigned_team = 'KYC Team'
ORDER BY created_at DESC;
```

### KYC Open Tickets Only
```sql
SELECT ticket_id, sender, subject, urgency, created_at
FROM tickets
WHERE assigned_team = 'KYC Team' AND status = 'open'
ORDER BY urgency DESC, created_at DESC;
```

### KYC Tickets by Intent
```sql
SELECT intent, COUNT(*) as count
FROM tickets
WHERE assigned_team = 'KYC Team'
GROUP BY intent
ORDER BY count DESC;
```

---

## 💻 Tech Support

### View All Tech Support Tickets
```sql
SELECT ticket_id, sender, subject, urgency, status, created_at
FROM tickets
WHERE assigned_team = 'Tech Support'
ORDER BY created_at DESC;
```

### Tech Support Critical/High Urgency
```sql
SELECT ticket_id, sender, subject, urgency, status, created_at
FROM tickets
WHERE assigned_team = 'Tech Support'
  AND urgency IN ('critical', 'high')
ORDER BY urgency DESC, created_at DESC;
```

### Tech Support Open Tickets
```sql
SELECT ticket_id, sender, subject, urgency, created_at
FROM tickets
WHERE assigned_team = 'Tech Support' AND status = 'open'
ORDER BY urgency DESC, created_at ASC;
```

---

## 💰 Finance Team

### View All Finance Tickets
```sql
SELECT ticket_id, sender, subject, urgency, status, created_at
FROM tickets
WHERE assigned_team = 'Finance Team'
ORDER BY created_at DESC;
```

### Finance Billing/Invoice Tickets
```sql
SELECT ticket_id, sender, subject, urgency, status, created_at
FROM tickets
WHERE assigned_team = 'Finance Team'
  AND (subject LIKE '%invoice%' OR subject LIKE '%billing%' OR message LIKE '%refund%')
ORDER BY created_at DESC;
```

### Finance Open Tickets
```sql
SELECT ticket_id, sender, subject, urgency, created_at
FROM tickets
WHERE assigned_team = 'Finance Team' AND status = 'open'
ORDER BY urgency DESC, created_at DESC;
```

---

## ⚖️ Compliance Team

### View All Compliance Tickets
```sql
SELECT ticket_id, sender, subject, urgency, status, created_at
FROM tickets
WHERE assigned_team = 'Compliance Team'
ORDER BY created_at DESC;
```

### Compliance Audit/Regulatory Requests
```sql
SELECT ticket_id, sender, subject, urgency, status, created_at
FROM tickets
WHERE assigned_team = 'Compliance Team'
  AND (subject LIKE '%audit%' OR subject LIKE '%GDPR%' OR subject LIKE '%compliance%')
ORDER BY created_at DESC;
```

### Compliance High Priority Open Tickets
```sql
SELECT ticket_id, sender, subject, urgency, created_at
FROM tickets
WHERE assigned_team = 'Compliance Team'
  AND status = 'open' AND urgency IN ('critical', 'high')
ORDER BY urgency DESC, created_at ASC;
```

---

## 📈 Sales Team

### View All Sales Tickets
```sql
SELECT ticket_id, sender, subject, urgency, status, created_at
FROM tickets
WHERE assigned_team = 'Sales Team'
ORDER BY created_at DESC;
```

### Sales Demo/Pricing Inquiries
```sql
SELECT ticket_id, sender, subject, urgency, status, created_at
FROM tickets
WHERE assigned_team = 'Sales Team'
  AND (subject LIKE '%demo%' OR subject LIKE '%pricing%' OR subject LIKE '%enterprise%')
ORDER BY created_at DESC;
```

### Sales Open Leads
```sql
SELECT ticket_id, sender, subject, urgency, created_at
FROM tickets
WHERE assigned_team = 'Sales Team' AND status = 'open'
ORDER BY created_at DESC;
```

---

## 🆘 General Support

### View All General Support Tickets
```sql
SELECT ticket_id, sender, subject, urgency, status, created_at
FROM tickets
WHERE assigned_team = 'General Support'
ORDER BY created_at DESC;
```

### General Support Documentation Questions
```sql
SELECT ticket_id, sender, subject, urgency, status, created_at
FROM tickets
WHERE assigned_team = 'General Support'
  AND (subject LIKE '%documentation%' OR message LIKE '%how to%')
ORDER BY created_at DESC;
```

---

## 🔄 Triage Team

### View All Triage Tickets
```sql
SELECT ticket_id, sender, subject, urgency, status, created_at
FROM tickets
WHERE assigned_team = 'Triage Team'
ORDER BY created_at DESC;
```

### Triage Pending Review
```sql
SELECT ticket_id, sender, subject, urgency, created_at
FROM tickets
WHERE assigned_team = 'Triage Team' AND status = 'open'
ORDER BY created_at ASC;
```

---

## 📊 Analytics Queries

### Count Tickets by Team
```sql
SELECT assigned_team, COUNT(*) as ticket_count
FROM tickets
GROUP BY assigned_team
ORDER BY ticket_count DESC;
```

### Open Tickets by Team
```sql
SELECT assigned_team, COUNT(*) as open_tickets
FROM tickets
WHERE status = 'open'
GROUP BY assigned_team
ORDER BY open_tickets DESC;
```

### Tickets by Urgency and Team
```sql
SELECT assigned_team, urgency, COUNT(*) as count
FROM tickets
GROUP BY assigned_team, urgency
ORDER BY assigned_team, urgency;
```

### Team Performance Summary
```sql
SELECT 
    assigned_team,
    COUNT(*) as total,
    COUNT(CASE WHEN status = 'open' THEN 1 END) as open,
    COUNT(CASE WHEN urgency = 'critical' THEN 1 END) as critical
FROM tickets
GROUP BY assigned_team
ORDER BY total DESC;
```

### Tickets Created Today by Team
```sql
SELECT assigned_team, COUNT(*) as today_count
FROM tickets
WHERE DATE(created_at) = DATE('now')
GROUP BY assigned_team
ORDER BY today_count DESC;
```

---

## 🔍 Search Queries

### Search by Sender Email
```sql
SELECT ticket_id, sender, subject, assigned_team, urgency, status
FROM tickets
WHERE sender LIKE '%@example.com%'
ORDER BY created_at DESC;
```

### Search by Keyword
```sql
SELECT ticket_id, sender, subject, assigned_team, urgency, status
FROM tickets
WHERE message LIKE '%API error%' OR subject LIKE '%API error%'
ORDER BY created_at DESC;
```

### Recent Updates
```sql
SELECT ticket_id, sender, subject, assigned_team, status, updated_at
FROM tickets
WHERE updated_at >= datetime('now', '-1 day')
ORDER BY updated_at DESC;
```

---

## 🎯 Most Common Queries

### All Tickets for Any Team
```sql
SELECT * FROM tickets WHERE assigned_team = 'Team Name' ORDER BY created_at DESC;
```

### Count Open Tickets
```sql
SELECT assigned_team, COUNT(*) FROM tickets WHERE status = 'open' GROUP BY assigned_team;
```

### Critical Tickets
```sql
SELECT * FROM tickets WHERE urgency = 'critical' ORDER BY created_at DESC;
```

### Tickets by Channel
```sql
SELECT channel, COUNT(*) FROM tickets GROUP BY channel;
```

---

## 📝 Usage Tips

1. **Replace team names** - Use exact team names from your database
2. **Adjust dates** - Change `-1 day` to `-7 days` or other ranges
3. **Add LIMIT** - Append `LIMIT 10` to restrict results
4. **Combine conditions** - Use `AND`/`OR` for complex filters
5. **Sort options** - Change `DESC` to `ASC` for ascending order

---

## 🔗 Related Files

- `SQL_QUERIES_BY_TEAM.md` - Comprehensive SQL queries guide
- `OPEN_IN_DB_BROWSER.md` - How to open database in DB Browser

---

## 📑 Database Indices

### View All Indices
```sql
SELECT name, tbl_name, sql 
FROM sqlite_master 
WHERE type='index' 
AND name NOT LIKE 'sqlite_%'
ORDER BY tbl_name, name;
```

### View Indices for Specific Table
```sql
PRAGMA index_list('tickets');
```

### View Columns in an Index
```sql
PRAGMA index_info('index_name');
```

### View All Indices with Python
```bash
python view_database.py indices
```

### Quick Index Check
```sql
-- See all indices and their tables
SELECT type, name, tbl_name 
FROM sqlite_master 
WHERE type='index';
```

