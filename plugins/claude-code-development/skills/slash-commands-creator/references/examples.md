# Slash Command Examples

## Simple Reusable Review Command

```markdown
---
description: Review code for correctness, security, and clarity
---

Review this code for:
- Logical and edge-case bugs
- Security issues
- Readability and maintainability problems
Provide concrete, actionable suggestions.
```

## Structured PR Review Command

```markdown
---
description: Review a pull request by number
argument-hint: [pr-number] [priority] [assignee]
---

Review PR #$1 with priority $2 and assign to $3.
Focus on:
- Security vulnerabilities
- Performance regressions
- Test coverage and failure risks
Return a concise, structured summary.
```

## Command with Bash Tools

```markdown
---
description: Run tests and generate coverage report
allowed-tools: [Bash(npm test:*), Bash(npm run coverage:*)]
---

Run the test suite and generate a coverage report:
1. Execute !`npm test`
2. Generate coverage with !`npm run coverage`
3. Summarize test results and coverage metrics
```

## Command with File Context

```markdown
---
description: Analyze component dependencies
argument-hint: [component-path]
---

Analyze dependencies for component at @$1:
- List all imports
- Identify circular dependencies
- Suggest optimization opportunities
```

## Command with Multiple Arguments

```markdown
---
description: Generate boilerplate for a new feature
argument-hint: [feature-name] [feature-type] [output-dir]
---

Generate boilerplate for feature "$1" of type $2 in directory $3:
- Create component structure
- Generate test files
- Add documentation template
Show the file structure before creating files.
```
