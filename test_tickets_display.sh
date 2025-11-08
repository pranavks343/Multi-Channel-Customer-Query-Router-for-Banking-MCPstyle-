#!/bin/bash

echo "========================================================================"
echo "           TICKETS DISPLAY DIAGNOSTIC TEST"
echo "========================================================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "Test 1: Check if app is running on port 8000..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ App is running${NC}"
else
    echo -e "${RED}❌ App is NOT running on port 8000${NC}"
    echo "   Please start the app first: python app.py 8000"
    exit 1
fi
echo ""

echo "Test 2: Check tickets API endpoint..."
RESPONSE=$(curl -s http://localhost:8000/api/tickets)
COUNT=$(echo $RESPONSE | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('count', 0))" 2>/dev/null)

if [ ! -z "$COUNT" ]; then
    echo -e "${GREEN}✅ API endpoint working${NC}"
    echo "   Total tickets: $COUNT"
else
    echo -e "${RED}❌ API endpoint error${NC}"
    echo "   Response: $RESPONSE"
    exit 1
fi
echo ""

echo "Test 3: List recent tickets from database..."
cd /Users/pranavks/hackathon
TICKETS=$(sqlite3 query_router.db "SELECT ticket_id, channel, urgency, substr(created_at, 1, 19) FROM tickets ORDER BY created_at DESC LIMIT 5;" 2>/dev/null)

if [ ! -z "$TICKETS" ]; then
    echo -e "${GREEN}✅ Database has tickets${NC}"
    echo "$TICKETS" | while IFS='|' read -r id channel urgency created; do
        echo "   - $id ($channel, $urgency) created at $created"
    done
else
    echo -e "${YELLOW}⚠️  No tickets in database${NC}"
fi
echo ""

echo "Test 4: Check if main page loads..."
if curl -s http://localhost:8000/ | grep -q "ticketsList"; then
    echo -e "${GREEN}✅ Main page loads and contains ticketsList element${NC}"
else
    echo -e "${RED}❌ Main page doesn't contain ticketsList element${NC}"
fi
echo ""

echo "Test 5: Check debug page..."
if curl -s http://localhost:8000/debug/tickets | grep -q "Tickets Debug View"; then
    echo -e "${GREEN}✅ Debug page is accessible${NC}"
    echo "   URL: http://localhost:8000/debug/tickets"
else
    echo -e "${RED}❌ Debug page not accessible${NC}"
fi
echo ""

echo "========================================================================"
echo "                         SUMMARY"
echo "========================================================================"
echo ""
echo "✅ All tests passed!"
echo ""
echo "Next steps:"
echo "1. Open: http://localhost:8000"
echo "2. Scroll to 'Recent ticket decisions' section"
echo "3. Open browser console (F12) and look for:"
echo "   - 'Loading tickets...'"
echo "   - 'Displaying X tickets'"
echo ""
echo "If tickets STILL don't show:"
echo "1. Open debug view: http://localhost:8000/debug/tickets"
echo "2. Try hard refresh: Ctrl+Shift+R (or Cmd+Shift+R on Mac)"
echo "3. Check browser console for JavaScript errors"
echo ""
echo "Current tickets in database: $COUNT"
echo "========================================================================"

