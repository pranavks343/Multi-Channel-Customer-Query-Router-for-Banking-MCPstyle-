# SQL Queries by Team - Execute in DB Browser for SQLite

Use these queries in the **"Execute SQL"** tab of DB Browser for SQLite to view and analyze data for each team.

---

## 🔍 General Queries (All Teams)

### View All Tickets
```sql
SELECT 
    ticket_id,
    channel,
    sender,
    subject,
    urgency,
    status,
    assigned_team,
    created_at
FROM tickets
ORDER BY created_at DESC;
```

### Count Tickets by Team
```sql
SELECT 
    assigned_team,
    COUNT(*) as ticket_count,
    COUNT(CASE WHEN status = 'open' THEN 1 END) as open_count,
    COUNT(CASE WHEN status = 'closed' THEN 1 END) as closed_count
FROM tickets
GROUP BY assigned_team
ORDER BY ticket_count DESC;
```

### Count Tickets by Urgency and Team
```sql
SELECT 
    assigned_team,
    urgency,
    COUNT(*) as count
FROM tickets
GROUP BY assigned_team, urgency
ORDER BY assigned_team, 
    CASE urgency
        WHEN 'critical' THEN 1
        WHEN 'high' THEN 2
        WHEN 'medium' THEN 3
        WHEN 'low' THEN 4
    END;
```

---

## 👥 KYC Team Queries

### All KYC Team Tickets
```sql
SELECT 
    ticket_id,
    channel,
    sender,
    subject,
    message,
    urgency,
    status,
    intent,
    created_at,
    updated_at
FROM tickets
WHERE assigned_team = 'KYC Team'
ORDER BY created_at DESC;
```

### KYC Team - Open Tickets Only
```sql
SELECT 
    ticket_id,
    sender,
    subject,
    urgency,
    created_at
FROM tickets
WHERE assigned_team = 'KYC Team' 
  AND status = 'open'
ORDER BY 
    CASE urgency
        WHEN 'critical' THEN 1
        WHEN 'high' THEN 2
        WHEN 'medium' THEN 3
        WHEN 'low' THEN 4
    END,
    created_at DESC;
```

### KYC Team - Tickets by Intent
```sql
SELECT 
    intent,
    COUNT(*) as count,
    COUNT(CASE WHEN status = 'open' THEN 1 END) as open_count
FROM tickets
WHERE assigned_team = 'KYC Team'
GROUP BY intent
ORDER BY count DESC;
```

### KYC Team - Recent Activity (Last 7 Days)
```sql
SELECT 
    ticket_id,
    sender,
    subject,
    status,
    urgency,
    created_at
FROM tickets
WHERE assigned_team = 'KYC Team'
  AND created_at >= datetime('now', '-7 days')
ORDER BY created_at DESC;
```

---

## 💻 Tech Support Queries

### All Tech Support Tickets
```sql
SELECT 
    ticket_id,
    channel,
    sender,
    subject,
    message,
    urgency,
    status,
    intent,
    created_at,
    updated_at
FROM tickets
WHERE assigned_team = 'Tech Support'
ORDER BY created_at DESC;
```

### Tech Support - Critical/High Urgency Tickets
```sql
SELECT 
    ticket_id,
    sender,
    subject,
    message,
    urgency,
    status,
    created_at
FROM tickets
WHERE assigned_team = 'Tech Support'
  AND urgency IN ('critical', 'high')
ORDER BY 
    CASE urgency
        WHEN 'critical' THEN 1
        WHEN 'high' THEN 2
    END,
    created_at DESC;
```

### Tech Support - Tickets by Intent Type
```sql
SELECT 
    intent,
    COUNT(*) as total_tickets,
    COUNT(CASE WHEN status = 'open' THEN 1 END) as open_tickets,
    COUNT(CASE WHEN urgency = 'critical' THEN 1 END) as critical_count
FROM tickets
WHERE assigned_team = 'Tech Support'
GROUP BY intent
ORDER BY total_tickets DESC;
```

### Tech Support - Open Tickets Needing Attention
```sql
SELECT 
    ticket_id,
    sender,
    subject,
    urgency,
    created_at,
    updated_at,
    julianday('now') - julianday(created_at) as days_open
FROM tickets
WHERE assigned_team = 'Tech Support'
  AND status = 'open'
ORDER BY 
    CASE urgency
        WHEN 'critical' THEN 1
        WHEN 'high' THEN 2
        WHEN 'medium' THEN 3
        WHEN 'low' THEN 4
    END,
    created_at ASC;
```

---

## 💰 Finance Team Queries

### All Finance Team Tickets
```sql
SELECT 
    ticket_id,
    channel,
    sender,
    subject,
    message,
    urgency,
    status,
    intent,
    created_at,
    updated_at
FROM tickets
WHERE assigned_team = 'Finance Team'
ORDER BY created_at DESC;
```

### Finance Team - Billing/Invoice Related Tickets
```sql
SELECT 
    ticket_id,
    sender,
    subject,
    message,
    urgency,
    status,
    created_at
FROM tickets
WHERE assigned_team = 'Finance Team'
  AND (subject LIKE '%invoice%' 
       OR subject LIKE '%billing%'
       OR subject LIKE '%payment%'
       OR message LIKE '%invoice%'
       OR message LIKE '%billing%'
       OR message LIKE '%refund%')
ORDER BY urgency DESC, created_at DESC;
```

### Finance Team - Tickets by Status
```sql
SELECT 
    status,
    COUNT(*) as count,
    GROUP_CONCAT(ticket_id, ', ') as ticket_ids
FROM tickets
WHERE assigned_team = 'Finance Team'
GROUP BY status
ORDER BY 
    CASE status
        WHEN 'open' THEN 1
        WHEN 'pending' THEN 2
        WHEN 'resolved' THEN 3
        WHEN 'closed' THEN 4
    END;
```

### Finance Team - High Urgency Tickets
```sql
SELECT 
    ticket_id,
    sender,
    subject,
    urgency,
    status,
    created_at
FROM tickets
WHERE assigned_team = 'Finance Team'
  AND urgency IN ('critical', 'high')
ORDER BY created_at DESC;
```

---

## ⚖️ Compliance Team Queries

### All Compliance Team Tickets
```sql
SELECT 
    ticket_id,
    channel,
    sender,
    subject,
    message,
    urgency,
    status,
    intent,
    created_at,
    updated_at
FROM tickets
WHERE assigned_team = 'Compliance Team'
ORDER BY created_at DESC;
```

### Compliance Team - Audit/Regulatory Requests
```sql
SELECT 
    ticket_id,
    sender,
    subject,
    message,
    urgency,
    status,
    created_at
FROM tickets
WHERE assigned_team = 'Compliance Team'
  AND (subject LIKE '%audit%'
       OR subject LIKE '%GDPR%'
       OR subject LIKE '%compliance%'
       OR subject LIKE '%regulatory%'
       OR message LIKE '%audit%'
       OR message LIKE '%GDPR%'
       OR message LIKE '%PCI%'
       OR message LIKE '%SOC%')
ORDER BY urgency DESC, created_at DESC;
```

### Compliance Team - Open High Priority Tickets
```sql
SELECT 
    ticket_id,
    sender,
    subject,
    urgency,
    created_at,
    updated_at
FROM tickets
WHERE assigned_team = 'Compliance Team'
  AND status = 'open'
  AND urgency IN ('critical', 'high')
ORDER BY 
    CASE urgency
        WHEN 'critical' THEN 1
        WHEN 'high' THEN 2
    END,
    created_at ASC;
```

---

## 📈 Sales Team Queries

### All Sales Team Tickets
```sql
SELECT 
    ticket_id,
    channel,
    sender,
    subject,
    message,
    urgency,
    status,
    intent,
    created_at,
    updated_at
FROM tickets
WHERE assigned_team = 'Sales Team'
ORDER BY created_at DESC;
```

### Sales Team - Demo/Pricing Inquiries
```sql
SELECT 
    ticket_id,
    sender,
    subject,
    message,
    urgency,
    status,
    created_at
FROM tickets
WHERE assigned_team = 'Sales Team'
  AND (subject LIKE '%demo%'
       OR subject LIKE '%pricing%'
       OR subject LIKE '%enterprise%'
       OR subject LIKE '%partnership%'
       OR message LIKE '%demo%'
       OR message LIKE '%pricing%'
       OR message LIKE '%enterprise%')
ORDER BY created_at DESC;
```

### Sales Team - Open Leads
```sql
SELECT 
    ticket_id,
    sender,
    subject,
    urgency,
    created_at
FROM tickets
WHERE assigned_team = 'Sales Team'
  AND status = 'open'
ORDER BY created_at DESC;
```

---

## 🆘 General Support Queries

### All General Support Tickets
```sql
SELECT 
    ticket_id,
    channel,
    sender,
    subject,
    message,
    urgency,
    status,
    intent,
    created_at,
    updated_at
FROM tickets
WHERE assigned_team = 'General Support'
ORDER BY created_at DESC;
```

### General Support - Documentation Questions
```sql
SELECT 
    ticket_id,
    sender,
    subject,
    message,
    urgency,
    status,
    created_at
FROM tickets
WHERE assigned_team = 'General Support'
  AND (subject LIKE '%documentation%'
       OR subject LIKE '%documentation%'
       OR message LIKE '%documentation%'
       OR message LIKE '%how to%'
       OR message LIKE '%guide%')
ORDER BY created_at DESC;
```

---

## 🔄 Triage Team Queries

### All Triage Team Tickets
```sql
SELECT 
    ticket_id,
    channel,
    sender,
    subject,
    message,
    urgency,
    status,
    intent,
    created_at,
    updated_at
FROM tickets
WHERE assigned_team = 'Triage Team'
ORDER BY created_at DESC;
```

### Triage Team - Pending Review
```sql
SELECT 
    ticket_id,
    sender,
    subject,
    urgency,
    status,
    created_at
FROM tickets
WHERE assigned_team = 'Triage Team'
  AND status = 'open'
ORDER BY created_at ASC;
```

---

## 📊 Advanced Analytics Queries

### Team Performance Summary
```sql
SELECT 
    assigned_team,
    COUNT(*) as total_tickets,
    COUNT(CASE WHEN status = 'open' THEN 1 END) as open_tickets,
    COUNT(CASE WHEN status = 'closed' THEN 1 END) as closed_tickets,
    COUNT(CASE WHEN urgency = 'critical' THEN 1 END) as critical_tickets,
    COUNT(CASE WHEN urgency = 'high' THEN 1 END) as high_tickets,
    ROUND(AVG(julianday('now') - julianday(created_at)), 2) as avg_days_open
FROM tickets
GROUP BY assigned_team
ORDER BY total_tickets DESC;
```

### Tickets Created Today by Team
```sql
SELECT 
    assigned_team,
    COUNT(*) as tickets_today
FROM tickets
WHERE DATE(created_at) = DATE('now')
GROUP BY assigned_team
ORDER BY tickets_today DESC;
```

### Channel Distribution by Team
```sql
SELECT 
    assigned_team,
    channel,
    COUNT(*) as count
FROM tickets
GROUP BY assigned_team, channel
ORDER BY assigned_team, count DESC;
```

### Routing Events for a Specific Team
```sql
SELECT 
    rl.ticket_id,
    rl.event_type,
    rl.timestamp,
    t.assigned_team,
    t.subject
FROM routing_log rl
JOIN tickets t ON rl.ticket_id = t.ticket_id
WHERE t.assigned_team = 'Tech Support'  -- Change team name here
ORDER BY rl.timestamp DESC
LIMIT 50;
```

### Most Common Intents by Team
```sql
SELECT 
    assigned_team,
    intent,
    COUNT(*) as count
FROM tickets
GROUP BY assigned_team, intent
ORDER BY assigned_team, count DESC;
```

---

## 🔍 Search Queries

### Search Tickets by Sender Email
```sql
SELECT 
    ticket_id,
    sender,
    subject,
    assigned_team,
    urgency,
    status,
    created_at
FROM tickets
WHERE sender LIKE '%@example.com%'  -- Replace with email domain
ORDER BY created_at DESC;
```

### Search Tickets by Keyword in Message
```sql
SELECT 
    ticket_id,
    sender,
    subject,
    assigned_team,
    urgency,
    status,
    created_at
FROM tickets
WHERE message LIKE '%API error%'  -- Replace with search term
   OR subject LIKE '%API error%'
ORDER BY created_at DESC;
```

### Find Tickets Updated Recently
```sql
SELECT 
    ticket_id,
    sender,
    subject,
    assigned_team,
    status,
    updated_at,
    created_at
FROM tickets
WHERE updated_at >= datetime('now', '-1 day')
ORDER BY updated_at DESC;
```

---

## 📝 Notes

- Replace team names in queries with actual team names from your database
- Use `LIKE '%keyword%'` for partial text matching
- Adjust date ranges (`-7 days`, `-1 day`) as needed
- Use `LIMIT` to restrict result count
- Combine queries for more complex analysis

---

## 🎯 Quick Reference

**View all tickets for a team:**
```sql
SELECT * FROM tickets WHERE assigned_team = 'Team Name' ORDER BY created_at DESC;
```

**Count open tickets by team:**
```sql
SELECT assigned_team, COUNT(*) FROM tickets WHERE status = 'open' GROUP BY assigned_team;
```

**Find critical tickets:**
```sql
SELECT * FROM tickets WHERE urgency = 'critical' ORDER BY created_at DESC;
```

