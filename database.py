"""
Database setup and management for the Customer Query Router system.
"""

import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
import json


class Database:
    def __init__(self, db_path: str = "query_router.db"):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Get a database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialize the database schema."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create tickets table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id TEXT UNIQUE NOT NULL,
                channel TEXT NOT NULL,
                sender TEXT,
                subject TEXT,
                message TEXT NOT NULL,
                intent TEXT,
                urgency TEXT,
                assigned_team TEXT,
                status TEXT DEFAULT 'open',
                response TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT
            )
        """)
        
        # Create routing_log table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS routing_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                event_data TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (ticket_id) REFERENCES tickets (ticket_id)
            )
        """)
        
        # Create teams table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS teams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_name TEXT UNIQUE NOT NULL,
                team_email TEXT,
                description TEXT,
                active BOOLEAN DEFAULT 1
            )
        """)
        
        # Create learning_patterns table for storing learned patterns
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS learning_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_type TEXT NOT NULL,
                pattern_key TEXT NOT NULL,
                pattern_value TEXT NOT NULL,
                confidence REAL DEFAULT 1.0,
                usage_count INTEGER DEFAULT 1,
                last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(pattern_type, pattern_key, pattern_value)
            )
        """)
        
        # Create learning_feedback table for tracking routing corrections
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS learning_feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id TEXT NOT NULL,
                original_intent TEXT,
                corrected_intent TEXT,
                original_team TEXT,
                corrected_team TEXT,
                feedback_type TEXT NOT NULL,
                feedback_data TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (ticket_id) REFERENCES tickets (ticket_id)
            )
        """)
        
        conn.commit()
        conn.close()
        
        # Initialize default teams
        self._init_default_teams()
    
    def _init_default_teams(self):
        """Initialize default teams."""
        default_teams = [
            {
                "team_name": "KYC Team",
                "team_email": "kyc@finlink.com",
                "description": "Handles account verification, identity checks, and compliance documentation"
            },
            {
                "team_name": "Tech Support",
                "team_email": "tech-support@finlink.com",
                "description": "Handles API issues, technical errors, and integration problems"
            },
            {
                "team_name": "Finance Team",
                "team_email": "finance@finlink.com",
                "description": "Handles billing, invoices, payment processing, and refunds"
            },
            {
                "team_name": "Compliance Team",
                "team_email": "compliance@finlink.com",
                "description": "Handles regulatory queries, audit requests, and policy questions"
            },
            {
                "team_name": "Sales Team",
                "team_email": "sales@finlink.com",
                "description": "Handles new customer inquiries and business development"
            },
            {
                "team_name": "Triage Team",
                "team_email": "triage@finlink.com",
                "description": "Handles low-confidence classifications and tickets requiring manual review"
            },
            {
                "team_name": "General Support",
                "team_email": "support@finlink.com",
                "description": "Handles general help requests, documentation questions, and non-urgent inquiries"
            }
        ]
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        for team in default_teams:
            try:
                cursor.execute("""
                    INSERT INTO teams (team_name, team_email, description)
                    VALUES (?, ?, ?)
                """, (team["team_name"], team["team_email"], team["description"]))
            except sqlite3.IntegrityError:
                # Team already exists
                pass
        
        conn.commit()
        conn.close()
    
    def create_ticket(self, ticket_data: Dict) -> str:
        """Create a new ticket."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        ticket_id = ticket_data.get("ticket_id")
        metadata = json.dumps(ticket_data.get("metadata", {}))
        
        cursor.execute("""
            INSERT INTO tickets 
            (ticket_id, channel, sender, subject, message, intent, urgency, 
             assigned_team, status, response, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            ticket_id,
            ticket_data.get("channel"),
            ticket_data.get("sender"),
            ticket_data.get("subject"),
            ticket_data.get("message"),
            ticket_data.get("intent"),
            ticket_data.get("urgency"),
            ticket_data.get("assigned_team"),
            ticket_data.get("status", "open"),
            ticket_data.get("response"),
            metadata
        ))
        
        conn.commit()
        conn.close()
        
        return ticket_id
    
    def get_ticket(self, ticket_id: str) -> Optional[Dict]:
        """Get a ticket by ID."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM tickets WHERE ticket_id = ?", (ticket_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    def get_all_tickets(self, status: Optional[str] = None) -> List[Dict]:
        """Get all tickets, optionally filtered by status."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if status:
            cursor.execute("SELECT * FROM tickets WHERE status = ? ORDER BY created_at DESC", (status,))
        else:
            cursor.execute("SELECT * FROM tickets ORDER BY created_at DESC")
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def update_ticket(self, ticket_id: str, updates: Dict):
        """Update a ticket."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Build update query dynamically
        set_clause = ", ".join([f"{key} = ?" for key in updates.keys()])
        values = list(updates.values())
        values.append(ticket_id)
        
        cursor.execute(f"""
            UPDATE tickets 
            SET {set_clause}, updated_at = CURRENT_TIMESTAMP
            WHERE ticket_id = ?
        """, values)
        
        conn.commit()
        conn.close()
    
    def log_routing_event(self, ticket_id: str, event_type: str, event_data: Dict):
        """Log a routing event."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO routing_log (ticket_id, event_type, event_data)
            VALUES (?, ?, ?)
        """, (ticket_id, event_type, json.dumps(event_data)))
        
        conn.commit()
        conn.close()
    
    def get_routing_events(self, ticket_id: str) -> List[Dict]:
        """Get routing events for a ticket."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM routing_log 
            WHERE ticket_id = ? 
            ORDER BY timestamp ASC
        """, (ticket_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_teams(self) -> List[Dict]:
        """Get all teams."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM teams WHERE active = 1")
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def delete_older_tickets(self, before_date: str = None) -> int:
        """
        Delete tickets older than a specified date.
        
        Args:
            before_date: Date string in format 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM:SS'.
                        If None, deletes all tickets older than today.
        
        Returns:
            Number of tickets deleted
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if before_date is None:
            # Default: delete all tickets older than today
            before_date = datetime.now().strftime("%Y-%m-%d")
        
        # First, get ticket IDs that will be deleted
        cursor.execute("""
            SELECT ticket_id FROM tickets 
            WHERE created_at < ?
        """, (before_date,))
        ticket_ids = [row[0] for row in cursor.fetchall()]
        
        if not ticket_ids:
            conn.close()
            return 0
        
        # Delete related routing_log entries first (due to foreign key)
        placeholders = ','.join(['?'] * len(ticket_ids))
        cursor.execute(f"""
            DELETE FROM routing_log 
            WHERE ticket_id IN ({placeholders})
        """, ticket_ids)
        
        # Delete tickets
        cursor.execute("""
            DELETE FROM tickets 
            WHERE created_at < ?
        """, (before_date,))
        
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        return deleted_count
    
    def delete_ticket(self, ticket_id: str) -> bool:
        """
        Delete a specific ticket by ID and its related routing logs.
        
        Args:
            ticket_id: The ticket ID to delete
            
        Returns:
            True if ticket was deleted, False if ticket not found
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Check if ticket exists
        cursor.execute("SELECT ticket_id FROM tickets WHERE ticket_id = ?", (ticket_id,))
        if not cursor.fetchone():
            conn.close()
            return False
        
        # Delete related routing_log entries first (due to foreign key)
        cursor.execute("DELETE FROM routing_log WHERE ticket_id = ?", (ticket_id,))
        
        # Delete related learning_feedback entries
        cursor.execute("DELETE FROM learning_feedback WHERE ticket_id = ?", (ticket_id,))
        
        # Delete the ticket
        cursor.execute("DELETE FROM tickets WHERE ticket_id = ?", (ticket_id,))
        
        conn.commit()
        conn.close()
        
        return True
    
    def delete_all_tickets(self) -> int:
        """
        Delete all tickets and their related routing logs.
        
        Returns:
            Number of tickets deleted
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get count before deletion
        cursor.execute("SELECT COUNT(*) FROM tickets")
        count = cursor.fetchone()[0]
        
        # Delete routing_log entries first
        cursor.execute("DELETE FROM routing_log")
        
        # Delete learning_feedback entries
        cursor.execute("DELETE FROM learning_feedback")
        
        # Delete all tickets
        cursor.execute("DELETE FROM tickets")
        
        conn.commit()
        conn.close()
        
        return count
    
    def save_learning_pattern(self, pattern_type: str, pattern_key: str, pattern_value: str, confidence: float = 1.0):
        """Save or update a learning pattern."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Check if pattern exists
        cursor.execute("""
            SELECT id, usage_count FROM learning_patterns 
            WHERE pattern_type = ? AND pattern_key = ? AND pattern_value = ?
        """, (pattern_type, pattern_key, pattern_value))
        
        existing = cursor.fetchone()
        
        if existing:
            # Update existing pattern
            new_count = existing[1] + 1
            cursor.execute("""
                UPDATE learning_patterns 
                SET usage_count = ?, last_used = CURRENT_TIMESTAMP, confidence = ?
                WHERE id = ?
            """, (new_count, confidence, existing[0]))
        else:
            # Insert new pattern
            cursor.execute("""
                INSERT INTO learning_patterns 
                (pattern_type, pattern_key, pattern_value, confidence, usage_count)
                VALUES (?, ?, ?, ?, 1)
            """, (pattern_type, pattern_key, pattern_value, confidence))
        
        conn.commit()
        conn.close()
    
    def get_learning_patterns(self, pattern_type: str = None) -> List[Dict]:
        """Get learning patterns, optionally filtered by type."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if pattern_type:
            cursor.execute("""
                SELECT * FROM learning_patterns 
                WHERE pattern_type = ?
                ORDER BY usage_count DESC, confidence DESC
            """, (pattern_type,))
        else:
            cursor.execute("""
                SELECT * FROM learning_patterns 
                ORDER BY usage_count DESC, confidence DESC
            """)
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def save_feedback(self, ticket_id: str, original_intent: str = None, corrected_intent: str = None,
                     original_team: str = None, corrected_team: str = None, feedback_type: str = "reassignment",
                     feedback_data: Dict = None):
        """Save feedback about routing corrections."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO learning_feedback 
            (ticket_id, original_intent, corrected_intent, original_team, corrected_team, 
             feedback_type, feedback_data)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            ticket_id,
            original_intent,
            corrected_intent,
            original_team,
            corrected_team,
            feedback_type,
            json.dumps(feedback_data or {})
        ))
        
        conn.commit()
        conn.close()
    
    def get_feedback_history(self, limit: int = 100) -> List[Dict]:
        """Get recent feedback history."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM learning_feedback 
            ORDER BY timestamp DESC 
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
