#!/usr/bin/env python3
"""
Simple script to view SQLite database contents.
"""
import json
import sqlite3
from datetime import datetime


def view_database(db_path="query_router.db"):
    """View all data in the database."""
    print("=" * 80)
    print("SQLite Database Viewer - query_router.db")
    print("=" * 80)
    print()

    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # View Teams
        print("📋 TEAMS TABLE")
        print("-" * 80)
        cursor.execute("SELECT * FROM teams")
        teams = cursor.fetchall()

        if teams:
            for team in teams:
                print(f"  • {team['team_name']}")
                print(f"    Email: {team['team_email']}")
                print(f"    Description: {team['description']}")
                print()
        else:
            print("  No teams found.")

        print()

        # View Tickets
        print("🎫 TICKETS TABLE")
        print("-" * 80)
        cursor.execute("SELECT COUNT(*) as count FROM tickets")
        ticket_count = cursor.fetchone()["count"]
        print(f"  Total Tickets: {ticket_count}")
        print()

        if ticket_count > 0:
            cursor.execute(
                """
                SELECT ticket_id, channel, intent, urgency, assigned_team, 
                       status, created_at, subject
                FROM tickets 
                ORDER BY created_at DESC 
                LIMIT 10
            """
            )
            tickets = cursor.fetchall()

            for i, ticket in enumerate(tickets, 1):
                print(f"  {i}. Ticket ID: {ticket['ticket_id']}")
                print(f"     Channel: {ticket['channel']}")
                print(f"     Subject: {ticket['subject']}")
                print(f"     Intent: {ticket['intent']}")
                print(f"     Urgency: {ticket['urgency']}")
                print(f"     Team: {ticket['assigned_team']}")
                print(f"     Status: {ticket['status']}")
                print(f"     Created: {ticket['created_at']}")
                print()

        # View Tickets by Status
        print("📊 TICKETS BY STATUS")
        print("-" * 80)
        cursor.execute(
            """
            SELECT status, COUNT(*) as count 
            FROM tickets 
            GROUP BY status
        """
        )
        status_counts = cursor.fetchall()

        if status_counts:
            for row in status_counts:
                print(f"  {row['status']}: {row['count']}")
        else:
            print("  No tickets yet.")

        print()

        # View Tickets by Team
        print("👥 TICKETS BY TEAM")
        print("-" * 80)
        cursor.execute(
            """
            SELECT assigned_team, COUNT(*) as count 
            FROM tickets 
            GROUP BY assigned_team
        """
        )
        team_counts = cursor.fetchall()

        if team_counts:
            for row in team_counts:
                print(f"  {row['assigned_team']}: {row['count']}")
        else:
            print("  No tickets assigned yet.")

        print()

        # View Routing Log
        print("📝 ROUTING LOG")
        print("-" * 80)
        cursor.execute("SELECT COUNT(*) as count FROM routing_log")
        log_count = cursor.fetchone()["count"]
        print(f"  Total Log Entries: {log_count}")

        if log_count > 0:
            cursor.execute(
                """
                SELECT ticket_id, event_type, timestamp 
                FROM routing_log 
                ORDER BY timestamp DESC 
                LIMIT 5
            """
            )
            logs = cursor.fetchall()
            print(f"\n  Recent Events:")
            for log in logs:
                print(
                    f"    • {log['event_type']} - {log['ticket_id']} - {log['timestamp']}"
                )

        print()
        print("=" * 80)

        conn.close()

    except sqlite3.Error as e:
        print(f"❌ Database Error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")


def query_custom(db_path="query_router.db", sql_query=None):
    """Run a custom SQL query."""
    if not sql_query:
        print("No query provided.")
        return

    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(sql_query)
        rows = cursor.fetchall()

        if rows:
            # Print column names
            print("\nResults:")
            print("-" * 80)
            for row in rows:
                print(dict(row))
        else:
            print("No results found.")

        conn.close()

    except sqlite3.Error as e:
        print(f"❌ SQL Error: {e}")


def show_schema(db_path="query_router.db"):
    """Show database schema."""
    print("=" * 80)
    print("DATABASE SCHEMA")
    print("=" * 80)
    print()

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        for table in tables:
            table_name = table[0]
            print(f"📊 Table: {table_name}")
            print("-" * 80)

            # Get table schema
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()

            for col in columns:
                col_id, name, col_type, not_null, default, pk = col
                pk_marker = " (PRIMARY KEY)" if pk else ""
                null_marker = " NOT NULL" if not_null else ""
                default_marker = f" DEFAULT {default}" if default else ""
                print(f"  • {name}: {col_type}{pk_marker}{null_marker}{default_marker}")

            print()

        conn.close()

    except sqlite3.Error as e:
        print(f"❌ Database Error: {e}")


def show_indices(db_path="query_router.db"):
    """Show all database indices."""
    print("=" * 80)
    print("DATABASE INDICES")
    print("=" * 80)
    print()

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Get all indices
        cursor.execute(
            """
            SELECT name, tbl_name, sql 
            FROM sqlite_master 
            WHERE type='index' 
            AND name NOT LIKE 'sqlite_%'
            ORDER BY tbl_name, name
        """
        )
        indices = cursor.fetchall()

        if not indices:
            print("  No custom indices found.")
            print(
                "  (SQLite automatically creates indices for PRIMARY KEY and UNIQUE constraints)"
            )
            print()
        else:
            current_table = None
            for index_name, table_name, index_sql in indices:
                if current_table != table_name:
                    if current_table is not None:
                        print()
                    print(f"📊 Table: {table_name}")
                    print("-" * 80)
                    current_table = table_name

                print(f"  • Index: {index_name}")
                if index_sql:
                    print(f"    SQL: {index_sql}")
                else:
                    # Auto-generated index (PRIMARY KEY or UNIQUE constraint)
                    print(
                        f"    Type: Auto-generated (PRIMARY KEY or UNIQUE constraint)"
                    )
                print()

        # Also show indices per table using PRAGMA
        print("=" * 80)
        print("INDICES BY TABLE (using PRAGMA)")
        print("=" * 80)
        print()

        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        for table in tables:
            table_name = table[0]
            print(f"📊 Table: {table_name}")
            print("-" * 80)

            # Get indices for this table
            cursor.execute(f"PRAGMA index_list({table_name})")
            table_indices = cursor.fetchall()

            if table_indices:
                for idx_info in table_indices:
                    seq, idx_name, unique, origin, partial = idx_info
                    unique_str = "UNIQUE" if unique else "NON-UNIQUE"
                    origin_str = f" ({origin})" if origin != "c" else ""

                    print(f"  • {idx_name} - {unique_str}{origin_str}")

                    # Get columns in this index
                    cursor.execute(f"PRAGMA index_info({idx_name})")
                    index_columns = cursor.fetchall()

                    if index_columns:
                        cols = [
                            col[2] for col in index_columns
                        ]  # Column name is at index 2
                        print(f"    Columns: {', '.join(cols)}")
                    print()
            else:
                print("  No indices found for this table.")
                print()

        conn.close()

    except sqlite3.Error as e:
        print(f"❌ Database Error: {e}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "schema":
            show_schema()
        elif command == "indices" or command == "indexes":
            show_indices()
        elif command == "query" and len(sys.argv) > 2:
            query_custom(sql_query=" ".join(sys.argv[2:]))
        else:
            print("Usage:")
            print("  python view_database.py              # View all data")
            print("  python view_database.py schema       # Show schema")
            print("  python view_database.py indices     # Show all indices")
            print("  python view_database.py query 'SQL'  # Run custom query")
    else:
        view_database()
