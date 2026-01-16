---
description: Run the todo console app in various modes (interactive, CLI, dev server)
handoffs:
  - label: Run tests
    agent: dev.test
    prompt: Run tests for the app
  - label: Add todo via app
    agent: todo.add
    prompt: Add a new todo
---

## User Input

```text
$ARGUMENTS
```

## Task

Run the Todo Console App in different modes with various options.

### Input Processing

1. **Parse the user input** from `$ARGUMENTS`:
   - Run mode:
     - `--interactive` or `-i` for interactive mode (default)
     - `--cli` for direct CLI command execution
     - `--dev` for development mode with hot reload
     - `--serve` to start as a server/daemon
   - Configuration:
     - `--config <file>` to specify config file
     - `--port <number>` for server mode
     - `--debug` for debug output
     - `--no-color` to disable colored output
   - Quick commands (when --cli):
     - `list`, `add`, `complete`, `delete` followed by arguments

2. **Auto-detect entry point**:
   - Check for main entry file (main.py, index.js, main.go, etc.)
   - Look for package.json "start" script
   - Check for compiled binary
   - Detect language/runtime needed

### Implementation Steps

1. **Detect app setup**:
   - Find main application file or entry point
   - Check if dependencies are installed
   - Verify configuration files exist
   - If no app exists, guide user to create spec and implement first

2. **Prepare runtime environment**:
   - Set environment variables (ENV=development, etc.)
   - Load configuration from files
   - Initialize logging level based on --debug flag
   - Check for required dependencies

3. **Run the application**:
   - **Interactive mode**: Launch full interactive CLI interface
   - **CLI mode**: Execute single command and exit
   - **Dev mode**: Run with file watching and auto-reload
   - **Server mode**: Start background process/daemon
   - Capture output and errors appropriately

4. **Monitor and report**:
   - Display startup confirmation
   - Show any initialization errors
   - Provide usage instructions for interactive mode
   - Log runtime errors with helpful context

### Output Format

**Interactive mode startup:**
```
🚀 Starting Todo Console App...

Environment: development
Config: ./config.json
Storage: ./data/todos.json

─────────────────────────────────────────
Todo Console App v1.0.0
─────────────────────────────────────────

Commands:
  add <description>      Add a new todo
  list [filters]         List todos
  complete <id>          Complete a todo
  delete <id>           Delete a todo
  help                  Show this help
  exit                  Exit the app

> [waiting for input]
```

**CLI mode (direct command):**
```
/dev.run --cli list --status pending

📋 Pending Todos (3)

○ 1. Buy groceries
○ 2. Finish project report
○ 3. Call dentist
```

**Dev mode (with file watching):**
```
🔧 Starting in development mode...

Watching: src/**/*.js
Server: http://localhost:3000
Debug: enabled

[Nodemon] starting `node src/index.js`
[Nodemon] App started on port 3000
[Nodemon] Watching for file changes...

Press Ctrl+C to stop
```

**Server mode:**
```
🌐 Starting Todo Console App server...

Server: http://localhost:8080
PID: 12345
Logs: ./logs/app.log

Server started successfully!
Access at: http://localhost:8080

To stop: kill 12345
```

### Framework-Specific Commands

**Python:**
```bash
python main.py [args]
python -m todo [args]
```

**Node.js:**
```bash
node index.js [args]
npm start
npm run dev
```

**Go:**
```bash
go run main.go [args]
./todo-app [args]
```

**Java:**
```bash
java -jar todo-app.jar [args]
mvn exec:java
```

### Error Handling

- If entry point not found: "Error: Main application file not found. Expected main.py, index.js, or similar."
- If dependencies missing: "Error: Dependencies not installed. Run `npm install` or `pip install -r requirements.txt`"
- If app not implemented: "The app hasn't been built yet. Use `/sp.specify` to create the specification first."
- If port already in use: "Error: Port [port] is already in use. Try a different port with --port [number]"
- If runtime errors: Display error with stack trace and suggest fixes

### Interactive Mode Features

When running in interactive mode, support:

1. **Command completion**: Tab to autocomplete commands
2. **Command history**: Up/down arrows to navigate history
3. **Multi-line input**: For long todo descriptions
4. **Colored output**: Visual distinction for different message types
5. **Help system**: Built-in help for all commands
6. **Graceful exit**: Ctrl+C or 'exit' command

### Examples

**Run in interactive mode (default):**
```
/dev.run
```

**Run with debug output:**
```
/dev.run --debug
```

**Execute single CLI command:**
```
/dev.run --cli list --status pending
```

**Start development server with hot reload:**
```
/dev.run --dev
```

**Start background server:**
```
/dev.run --serve --port 8080
```

**Run with custom config:**
```
/dev.run --config ./config.production.json
```

**Quick add via CLI:**
```
/dev.run --cli add "Buy groceries" --priority high
```

## Notes

- Auto-detect language/runtime and use appropriate run command
- Support hot reload in dev mode for faster iteration
- Provide clear error messages with actionable suggestions
- Support both interactive REPL and single-command CLI modes
- Handle graceful shutdown (save state, close connections)
- Validate configuration before starting
- Log all operations for debugging
- Support different environments (dev, staging, production)
- Consider containerized deployment (Docker)
- Provide health check endpoint for server mode
