# Full-Stack Todo Application - Testing Guide

## Server Status

✅ **Backend**: Running on http://localhost:8001
✅ **Frontend**: Running on http://localhost:3000

## Testing Checklist

### 1. Authentication Flow

#### User Registration
- [ ] Navigate to http://localhost:3000/register
- [ ] Enter email: `test@example.com`
- [ ] Enter password: `Test123456`
- [ ] Click "Register"
- [ ] Verify: Redirected to todos page
- [ ] Verify: User is logged in

#### User Login
- [ ] Navigate to http://localhost:3000/login
- [ ] Enter registered email and password
- [ ] Click "Login"
- [ ] Verify: Redirected to todos page
- [ ] Verify: JWT token stored (check browser DevTools → Application → Local Storage)

#### Session Persistence
- [ ] While logged in, refresh the page (F5)
- [ ] Verify: Still logged in, todos page loads
- [ ] Verify: No redirect to login page

#### User Logout
- [ ] Click "Logout" button in header
- [ ] Verify: Redirected to login page
- [ ] Verify: JWT token removed from storage
- [ ] Try accessing http://localhost:3000/todos directly
- [ ] Verify: Redirected to login page

### 2. Basic CRUD Operations

#### Create Todo
- [ ] Log in to the application
- [ ] Enter todo title: "Test Todo 1"
- [ ] Enter description: "This is a test todo"
- [ ] Click "Add Todo"
- [ ] Verify: Todo appears at top of list
- [ ] Verify: Todo shows as incomplete (unchecked)

#### Read/View Todos
- [ ] Create multiple todos (at least 5)
- [ ] Verify: All todos display in the list
- [ ] Verify: Todos sorted by creation date (newest first)
- [ ] Verify: Each todo shows title, description, and status

#### Update Todo
- [ ] Click "Edit" button on a todo
- [ ] Change title to "Updated Todo"
- [ ] Change description to "Updated description"
- [ ] Click "Save"
- [ ] Verify: Changes persist immediately
- [ ] Refresh page
- [ ] Verify: Changes still visible

#### Complete/Uncomplete Todo
- [ ] Click checkbox next to an incomplete todo
- [ ] Verify: Todo marked as complete (visual change)
- [ ] Click checkbox again
- [ ] Verify: Todo marked as incomplete
- [ ] Refresh page
- [ ] Verify: Status persists

#### Delete Todo
- [ ] Click "Delete" button on a todo
- [ ] Verify: Confirmation modal appears
- [ ] Click "Cancel"
- [ ] Verify: Todo still exists
- [ ] Click "Delete" again
- [ ] Click "Confirm"
- [ ] Verify: Todo removed from list
- [ ] Refresh page
- [ ] Verify: Todo still deleted

### 3. Phase 2 Features - Priority

#### Set Priority on Create
- [ ] Create new todo with title "High Priority Task"
- [ ] Select "High" from priority dropdown
- [ ] Click "Add Todo"
- [ ] Verify: Todo shows red "High Priority" badge

#### Set Priority on Edit
- [ ] Edit an existing todo
- [ ] Change priority to "Low"
- [ ] Click "Save"
- [ ] Verify: Todo shows green "Low Priority" badge

#### Sort by Priority
- [ ] Create todos with different priorities (High, Medium, Low)
- [ ] Select "Priority (High to Low)" from sort dropdown
- [ ] Verify: High priority todos appear first
- [ ] Verify: Low priority todos appear last

### 4. Phase 2 Features - Due Dates

#### Set Due Date on Create
- [ ] Create new todo with title "Task with deadline"
- [ ] Select a future date from due date picker
- [ ] Click "Add Todo"
- [ ] Verify: Todo shows due date badge

#### Set Past Due Date (Overdue)
- [ ] Create new todo with title "Overdue task"
- [ ] Select a past date (e.g., yesterday)
- [ ] Click "Add Todo"
- [ ] Verify: Todo shows red badge with ⚠️ warning
- [ ] Verify: Badge says "Due: [date]"

#### Sort by Due Date
- [ ] Create multiple todos with different due dates
- [ ] Select "Due Date (Earliest First)" from sort dropdown
- [ ] Verify: Todos with earliest dates appear first
- [ ] Verify: Todos without due dates appear last

### 5. Phase 2 Features - Tags

#### Create Tags
- [ ] Scroll to "Manage Tags" section
- [ ] Enter tag name: "Work"
- [ ] Select a color (e.g., blue)
- [ ] Click "Add Tag"
- [ ] Verify: Tag appears in tag list
- [ ] Create more tags: "Personal", "Urgent"

#### Assign Tags to Todo (Create)
- [ ] Create new todo
- [ ] Click on tags to select them (should show checkmark)
- [ ] Click "Add Todo"
- [ ] Verify: Todo displays selected tags with custom colors

#### Assign Tags to Todo (Edit)
- [ ] Edit an existing todo
- [ ] Select/deselect tags
- [ ] Click "Save"
- [ ] Verify: Tag changes persist

#### Delete Tag
- [ ] Click "×" button on a tag in tag management
- [ ] Verify: Tag removed from list
- [ ] Verify: Tag removed from all todos that had it

### 6. Filtering and Sorting

#### Filter by Status
- [ ] Create mix of complete and incomplete todos
- [ ] Click "Active" filter button
- [ ] Verify: Only incomplete todos shown
- [ ] Click "Completed" filter button
- [ ] Verify: Only completed todos shown
- [ ] Click "All" filter button
- [ ] Verify: All todos shown

#### Sort Options
- [ ] Test "Newest First" - verify newest at top
- [ ] Test "Oldest First" - verify oldest at top
- [ ] Test "Title (A-Z)" - verify alphabetical order
- [ ] Test "Title (Z-A)" - verify reverse alphabetical

### 7. Search Functionality

#### Search by Title
- [ ] Create todos with distinct titles
- [ ] Enter search term in search box
- [ ] Verify: Only matching todos shown
- [ ] Clear search
- [ ] Verify: All todos shown again

#### Search by Description
- [ ] Enter search term that matches a description
- [ ] Verify: Todos with matching descriptions shown

### 8. Pagination

#### Test Pagination
- [ ] Create 25+ todos
- [ ] Verify: Pagination controls appear
- [ ] Verify: Shows "Page 1 of 2" (or similar)
- [ ] Click "Next" button
- [ ] Verify: Page 2 loads with remaining todos
- [ ] Click "Previous" button
- [ ] Verify: Returns to page 1

### 9. Error Handling

#### Invalid Login
- [ ] Try logging in with wrong password
- [ ] Verify: Error message displayed
- [ ] Verify: Not logged in

#### Empty Todo Title
- [ ] Try creating todo with empty title
- [ ] Verify: Validation error or button disabled

#### Network Error Simulation
- [ ] Stop backend server
- [ ] Try creating a todo
- [ ] Verify: Error message displayed
- [ ] Restart backend server

### 10. Data Isolation

#### Multi-User Test
- [ ] Register user 1: `user1@test.com`
- [ ] Create 3 todos for user 1
- [ ] Logout
- [ ] Register user 2: `user2@test.com`
- [ ] Verify: User 2 sees empty todo list
- [ ] Create 2 todos for user 2
- [ ] Logout and login as user 1
- [ ] Verify: User 1 only sees their 3 todos
- [ ] Verify: User 1 cannot see user 2's todos

## API Testing (Backend)

### Health Check
```bash
curl http://localhost:8001/api/health
```
Expected: `{"status":"ok","timestamp":"...","version":"1.0.0"}`

### Register User
```bash
curl -X POST http://localhost:8001/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"api-test@example.com","password":"Test123456"}'
```
Expected: `{"access_token":"...","token_type":"bearer"}`

### Login User
```bash
curl -X POST http://localhost:8001/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"api-test@example.com","password":"Test123456"}'
```
Expected: `{"access_token":"...","token_type":"bearer"}`

### Get Todos (Authenticated)
```bash
curl http://localhost:8001/api/v1/todos \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```
Expected: `{"todos":[],"total":0,"page":1,"page_size":50,"total_pages":1}`

## Performance Testing

### Load Time
- [ ] Open DevTools → Network tab
- [ ] Load http://localhost:3000/todos
- [ ] Verify: Page loads in < 3 seconds
- [ ] Verify: No console errors

### Large Dataset
- [ ] Create 100+ todos (can use API script)
- [ ] Verify: Page still loads smoothly
- [ ] Verify: Pagination works correctly
- [ ] Verify: Scrolling is smooth

## Browser Compatibility

Test in multiple browsers:
- [ ] Chrome/Edge (Chromium)
- [ ] Firefox
- [ ] Safari (if on Mac)

## Mobile Responsiveness

- [ ] Open DevTools → Toggle device toolbar
- [ ] Test at 320px width (mobile)
- [ ] Test at 768px width (tablet)
- [ ] Test at 1920px width (desktop)
- [ ] Verify: UI adapts to all screen sizes
- [ ] Verify: All buttons are tappable
- [ ] Verify: No horizontal scrolling

## Deployment Readiness Checklist

### Backend (Hugging Face Spaces)
- [ ] All environment variables documented
- [ ] Database migrations working
- [ ] Health endpoint responding
- [ ] CORS configured for frontend domain
- [ ] No hardcoded secrets in code

### Frontend (Vercel)
- [ ] Environment variables documented
- [ ] API URL configurable
- [ ] Build succeeds without errors
- [ ] No TypeScript errors
- [ ] All pages load correctly

## Issues Found

Document any issues discovered during testing:

1. **Issue**: [Description]
   - **Severity**: Critical/High/Medium/Low
   - **Steps to Reproduce**: [Steps]
   - **Expected**: [Expected behavior]
   - **Actual**: [Actual behavior]

## Test Results Summary

- **Total Tests**: [Number]
- **Passed**: [Number]
- **Failed**: [Number]
- **Blocked**: [Number]

**Overall Status**: ✅ Ready for Deployment / ⚠️ Issues Found / ❌ Not Ready

---

**Last Updated**: 2026-01-15
**Tested By**: [Your Name]
**Environment**: Local Development (localhost)
