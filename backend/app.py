"""
Flask web application for Multi-Channel Customer Query Router.
Provides REST API and web UI for query routing.
"""

import json
import os
import sys
import time
from datetime import datetime

from dotenv import load_dotenv
from flask import (
    Flask,
    Response,
    jsonify,
    render_template,
    request,
    send_file,
    stream_with_context,
)

# Add parent directory to path to import from agents
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.router_agent import RouterAgent
from sample_data import get_canned_responses, get_sample_queries

load_dotenv()

# Set template folder to frontend/templates
template_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend', 'templates')
app = Flask(__name__, template_folder=template_dir)
app.config["JSON_SORT_KEYS"] = False

# Initialize router agent
router = RouterAgent()

# Store for server-sent events
event_subscribers = []


@app.route("/")
def index():
    """Serve the main web interface."""
    return render_template("index.html")


@app.route("/debug/tickets")
def debug_tickets():
    """Serve the debug tickets page."""
    return render_template("debug_tickets.html")


@app.route("/test/simple")
def test_simple():
    """Serve the simple test page."""
    return render_template("test_simple.html")


@app.route("/email")
def email_channel():
    """Serve the email channel page."""
    return render_template("email_channel.html")


@app.route("/api/submit_email", methods=["POST"])
def submit_email():
    """
    Submit an email for routing with NLP classification.

    This endpoint specifically handles email input and uses NLP to classify
    the category/intent based on the email subject and message body.

    Expected JSON:
    {
        "from": "sender@example.com",
        "subject": "Email subject line",
        "body": "Email message body",
        "timestamp": "2025-11-08T12:00:00" (optional),
        "attachments": ["file1.pdf"] (optional),
        "auto_respond": true (optional)
    }
    """
    try:
        data = request.get_json()

        # Validate required fields
        if not data:
            return jsonify({"error": "Missing request body"}), 400

        # Email channel requires at least body or subject
        body = data.get("body") or data.get("message") or ""
        subject = data.get("subject") or ""

        if not body and not subject:
            return (
                jsonify(
                    {
                        "error": "Missing required field: either 'body' or 'subject' must be provided"
                    }
                ),
                400,
            )

        # Use email channel
        channel = "email"
        sender = data.get("from") or data.get("sender")
        auto_respond = data.get("auto_respond", True)

        # Combine subject and body for NLP classification
        # The NLP classifier will analyze both to determine category/intent
        message = f"{subject}\n\n{body}".strip() if subject else body

        # Extract additional metadata for email channel
        metadata = {
            "channel_type": channel,
            "timestamp": data.get("timestamp", datetime.now().isoformat()),
            "attachments": data.get("attachments", []),
            "email_from": sender,
            "email_subject": subject,
            "email_body": body,
        }

        # Emit event: Processing started
        emit_event(
            {
                "type": "processing_started",
                "channel": channel,
                "timestamp": datetime.now().isoformat(),
            }
        )

        # Process the query - NLP classification happens automatically via RouterAgent
        # The IntentClassifier uses Gemini AI to analyze the message and classify:
        # - Intent category (kyc_verification, technical_support, billing_finance, etc.)
        # - Urgency level (critical, high, medium, low)
        # - Key entities and sentiment
        result = router.process_query(
            channel=channel,
            message=message,
            sender=sender,
            subject=subject,
            auto_respond=auto_respond,
            extra_metadata=metadata,
        )

        # Emit event: Routing completed
        emit_event(
            {
                "type": "routing_completed",
                "ticket_id": result["ticket_id"],
                "team": result["routing"]["final_team"],
                "urgency": result["classification"]["urgency"],
                "intent": result["classification"]["intent"],
                "timestamp": datetime.now().isoformat(),
            }
        )

        return (
            jsonify(
                {
                    "success": True,
                    "message": "Email processed and routed using NLP classification",
                    "result": {
                        "ticket_id": result["ticket_id"],
                        "classification": {
                            "intent": result["classification"]["intent"],
                            "category": result["classification"][
                                "intent"
                            ],  # Alias for clarity
                            "urgency": result["classification"]["urgency"],
                            "confidence": result["classification"]["confidence"],
                            "reasoning": result["classification"].get("reasoning", ""),
                            "key_entities": result["classification"].get(
                                "key_entities", []
                            ),
                            "sentiment": result["classification"].get(
                                "sentiment", "neutral"
                            ),
                        },
                        "routing": {
                            "assigned_team": result["routing"]["final_team"],
                            "escalate": result["routing"].get("escalate", False),
                        },
                        "response": result.get("response", {}),
                        "metadata": metadata,
                    },
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/submit_query", methods=["POST"])
def submit_query():
    """
    Submit a new customer query for routing.

    Expected JSON:
    {
        "channel": "form" | "email" | "chat",
        "message": "query text",
        "sender": "email@example.com",
        "subject": "optional subject",
        "auto_respond": true
    }
    """
    try:
        data = request.get_json()

        # Validate required fields
        if not data or "message" not in data:
            return jsonify({"error": "Missing required field: message"}), 400

        # Support multiple channels
        channel = data.get("channel", "form")
        if channel not in ["form", "email", "chat"]:
            channel = "form"  # Default to form

        message = data["message"]
        sender = data.get("sender")
        subject = data.get("subject")
        auto_respond = data.get("auto_respond", True)

        # Extract additional metadata based on channel
        metadata = {
            "channel_type": channel,
            "timestamp": data.get("timestamp", datetime.now().isoformat()),
        }

        if channel == "form":
            metadata.update(
                {
                    "customer_name": data.get("customer_name"),
                    "category": data.get("category"),
                    "attachment": data.get("attachment"),
                }
            )
        elif channel == "email":
            metadata.update(
                {
                    "attachments": data.get("attachments", []),
                    "email_from": sender,
                    "email_subject": subject,
                    "email_body": message,
                }
            )
        elif channel == "chat":
            metadata.update(
                {"user_id": data.get("user_id"), "session_id": data.get("session_id")}
            )

        # Emit event: Processing started
        emit_event(
            {
                "type": "processing_started",
                "channel": channel,
                "timestamp": datetime.now().isoformat(),
            }
        )

        # Process the query - NLP classification happens automatically
        result = router.process_query(
            channel=channel,
            message=message,
            sender=sender,
            subject=subject,
            auto_respond=auto_respond,
            extra_metadata=metadata,
        )

        # Emit event: Routing completed
        emit_event(
            {
                "type": "routing_completed",
                "ticket_id": result["ticket_id"],
                "team": result["routing"]["final_team"],
                "urgency": result["classification"]["urgency"],
                "timestamp": datetime.now().isoformat(),
            }
        )

        return jsonify({"success": True, "result": result}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/tickets", methods=["GET"])
def get_tickets():
    """Get all tickets, optionally filtered by status."""
    try:
        status = request.args.get("status")
        tickets = router.ticket_manager.get_all_tickets(status)

        response = jsonify({"success": True, "count": len(tickets), "tickets": tickets})

        # Prevent browser caching of tickets
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"

        return response, 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/tickets/<ticket_id>", methods=["GET"])
def get_ticket(ticket_id):
    """Get details for a specific ticket."""
    try:
        ticket_details = router.get_ticket_details(ticket_id)

        if not ticket_details:
            return jsonify({"error": "Ticket not found"}), 404

        return jsonify({"success": True, "ticket": ticket_details}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/tickets/<ticket_id>", methods=["PUT", "PATCH"])
def update_ticket(ticket_id):
    """Update a specific ticket."""
    try:
        data = request.get_json()

        if not data:
            return jsonify({"success": False, "error": "Missing request body"}), 400

        # Check if ticket exists
        ticket = router.ticket_manager.db.get_ticket(ticket_id)
        if not ticket:
            return jsonify({"success": False, "error": "Ticket not found"}), 404

        # Prepare updates - only include allowed fields
        allowed_fields = [
            "status",
            "assigned_team",
            "urgency",
            "intent",
            "message",
            "subject",
            "sender",
            "response",
        ]
        updates = {}

        for field in allowed_fields:
            if field in data:
                updates[field] = data[field]

        # Handle metadata updates
        if "metadata" in data:
            import json

            existing_metadata = json.loads(ticket.get("metadata", "{}") or "{}")
            existing_metadata.update(data["metadata"])
            updates["metadata"] = json.dumps(existing_metadata)

        if not updates:
            return (
                jsonify({"success": False, "error": "No valid fields to update"}),
                400,
            )

        # Update the ticket in database
        router.ticket_manager.db.update_ticket(ticket_id, updates)

        # Verify the update was persisted by fetching the ticket
        updated_ticket = router.ticket_manager.db.get_ticket(ticket_id)

        if not updated_ticket:
            return (
                jsonify({"success": False, "error": "Ticket not found after update"}),
                500,
            )

        # Verify that the updates were actually applied
        verification_failed = []
        for field, value in updates.items():
            if field == "metadata":
                # Metadata is stored as JSON string, so we need to parse it
                import json

                stored_metadata = json.loads(
                    updated_ticket.get("metadata", "{}") or "{}"
                )
                expected_metadata = (
                    json.loads(value) if isinstance(value, str) else value
                )
                if stored_metadata != expected_metadata:
                    verification_failed.append(field)
            else:
                if str(updated_ticket.get(field, "")) != str(value):
                    verification_failed.append(field)

        if verification_failed:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": f"Update verification failed for fields: {', '.join(verification_failed)}",
                        "ticket": dict(updated_ticket),
                    }
                ),
                500,
            )

        # Log the update event
        router.ticket_manager.db.log_routing_event(
            ticket_id,
            "ticket_updated",
            {
                "updated_fields": list(updates.keys()),
                "updates": updates,
                "verified": True,
            },
        )

        return (
            jsonify(
                {
                    "success": True,
                    "message": f"Ticket {ticket_id} updated successfully and verified in database",
                    "ticket": dict(updated_ticket),
                    "updated_fields": list(updates.keys()),
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/tickets/<ticket_id>", methods=["DELETE"])
def delete_ticket(ticket_id):
    """Delete a specific ticket."""
    try:
        # Verify ticket exists before deletion
        ticket = router.ticket_manager.db.get_ticket(ticket_id)
        if not ticket:
            return jsonify({"success": False, "error": "Ticket not found"}), 404

        # Delete the ticket
        success = router.ticket_manager.delete_ticket(ticket_id)

        if not success:
            return jsonify({"success": False, "error": "Failed to delete ticket"}), 500

        # Verify deletion by attempting to fetch the ticket
        deleted_ticket = router.ticket_manager.db.get_ticket(ticket_id)
        if deleted_ticket:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Ticket still exists after deletion - database commit may have failed",
                    }
                ),
                500,
            )

        return (
            jsonify(
                {
                    "success": True,
                    "message": f"Ticket {ticket_id} deleted successfully and verified in database",
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/tickets", methods=["DELETE"])
def delete_all_tickets():
    """Delete all tickets."""
    try:
        # Get count before deletion
        all_tickets = router.ticket_manager.get_all_tickets()
        count = len(all_tickets)

        if count == 0:
            return (
                jsonify(
                    {
                        "success": True,
                        "message": "No tickets to delete",
                        "deleted_count": 0,
                    }
                ),
                200,
            )

        # Delete all tickets
        deleted_count = router.ticket_manager.delete_all_tickets()

        return (
            jsonify(
                {
                    "success": True,
                    "message": f"Successfully deleted {deleted_count} ticket(s)",
                    "deleted_count": deleted_count,
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/stats", methods=["GET"])
def get_stats():
    """Get dashboard statistics."""
    try:
        stats = router.get_dashboard_stats()

        response = jsonify({"success": True, "stats": stats})

        # Prevent browser caching of stats
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"

        return response, 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/export_tickets", methods=["GET"])
def export_tickets():
    """Export tickets to CSV and serve for download."""
    try:
        status = request.args.get("status")
        filename = router.export_tickets(status=status)

        if not filename:
            return jsonify({"success": False, "error": "No tickets to export"}), 404

        # Serve the file for download
        return send_file(
            filename, mimetype="text/csv", as_attachment=True, download_name=filename
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/sample_queries", methods=["GET"])
def get_samples():
    """Get sample queries for testing."""
    try:
        samples = get_sample_queries()

        return (
            jsonify({"success": True, "count": len(samples), "samples": samples}),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/teams", methods=["GET"])
def get_teams():
    """Get all available teams."""
    try:
        teams = router.db.get_teams()

        return jsonify({"success": True, "teams": teams}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/learning/stats", methods=["GET"])
def get_learning_stats():
    """Get learning system statistics."""
    try:
        stats = router.learning_system.get_learning_stats()

        return jsonify({"success": True, "stats": stats}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/learning/analyze", methods=["POST"])
def analyze_learning():
    """Trigger learning analysis on all tickets."""
    try:
        router.learning_system.analyze_and_update_patterns()

        # Refresh classifier with new patterns
        router.classifier.update_from_learning()

        return (
            jsonify(
                {
                    "success": True,
                    "message": "Learning analysis completed and patterns updated",
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/stream_events")
def stream_events():
    """Server-sent events endpoint for real-time routing updates."""

    def event_stream():
        # Subscribe this client
        messages = []
        event_subscribers.append(messages)

        try:
            # Send initial connection message
            yield f"data: {json.dumps({'type': 'connected', 'timestamp': datetime.now().isoformat()})}\n\n"

            # Stream events
            while True:
                if messages:
                    message = messages.pop(0)
                    yield f"data: {json.dumps(message)}\n\n"
                else:
                    # Send heartbeat every 30 seconds
                    yield f": heartbeat\n\n"
                    time.sleep(30)

        finally:
            # Unsubscribe when connection closes
            event_subscribers.remove(messages)

    return Response(
        stream_with_context(event_stream()),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.route("/api/process_batch", methods=["POST"])
def process_batch():
    """Process multiple queries in batch."""
    try:
        data = request.get_json()

        if not data or "queries" not in data:
            return jsonify({"error": "Missing required field: queries"}), 400

        queries = data["queries"]

        # Process batch
        results = router.batch_process(queries)

        return (
            jsonify({"success": True, "count": len(results), "results": results}),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def emit_event(event_data):
    """Emit an event to all subscribed clients."""
    for messages in event_subscribers:
        messages.append(event_data)


@app.route("/health")
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()}), 200


if __name__ == "__main__":
    import sys

    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000

    print("=" * 80)
    print("Multi-Channel Customer Query Router")
    print("=" * 80)
    print(f"Starting Flask application...")
    print(f"Access the web UI at: http://localhost:{port}")
    print(f"API documentation: http://localhost:{port}/api/stats")
    print("=" * 80)

    app.run(debug=True, host="0.0.0.0", port=port, threaded=True)
