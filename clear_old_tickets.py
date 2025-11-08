#!/usr/bin/env python3
"""
Script to clear older tickets from the database.
"""

import os
import sys
from datetime import datetime, timedelta

from database import Database


def main():
    """Clear older tickets."""
    print("=" * 80)
    print("🗑️  Clear Older Tickets")
    print("=" * 80)
    print()

    # Initialize database
    db = Database()

    # Get current ticket count
    all_tickets = db.get_all_tickets()
    print(f"Current tickets in database: {len(all_tickets)}")

    if len(all_tickets) == 0:
        print("✓ No tickets to delete.")
        return

    # Show date range
    if all_tickets:
        dates = [ticket["created_at"] for ticket in all_tickets]
        print(f"Oldest ticket: {min(dates)}")
        print(f"Newest ticket: {max(dates)}")
    print()

    # Ask user what to delete
    print("Options:")
    print("  1. Delete all tickets older than today")
    print("  2. Delete all tickets older than a specific date")
    print("  3. Delete ALL tickets")
    print()

    choice = input("Enter your choice (1-3): ").strip()

    deleted_count = 0

    if choice == "1":
        # Delete tickets older than today
        today = datetime.now().strftime("%Y-%m-%d")
        print(f"\nDeleting tickets older than {today}...")
        deleted_count = db.delete_older_tickets(before_date=today)

    elif choice == "2":
        # Delete tickets older than a specific date
        date_str = input("\nEnter date (YYYY-MM-DD): ").strip()
        try:
            # Validate date format
            datetime.strptime(date_str, "%Y-%m-%d")
            print(f"\nDeleting tickets older than {date_str}...")
            deleted_count = db.delete_older_tickets(before_date=date_str)
        except ValueError:
            print("❌ Invalid date format. Please use YYYY-MM-DD")
            sys.exit(1)

    elif choice == "3":
        # Delete all tickets
        confirm = (
            input("\n⚠️  Are you sure you want to delete ALL tickets? (yes/no): ")
            .strip()
            .lower()
        )
        if confirm == "yes":
            print("\nDeleting all tickets...")
            deleted_count = db.delete_all_tickets()
        else:
            print("Operation cancelled.")
            return
    else:
        print("❌ Invalid choice.")
        sys.exit(1)

    # Show results
    print()
    print("=" * 80)
    if deleted_count > 0:
        print(f"✓ Successfully deleted {deleted_count} ticket(s)")

        # Show remaining tickets
        remaining = db.get_all_tickets()
        print(f"Remaining tickets: {len(remaining)}")
    else:
        print("✓ No tickets were deleted (none matched the criteria)")
    print("=" * 80)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
