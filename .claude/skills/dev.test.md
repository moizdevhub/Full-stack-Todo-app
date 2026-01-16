---
description: Run tests for the todo console app with various options and coverage
handoffs:
  - label: Run the app
    agent: dev.run
    prompt: Run the todo console app
  - label: View test coverage
    agent: dev.test
    prompt: Run tests with coverage --coverage
---

## User Input

```text
$ARGUMENTS
```

## Task

Run tests for the Todo Console App with various testing modes and options.

### Input Processing

1. **Parse the user input** from `$ARGUMENTS`:
   - Test scope:
     - `--unit` run only unit tests
     - `--integration` run only integration tests
     - `--e2e` run end-to-end tests
     - (no flag) run all tests
   - Coverage: `--coverage` to generate coverage report
   - Watch mode: `--watch` to run tests in watch mode
   - Specific test: `--file <pattern>` to run specific test file(s)
   - Verbose: `--verbose` for detailed output
   - Bail: `--bail` to stop on first failure

2. **Auto-detect test framework**:
   - Check for test configuration files (jest.config.js, pytest.ini, etc.)
   - Detect test framework from package.json or requirements.txt
   - Support common frameworks: Jest, Mocha, PyTest, Go test, etc.

### Implementation Steps

1. **Detect test setup**:
   - Look for test files in common locations (test/, tests/, __tests__/)
   - Check package.json or other config for test scripts
   - Identify test framework being used
   - If no tests exist, guide user to create them

2. **Build test command**:
   - Based on detected framework, construct appropriate test command
   - Apply user-provided flags and filters
   - Set up environment variables if needed (TEST_ENV=test)

3. **Run tests**:
   - Execute test command with appropriate flags
   - Capture and format output
   - Parse test results (passed, failed, skipped)
   - Generate coverage report if requested

4. **Report results**:
   - Show summary statistics
   - Highlight failures with details
   - Display coverage percentage if generated
   - Suggest fixes for common issues

### Output Format

**Test run summary:**
```
🧪 Running tests...

Framework: [Jest/PyTest/etc]
Scope: [unit/integration/all]
Files: [count] test files

─────────────────────────────────────────
[Test execution output]
─────────────────────────────────────────

Results:
  ✓ Passed: [count] ([percentage]%)
  ✗ Failed: [count] ([percentage]%)
  ○ Skipped: [count]
  ⏱ Duration: [time]

[If --coverage]
Coverage:
  Lines: [percentage]%
  Functions: [percentage]%
  Branches: [percentage]%
```

**With failures:**
```
Failed Tests:

✗ test/todo.test.js
  ✗ should add todo item
    Expected: true
    Received: false
    at todo.test.js:15:10

✗ test/delete.test.js
  ✗ should delete todo by id
    Error: Todo not found
    at delete.test.js:23:5

Run with --verbose for full stack traces
```

**Coverage report:**
```
📊 Test Coverage Report

File                  | Lines    | Functions | Branches
─────────────────────|──────────|───────────|──────────
src/todo.js          | 85.2%    | 80.0%     | 75.5%
src/storage.js       | 92.3%    | 100.0%    | 88.9%
src/utils.js         | 78.5%    | 75.0%     | 70.2%
─────────────────────|──────────|───────────|──────────
Total                | 85.0%    | 85.0%     | 78.2%

Coverage report: ./coverage/index.html
```

### Framework-Specific Commands

**JavaScript/TypeScript (Jest):**
```bash
npm test [-- options]
npm run test:unit
npm run test:coverage
```

**Python (PyTest):**
```bash
pytest tests/
pytest --cov=src tests/
pytest -v tests/test_todo.py
```

**Go:**
```bash
go test ./...
go test -v -cover ./...
go test -run TestAddTodo
```

**Java (JUnit/Maven):**
```bash
mvn test
mvn test -Dtest=TodoTest
```

### Error Handling

- If no tests found: "No test files found. Create tests in the test/ directory."
- If test framework not installed: "Test framework not found. Install [framework] first."
- If all tests fail: Provide failure summary and suggest running with --verbose
- If coverage tool not available: "Coverage tool not installed. Install [tool] first."

### Interactive Mode

If no arguments provided, show test options:

```
Select test mode:

1. Run all tests
2. Run unit tests only
3. Run integration tests only
4. Run with coverage
5. Watch mode (re-run on changes)
6. Run specific test file

Enter number (1-6):
```

### Examples

**Run all tests:**
```
/dev.test
```

**Run only unit tests:**
```
/dev.test --unit
```

**Run with coverage:**
```
/dev.test --coverage
```

**Run specific test file:**
```
/dev.test --file todo.test.js
```

**Watch mode for TDD:**
```
/dev.test --watch
```

**Verbose output with coverage:**
```
/dev.test --verbose --coverage
```

**Stop on first failure:**
```
/dev.test --bail
```

## Notes

- Auto-detect test framework and adapt commands accordingly
- Support multiple test frameworks in the same project
- Cache test results for faster subsequent runs
- Integrate with CI/CD pipelines
- Suggest creating tests if none exist
- Provide helpful error messages for common test failures
- Consider parallel test execution for faster runs
- Support test filtering by tags/categories
