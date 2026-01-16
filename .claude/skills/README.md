# Todo Console App Skills

Custom Claude Code skills for managing and developing the Todo Console App.

## Available Skills

### Todo Management Skills

#### `/todo.add` - Add New Todo
Add a new todo item with optional priority, due date, and tags.

**Usage:**
```
/todo.add Buy groceries
/todo.add Finish project report --priority high
/todo.add Review pull requests --due 2025-12-31 --tags work,code-review
```

**Features:**
- Set priority (high/medium/low)
- Add due dates
- Organize with tags
- Input validation

---

#### `/todo.list` - List Todos
Display todos with filtering and sorting options.

**Usage:**
```
/todo.list
/todo.list --status pending
/todo.list --priority high
/todo.list --tags work --sort due
```

**Features:**
- Filter by status (pending/completed)
- Filter by priority
- Filter by tags
- Sort by various criteria
- Visual indicators for status

---

#### `/todo.complete` - Complete Todos
Mark one or more todos as completed.

**Usage:**
```
/todo.complete 5
/todo.complete 3,5,7
/todo.complete --all-pending
/todo.complete 5 --undo
```

**Features:**
- Complete single or multiple todos
- Bulk complete all pending
- Undo completion
- Celebration messages

---

#### `/todo.delete` - Delete Todos
Delete todos permanently or archive them.

**Usage:**
```
/todo.delete 5
/todo.delete 3,5,7
/todo.delete --completed
/todo.delete 5 --archive
/todo.delete --all
```

**Features:**
- Delete single or multiple todos
- Archive instead of permanent delete
- Bulk delete completed todos
- Safety confirmations for destructive operations

---

### Development Skills

#### `/dev.run` - Run the App
Run the todo console app in various modes.

**Usage:**
```
/dev.run
/dev.run --interactive
/dev.run --cli list --status pending
/dev.run --dev
/dev.run --serve --port 8080
```

**Features:**
- Interactive REPL mode
- Direct CLI command execution
- Development mode with hot reload
- Server/daemon mode
- Debug mode
- Custom configuration

---

#### `/dev.test` - Run Tests
Execute tests with various options and coverage.

**Usage:**
```
/dev.test
/dev.test --unit
/dev.test --coverage
/dev.test --watch
/dev.test --file todo.test.js --verbose
```

**Features:**
- Run all or specific test suites
- Unit, integration, and E2E tests
- Coverage reports
- Watch mode for TDD
- Verbose output
- Auto-detect test framework

---

## Skill Categories

### 📝 Todo Operations
- `todo.add` - Create new todos
- `todo.list` - View and filter todos
- `todo.complete` - Mark todos as done
- `todo.delete` - Remove or archive todos

### 🔧 Development
- `dev.run` - Run the application
- `dev.test` - Execute test suites

## How to Use Skills

1. **Invoke a skill** by typing `/` followed by the skill name:
   ```
   /todo.add Buy milk
   ```

2. **Pass arguments** after the skill name:
   ```
   /todo.list --status pending --priority high
   ```

3. **Use handoffs** - skills can suggest related skills:
   - After adding a todo, you might be prompted to list all todos
   - After running tests, you might be prompted to run the app

## Notes

- Skills adapt to your implementation (file-based, database, etc.)
- All skills include validation and error handling
- Interactive prompts guide you when arguments are unclear
- Skills integrate with the SDD workflow (spec, plan, tasks)

## Next Steps

If you haven't built the Todo Console App yet:

1. Create the specification: `/sp.specify Build a todo console app with add, list, complete, and delete features`
2. Generate the plan: `/sp.plan`
3. Create tasks: `/sp.tasks`
4. Implement: `/sp.implement`

Then use these skills to interact with your app!

## Future Enhancements

Potential additional skills to create:
- `todo.search` - Search todos by keyword
- `todo.edit` - Edit existing todos
- `todo.stats` - Show productivity statistics
- `todo.export` - Export todos to various formats
- `todo.import` - Import todos from files
- `dev.build` - Build and package the app
- `dev.deploy` - Deploy the application
- `dev.lint` - Run code quality checks
