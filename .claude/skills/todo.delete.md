---
description: Delete one or more todo items permanently or archive completed todos
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

Delete todo item(s) from the todo list application.

### Input Processing

1. **Parse the user input** from `$ARGUMENTS`:
   - Todo ID(s) (required): Single ID or comma-separated list (e.g., "5" or "3,5,7")
   - Bulk operations:
     - `--completed` to delete all completed todos
     - `--all` to delete ALL todos (requires confirmation)
   - Archive mode: `--archive` to move to archive instead of permanent delete
   - Force: `--force` to skip confirmation prompts

2. **Validation**:
   - Ensure at least one ID is provided (or bulk flag)
   - Validate ID format
   - Confirm todos exist before deleting

### Implementation Steps

1. **Determine the data source**:
   - Check if todo storage exists
   - If app code exists, use existing delete functionality
   - If no implementation exists, guide user to create one first

2. **Confirmation (unless --force)**:
   - Show todo details before deletion
   - Ask for explicit confirmation for destructive operations
   - **Always confirm** before `--all` flag

3. **Delete or archive the todo(s)**:
   - If `--archive`: Move to archive file/table instead of deleting
   - If permanent delete:
     - If CLI exists: Run the app's delete command with ID(s)
     - If module exists: Import and call the delete function
     - If JSON file: Read, filter out items, write back
   - Keep archive history with deletion timestamp if archiving

4. **Provide feedback**:
   - Confirm deletion/archival
   - Show remaining todos count
   - Warn about permanent deletion

### Output Format

**Single todo deleted:**
```
⚠ Todo deleted permanently!

[ID] [Description]
Status: [completed/pending]

Remaining todos: [count]
```

**Multiple todos deleted:**
```
⚠ [N] todos deleted permanently!

Deleted:
  [ID] [Description]
  [ID] [Description]
  [ID] [Description]

Remaining todos: [count]
```

**Archived instead of deleted:**
```
📦 Todo archived successfully!

[ID] [Description]
Archived: [timestamp]

You can restore archived todos later.
Remaining active todos: [count]
```

**Bulk delete completed todos:**
```
⚠ Deleting all completed todos ([N] items)

Are you sure? This cannot be undone. (y/N): [wait for confirmation]

[After confirmation]
✓ [N] completed todos deleted
Remaining todos: [count]
```

### Confirmation Prompts

**Delete single todo:**
```
You are about to delete:
  [ID] [Description]

This action cannot be undone.
Continue? (y/N):
```

**Delete all todos:**
```
⚠ WARNING: You are about to delete ALL todos ([N] items)

This will permanently delete:
  - [N] pending todos
  - [N] completed todos

This action CANNOT be undone!
Type 'DELETE ALL' to confirm:
```

### Error Handling

- If no ID provided: "Error: Please specify a todo ID (e.g., `/todo.delete 5`)"
- If ID doesn't exist: "Error: Todo [ID] not found"
- If user cancels confirmation: "Deletion cancelled"
- If storage doesn't exist: "Error: Todo storage not found"
- If app not implemented: Guide user to use `/sp.specify`

### Interactive Mode

If ID is not provided, offer to show todos and ask which to delete:

```
Which todo would you like to delete?

Your todos:
1. Buy groceries (ID: 5, pending)
2. Finish project report (ID: 7, completed)
3. Call dentist (ID: 9, pending)

Reply with the ID or number to delete.
```

### Examples

**Delete single todo:**
```
/todo.delete 5
```

**Delete multiple todos:**
```
/todo.delete 3,5,7
```

**Delete all completed todos:**
```
/todo.delete --completed
```

**Archive instead of delete:**
```
/todo.delete 5 --archive
```

**Force delete without confirmation:**
```
/todo.delete 5 --force
```

**Delete all todos (dangerous):**
```
/todo.delete --all
[Requires typing 'DELETE ALL' to confirm]
```

## Notes

- **Always confirm destructive operations** unless --force is used
- Prefer archiving over permanent deletion for audit trail
- Consider implementing soft delete with trash/restore functionality
- Keep deletion logs for accountability
- Warn users about permanent deletion clearly
- Never delete without user consent for bulk operations
- Consider retention policies for archived items
