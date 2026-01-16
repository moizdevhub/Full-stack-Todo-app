---
description: Add a new todo item to the list with optional priority and due date
handoffs:
  - label: List all todos
    agent: todo.list
    prompt: Show me all todos
  - label: Run the app
    agent: dev.run
    prompt: Run the todo console app
---

## User Input

```text
$ARGUMENTS
```

## Task

Add a new todo item to the todo list application.

### Input Processing

1. **Parse the user input** from `$ARGUMENTS`:
   - Todo description (required)
   - Priority flag: `--priority high|medium|low` (optional, default: medium)
   - Due date: `--due YYYY-MM-DD` (optional)
   - Tags: `--tags tag1,tag2` (optional)

2. **Validation**:
   - Ensure todo description is not empty
   - If priority specified, validate it's one of: high, medium, low
   - If due date specified, validate format and ensure it's not in the past
   - Sanitize input to prevent any injection issues

### Implementation Steps

1. **Determine the implementation approach**:
   - Check if todo storage file exists (e.g., `todos.json`, `todos.txt`, or database)
   - If app code exists, use existing add functionality
   - If no implementation exists, guide user to create one first using `/sp.specify`

2. **Add the todo**:
   - If CLI exists: Run the app's add command with parsed parameters
   - If module exists: Import and call the add function programmatically
   - If JSON file: Read, append, write back with proper formatting
   - Assign unique ID (timestamp or incremental)

3. **Verify success**:
   - Confirm the todo was added successfully
   - Display the added todo with its ID and details
   - Show total count of todos

### Output Format

Display the result in this format:

```
✓ Todo added successfully!

ID: [generated-id]
Description: [todo description]
Priority: [high|medium|low]
Due: [date or "No due date"]
Tags: [tags or "None"]
Created: [timestamp]

Total todos: [count]
```

### Error Handling

- If todo description is missing: "Error: Todo description is required"
- If storage is not initialized: "Error: Todo storage not found. Please run the app initialization first."
- If validation fails: "Error: [specific validation message]"
- Suggest using `/sp.specify` if the app doesn't exist yet

### Examples

**Simple todo:**
```
/todo.add Buy groceries
```

**Todo with priority:**
```
/todo.add Finish project report --priority high
```

**Todo with due date and tags:**
```
/todo.add Review pull requests --due 2025-12-31 --tags work,code-review --priority medium
```

## Notes

- This skill assumes a todo app implementation exists
- If the app is not yet built, guide the user to create the spec first
- Adapt to whatever storage mechanism the app uses (file, database, etc.)
- Always validate and sanitize user input
