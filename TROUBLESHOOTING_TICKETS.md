# Troubleshooting: Recent Tickets Not Showing

## Issue
Recent tickets not appearing in the "Recent ticket decisions" section on the main page.

## Root Cause Analysis
The tickets ARE being properly:
✅ Saved to the database  
✅ Returned by the API endpoint (`/api/tickets`)  
✅ Ordered correctly (most recent first)  

The issue is likely one of these:
1. **Browser Cache** - Old JavaScript/CSS cached
2. **JavaScript Error** - Console errors preventing rendering
3. **CSS Issue** - Tickets rendered but not visible
4. **Element Not Found** - DOM element missing

## Solutions

### Solution 1: Check Debug Page (RECOMMENDED)
1. Open: **http://localhost:8000/debug/tickets**
2. This page shows all tickets with auto-refresh every 5 seconds
3. If tickets appear here, the API is working correctly

### Solution 2: Clear Browser Cache
1. Open the main app: http://localhost:8000
2. Open browser DevTools (F12 or Cmd+Option+I on Mac)
3. Hard refresh:
   - **Chrome/Edge**: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
   - **Firefox**: Ctrl+F5 (Windows) or Cmd+Shift+R (Mac)
   - **Safari**: Cmd+Option+R
4. Or right-click refresh button → "Empty Cache and Hard Reload"

### Solution 3: Check Browser Console
1. Open browser DevTools (F12)
2. Go to **Console** tab
3. Look for these messages when page loads:
   ```
   Loading tickets...
   Tickets API response: {success: true, count: 14, ...}
   Displaying 14 tickets
   displayTickets called with 14 tickets
   Setting innerHTML with 10 tickets
   ```

4. **If you see errors:**
   - Red error messages → JavaScript issue
   - "ticketsList element not found" → DOM issue
   - "Fetch failed" → API connection issue

### Solution 4: Check Network Tab
1. Open DevTools → **Network** tab
2. Reload the page
3. Look for `/api/tickets` request
4. Click on it to see:
   - **Status:** Should be 200
   - **Response:** Should show tickets array
   - **Headers:** Should show `Content-Type: application/json`

### Solution 5: Verify Tickets Panel Exists
1. Open DevTools → **Elements** tab
2. Press Ctrl+F (Cmd+F on Mac) to search
3. Search for: `id="ticketsList"`
4. Should find: `<div class="tickets-list" id="ticketsList"></div>`
5. If not found → HTML structure issue

### Solution 6: Check CSS Display
If tickets panel exists but is empty:
1. In DevTools → **Elements** tab
2. Find the tickets panel
3. Check computed styles:
   - `display` should not be `none`
   - `visibility` should not be `hidden`
   - `opacity` should not be `0`

### Solution 7: Manual Refresh Button
1. Scroll to "Recent ticket decisions" section
2. Click the **"Refresh tickets"** button
3. Check console for logs

### Solution 8: Submit a New Test Query
1. Use the query form to submit a new test query
2. After submission, check if it appears in tickets list
3. If it appears, older tickets should also be visible

## Testing the Fix

### Quick Test Commands

```bash
# Test 1: Verify API returns tickets
curl http://localhost:8000/api/tickets

# Test 2: Count tickets in database
cd /Users/pranavks/hackathon
sqlite3 query_router.db "SELECT COUNT(*) FROM tickets;"

# Test 3: Show latest 5 tickets
sqlite3 query_router.db "SELECT ticket_id, created_at FROM tickets ORDER BY created_at DESC LIMIT 5;"
```

### Test in Browser

```javascript
// Paste in browser console:

// Test 1: Manual API call
fetch('/api/tickets')
  .then(r => r.json())
  .then(d => console.log('Tickets:', d));

// Test 2: Check if element exists
console.log('ticketsList element:', document.getElementById('ticketsList'));

// Test 3: Manual load
loadTickets();

// Test 4: Check tickets after 2 seconds
setTimeout(() => {
  console.log('Tickets HTML:', document.getElementById('ticketsList').innerHTML.substring(0, 200));
}, 2000);
```

## Expected Behavior

When working correctly, you should see:

1. **On Page Load:**
   - Tickets section shows up to 10 most recent tickets
   - Each ticket shows: ID, urgency badge, message, channel, team, intent

2. **After Submitting New Query:**
   - New ticket appears at the top of the list
   - Stats update automatically
   - Live activity stream shows routing event

3. **After Clicking Refresh:**
   - Tickets reload from API
   - Most recent tickets appear first

## Files Modified

✅ `app.py` - Added `/debug/tickets` route  
✅ `templates/index.html` - Added console logging  
✅ `templates/debug_tickets.html` - New debug page  

## Verification Steps

1. ✅ Database has tickets (confirmed via SQL query)
2. ✅ API returns tickets (confirmed via curl)
3. ✅ Tickets are ordered correctly (DESC by created_at)
4. ✅ JavaScript functions exist (loadTickets, displayTickets)
5. ✅ CSS styles are correct (ticket-item styling)
6. ⚠️ **Need to verify:** Browser rendering

## Next Steps

1. **Visit debug page:** http://localhost:8000/debug/tickets
   - If tickets show here → Browser cache issue
   - If tickets don't show → API issue

2. **Check browser console** for error messages

3. **Try hard refresh** (Ctrl+Shift+R or Cmd+Shift+R)

4. **If still not working:**
   - Take screenshot of browser console
   - Take screenshot of Network tab showing /api/tickets request
   - Check if tickets appear in debug page

## Recent Enhancements

- ✅ Added console.log statements for debugging
- ✅ Added element existence check
- ✅ Added detailed logging of ticket count
- ✅ Created dedicated debug page
- ✅ Fixed urgency badge (added toUpperCase())

## Success Indicators

✅ Console shows: "Loading tickets..."  
✅ Console shows: "Tickets API response: {success: true, count: X}"  
✅ Console shows: "displayTickets called with X tickets"  
✅ Console shows: "Setting innerHTML with X tickets"  
✅ Tickets panel shows ticket cards  
✅ Each ticket has ID, urgency badge, message, meta info  

## Contact Info for Further Help

If the issue persists after trying all solutions:

1. Capture browser console output
2. Check http://localhost:8000/debug/tickets
3. Run test commands above
4. Share results for further diagnosis

