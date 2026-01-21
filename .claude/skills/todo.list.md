---
description: Display all todos or filter by status, priority, or tags
handoffs:
  - label: Add new todo
    agent: todo.add
    prompt: Add a new todo
  - label: Complete a todo
    agent: todo.complete
    prompt: Mark todo as complete
  - label: Delete a todo
    agent: todo.delete
    prompt: Delete a todo
---

## User Input

```text
$ARGUMENTS
```

## Task

Display todos from the todo list application with optional filtering and sorting.

### Input Processing

1. **Parse the user input** from `$ARGUMENTS`:
   - Filter by status: `--status all|pending|completed` (optional, default: all)
   - Filter by priority: `--priority high|medium|low` (optional)
   - Filter by tags: `--tags tag1,tag2` (optional)
   - Sort by: `--sort priority|due|created` (optional, default: created)
   - Limit results: `--limit N` (optional)

2. **Validation**:
   - Validate status values if provided
   - Validate priority values if provided
   - Validate sort options if provided

### Implementation Steps

1. **Determine the data source**:
   - Check if todo storage exists (e.g., `todos.json`, database)
   - If app code exists, use existing list functionality
   - If no implementation exists, guide user to create one first

2. **Retrieve and filter todos**:
   - If CLI exists: Run the app's list command with parsed filters
   - If module exists: Import and call the list function programmatically
   - If JSON file: Read and filter the data
   - Apply all requested filters (status, priority, tags)
   - Sort according to requested order

3. **Format and display**:
   - Group by status if showing all
   - Use clear visual indicators (✓ for completed, ○ for pending, ⚠ for high priority)
   - Show relevant metadata (due date, priority, tags)
   - Display summary statistics

### Output Format

Display the result in this format:

```
📋 Todo List

[Status Group - if applicable]
─────────────────────────────────────────

○ [ID] [Description]
  Priority: [high|medium|low] | Due: [date or "None"] | Tags: [tags]
  Created: [date]

✓ [ID] [Description]
  Priority: [high|medium|low] | Completed: [date]
  Created: [date]

─────────────────────────────────────────
Summary:
  Total: [count]
  Pending: [count]
  Completed: [count]
  Overdue: [count]
```

### Special Display Modes

**By Priority (high priority first):**
```
⚠ High Priority ([count])
  [todos]

○ Medium Priority ([count])
  [todos]

○ Low Priority ([count])
  [todos]
```

**Compact Mode (for large lists):**
```
[ID] [Status] [Description] (Priority: [X], Due: [date])
```

### Error Handling

- If storage doesn't exist: "No todos found. Add your first todo with `/todo.add`"
- If no todos match filters: "No todos found matching your filters"
- If app not implemented: Guide user to use `/sp.specify` to create the app spec

### Examples

**List all todos:**
```
/todo.list
```

**List only pending todos:**
```
/todo.list --status pending
```

**List high priority todos:**
```
/todo.list --priority high
```

**List todos with specific tag:**
```
/todo.list --tags work
```

**List pending todos sorted by due date:**
```
/todo.list --status pending --sort due
```

## Notes

- Adapt to whatever storage mechanism the app uses
- Consider pagination for large todo lists (use --limit)
- Highlight overdue items in red if possible
- Show relative dates for better UX (e.g., "Due tomorrow", "Overdue by 3 days")
