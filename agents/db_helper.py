#!/usr/bin/env python3
"""
Interactive database helper - Easy SQLite operations.
"""
import json
import sqlite3
import sys
from datetime import datetime

DB_PATH = "query_router.db"


def main_menu():
    """Display main menu."""
    print("\n" + "=" * 80)
    print("📊 SQLite Database Helper - query_router.db")
    print("=" * 80)
    print("\nWhat would you like to do?\n")
    print("  1. View all tickets")
    print("  2. View tickets by status (open/closed)")
    print("  3. View tickets by team")
    print("  4. View a specific ticket")
    print("  5. View all teams")
    print("  6. View routing logs")
    print("  7. Search tickets by keyword")
    print("  8. Show database statistics")
    print("  9. Export tickets to CSV")
    print("  10. Backup database")
    print("  11. Run custom SQL query")
    print("  0. Exit")
    print()


def get_connection():
    """Get database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def view_all_tickets():
    """View all tickets."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tickets ORDER BY created_at DESC")
    tickets = cursor.fetchall()

    if not tickets:
        print("\n❌ No tickets found.")
        conn.close()
        return

    print(f"\n📋 Found {len(tickets)} tickets:\n")

    for i, ticket in enumerate(tickets, 1):
        print(f"{i}. [{ticket['urgency'].upper()}] {ticket['ticket_id']}")
        print(f"   Channel: {ticket['channel']} | Team: {ticket['assigned_team']}")
        print(f"   Subject: {ticket['subject']}")
        print(f"   Status: {ticket['status']} | Created: {ticket['created_at']}")
        print()

    conn.close()


def view_tickets_by_status():
    """View tickets filtered by status."""
    status = input("\nEnter status (open/closed/pending): ").strip().lower()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM tickets WHERE status = ? ORDER BY created_at DESC", (status,)
    )
    tickets = cursor.fetchall()

    if not tickets:
        print(f"\n❌ No {status} tickets found.")
        conn.close()
        return

    print(f"\n📋 Found {len(tickets)} {status} tickets:\n")

    for i, ticket in enumerate(tickets, 1):
        print(f"{i}. [{ticket['urgency'].upper()}] {ticket['ticket_id']}")
        print(f"   Team: {ticket['assigned_team']}")
        print(f"   Subject: {ticket['subject']}")
        print(f"   Created: {ticket['created_at']}")
        print()

    conn.close()


def view_tickets_by_team():
    """View tickets by team."""
    # First show available teams
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT assigned_team FROM tickets ORDER BY assigned_team")
    teams = cursor.fetchall()

    print("\n👥 Available teams:")
    for i, team in enumerate(teams, 1):
        print(f"  {i}. {team['assigned_team']}")

    team_name = input("\nEnter team name: ").strip()

    cursor.execute(
        "SELECT * FROM tickets WHERE assigned_team = ? ORDER BY created_at DESC",
        (team_name,),
    )
    tickets = cursor.fetchall()

    if not tickets:
        print(f"\n❌ No tickets found for team: {team_name}")
        conn.close()
        return

    print(f"\n📋 Found {len(tickets)} tickets for {team_name}:\n")

    for i, ticket in enumerate(tickets, 1):
        print(f"{i}. [{ticket['urgency'].upper()}] {ticket['ticket_id']}")
        print(f"   Subject: {ticket['subject']}")
        print(f"   Status: {ticket['status']} | Created: {ticket['created_at']}")
        print()

    conn.close()


def view_specific_ticket():
    """View detailed information about a specific ticket."""
    ticket_id = input("\nEnter ticket ID: ").strip()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tickets WHERE ticket_id = ?", (ticket_id,))
    ticket = cursor.fetchone()

    if not ticket:
        print(f"\n❌ Ticket not found: {ticket_id}")
        conn.close()
        return

    print("\n" + "=" * 80)
    print(f"🎫 Ticket Details: {ticket['ticket_id']}")
    print("=" * 80)
    print(f"Channel:       {ticket['channel']}")
    print(f"Sender:        {ticket['sender']}")
    print(f"Subject:       {ticket['subject']}")
    print(f"Intent:        {ticket['intent']}")
    print(f"Urgency:       {ticket['urgency']}")
    print(f"Assigned Team: {ticket['assigned_team']}")
    print(f"Status:        {ticket['status']}")
    print(f"Created:       {ticket['created_at']}")
    print(f"Updated:       {ticket['updated_at']}")
    print()
    print("Message:")
    print("-" * 80)
    print(ticket["message"])
    print()

    if ticket["response"]:
        print("Response:")
        print("-" * 80)
        print(ticket["response"])
        print()

    # Show routing history
    cursor.execute(
        "SELECT * FROM routing_log WHERE ticket_id = ? ORDER BY timestamp", (ticket_id,)
    )
    logs = cursor.fetchall()

    if logs:
        print("Routing History:")
        print("-" * 80)
        for log in logs:
            print(f"  • {log['event_type']} - {log['timestamp']}")
            if log["event_data"]:
                try:
                    data = json.loads(log["event_data"])
                    print(f"    Data: {data}")
                except:
                    pass
        print()

    conn.close()


def view_teams():
    """View all teams."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM teams WHERE active = 1")
    teams = cursor.fetchall()

    print("\n" + "=" * 80)
    print("👥 Teams")
    print("=" * 80)

    for team in teams:
        print(f"\n{team['team_name']}")
        print(f"  Email: {team['team_email']}")
        print(f"  Description: {team['description']}")

    conn.close()


def view_routing_logs():
    """View recent routing logs."""
    limit = input("\nHow many recent logs to show? (default: 20): ").strip()
    limit = int(limit) if limit.isdigit() else 20

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM routing_log ORDER BY timestamp DESC LIMIT {limit}")
    logs = cursor.fetchall()

    print(f"\n📝 Last {len(logs)} routing events:\n")

    for log in logs:
        print(f"• {log['timestamp']} | {log['ticket_id']}")
        print(f"  Event: {log['event_type']}")
        if log["event_data"]:
            try:
                data = json.loads(log["event_data"])
                print(f"  Data: {json.dumps(data, indent=2)}")
            except:
                print(f"  Data: {log['event_data']}")
        print()

    conn.close()


def search_tickets():
    """Search tickets by keyword."""
    keyword = input("\nEnter search keyword: ").strip()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM tickets 
        WHERE message LIKE ? OR subject LIKE ? OR sender LIKE ?
        ORDER BY created_at DESC
    """,
        (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"),
    )

    tickets = cursor.fetchall()

    if not tickets:
        print(f"\n❌ No tickets found matching: {keyword}")
        conn.close()
        return

    print(f"\n🔍 Found {len(tickets)} tickets matching '{keyword}':\n")

    for i, ticket in enumerate(tickets, 1):
        print(f"{i}. [{ticket['urgency'].upper()}] {ticket['ticket_id']}")
        print(f"   Subject: {ticket['subject']}")
        print(f"   Team: {ticket['assigned_team']} | Status: {ticket['status']}")
        print()

    conn.close()


def show_statistics():
    """Show database statistics."""
    conn = get_connection()
    cursor = conn.cursor()

    print("\n" + "=" * 80)
    print("📊 Database Statistics")
    print("=" * 80)

    # Total tickets
    cursor.execute("SELECT COUNT(*) as count FROM tickets")
    total = cursor.fetchone()["count"]
    print(f"\n📋 Total Tickets: {total}")

    # By status
    cursor.execute("SELECT status, COUNT(*) as count FROM tickets GROUP BY status")
    print("\nBy Status:")
    for row in cursor.fetchall():
        print(f"  • {row['status']}: {row['count']}")

    # By urgency
    cursor.execute("SELECT urgency, COUNT(*) as count FROM tickets GROUP BY urgency")
    print("\nBy Urgency:")
    for row in cursor.fetchall():
        print(f"  • {row['urgency']}: {row['count']}")

    # By team
    cursor.execute(
        "SELECT assigned_team, COUNT(*) as count FROM tickets GROUP BY assigned_team"
    )
    print("\nBy Team:")
    for row in cursor.fetchall():
        print(f"  • {row['assigned_team']}: {row['count']}")

    # By channel
    cursor.execute("SELECT channel, COUNT(*) as count FROM tickets GROUP BY channel")
    print("\nBy Channel:")
    for row in cursor.fetchall():
        print(f"  • {row['channel']}: {row['count']}")

    # Recent activity
    cursor.execute(
        "SELECT COUNT(*) as count FROM tickets WHERE date(created_at) = date('now')"
    )
    today = cursor.fetchone()["count"]
    print(f"\n🕒 Tickets Created Today: {today}")

    conn.close()


def export_to_csv():
    """Export tickets to CSV."""
    import csv

    filename = f"tickets_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tickets ORDER BY created_at DESC")
    tickets = cursor.fetchall()

    if not tickets:
        print("\n❌ No tickets to export.")
        conn.close()
        return

    with open(filename, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=tickets[0].keys())
        writer.writeheader()

        for ticket in tickets:
            writer.writerow(dict(ticket))

    print(f"\n✓ Exported {len(tickets)} tickets to: {filename}")
    conn.close()


def backup_database():
    """Backup the database."""
    import shutil

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"query_router_backup_{timestamp}.db"

    try:
        shutil.copy(DB_PATH, backup_name)
        print(f"\n✓ Database backed up to: {backup_name}")
    except Exception as e:
        print(f"\n❌ Backup failed: {e}")


def run_custom_query():
    """Run a custom SQL query."""
    print("\n⚠️  Be careful with UPDATE/DELETE queries!")
    query = input("\nEnter SQL query: ").strip()

    if not query:
        print("No query entered.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(query)

        # If it's a SELECT query, show results
        if query.strip().upper().startswith("SELECT"):
            rows = cursor.fetchall()
            if rows:
                print(f"\n✓ Found {len(rows)} results:\n")
                for i, row in enumerate(rows[:50], 1):  # Limit to 50 results
                    print(f"{i}. {dict(row)}")
                if len(rows) > 50:
                    print(f"\n... and {len(rows) - 50} more")
            else:
                print("\n❌ No results found.")
        else:
            # For INSERT/UPDATE/DELETE, commit changes
            conn.commit()
            print(f"\n✓ Query executed successfully. Rows affected: {cursor.rowcount}")

    except sqlite3.Error as e:
        print(f"\n❌ SQL Error: {e}")

    conn.close()


def main():
    """Main interactive loop."""
    while True:
        main_menu()
        choice = input("Enter your choice (0-11): ").strip()

        if choice == "0":
            print("\n👋 Goodbye!\n")
            break
        elif choice == "1":
            view_all_tickets()
        elif choice == "2":
            view_tickets_by_status()
        elif choice == "3":
            view_tickets_by_team()
        elif choice == "4":
            view_specific_ticket()
        elif choice == "5":
            view_teams()
        elif choice == "6":
            view_routing_logs()
        elif choice == "7":
            search_tickets()
        elif choice == "8":
            show_statistics()
        elif choice == "9":
            export_to_csv()
        elif choice == "10":
            backup_database()
        elif choice == "11":
            run_custom_query()
        else:
            print("\n❌ Invalid choice. Please try again.")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!\n")
        sys.exit(0)
