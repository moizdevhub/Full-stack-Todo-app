---
description: Mark one or more todo items as completed
handoffs:
  - label: List all todos
    agent: todo.list
    prompt: Show me all todos
  - label: Add new todo
    agent: todo.add
    prompt: Add a new todo
---

## User Input

```text
$ARGUMENTS
```

## Task

Mark todo item(s) as completed in the todo list application.

### Input Processing

1. **Parse the user input** from `$ARGUMENTS`:
   - Todo ID(s) (required): Single ID or comma-separated list (e.g., "5" or "3,5,7")
   - Bulk complete: `--all-pending` to complete all pending todos (use with caution)
   - Undo: `--undo` to mark completed todos as pending again

2. **Validation**:
   - Ensure at least one ID is provided (or --all-pending flag)
   - Validate ID format (numeric or UUID depending on implementation)
   - Confirm todos exist before completing

### Implementation Steps

1. **Determine the data source**:
   - Check if todo storage exists
   - If app code exists, use existing complete functionality
   - If no implementation exists, guide user to create one first

2. **Complete the todo(s)**:
   - If CLI exists: Run the app's complete command with ID(s)
   - If module exists: Import and call the complete function programmatically
   - If JSON file: Read, update status and completion timestamp, write back
   - Validate each ID exists before updating
   - Record completion timestamp

3. **Provide feedback**:
   - List completed todo(s) with their descriptions
   - Show remaining pending todos count
   - Celebrate completion with positive message

### Output Format

**Single todo completed:**
```
✓ Todo completed!

[ID] [Description]
Completed: [timestamp]

Remaining pending todos: [count]
```

**Multiple todos completed:**
```
✓ [N] todos completed!

✓ [ID] [Description]
✓ [ID] [Description]
✓ [ID] [Description]

Completed: [timestamp]
Remaining pending todos: [count]
```

**All pending completed:**
```
🎉 All pending todos completed!

Completed [N] todos:
✓ [ID] [Description]
✓ [ID] [Description]
...

Great job! Your todo list is clear.
```

### Error Handling

- If no ID provided: "Error: Please specify a todo ID (e.g., `/todo.complete 5`)"
- If ID doesn't exist: "Error: Todo [ID] not found"
- If todo already completed: "Todo [ID] is already completed. Use `--undo` to reopen it."
- If storage doesn't exist: "Error: Todo storage not found"
- If app not implemented: Guide user to use `/sp.specify`

### Interactive Mode

If ID is not provided, offer to show pending todos and ask which to complete:

```
Which todo would you like to complete?

Pending todos:
1. Buy groceries (ID: 5)
2. Finish project report (ID: 7)
3. Call dentist (ID: 9)

Reply with the ID or number to complete, or 'all' to complete all pending todos.
```

### Examples

**Complete single todo:**
```
/todo.complete 5
```

**Complete multiple todos:**
```
/todo.complete 3,5,7
```

**Complete all pending todos:**
```
/todo.complete --all-pending
```

**Undo completion (mark as pending):**
```
/todo.complete 5 --undo
```

**Interactive completion:**
```
/todo.complete
[Shows pending todos and prompts for selection]
```

## Notes

- Always confirm before bulk operations (--all-pending)
- Record completion timestamp for analytics
- Consider adding completion notes/comments in future versions
- Support undo functionality to reopen completed todos
- Celebrate user achievements with positive messages
