---
name: markdown-task-manager
description: Use to manage Kanban tasks using local Markdown files. Creates tasks in kanban.md, archives to archive.md, and integrates with task-manager.html. Handles task creation, progress tracking, archival, and reporting.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - TodoWrite
---

# Markdown Task Manager

## Quick Start

Create and manage tasks using strict format:

```
"Create a new task for implementing user authentication"
"Archive completed task TASK-001"
"Generate status report for current sprint"
```

## How It Works

1. **Task Creation** - Creates tasks in `kanban.md` with strict format
2. **Progress Tracking** - Updates task status and timestamps
3. **Archival** - Moves completed tasks to `archive.md`
4. **Reporting** - Generates status and progress reports

## Task Format

All tasks follow this mandatory structure:
- **ID**: TASK-XXX format
- **Priority**: Critical/High/Medium/Low
- **Status**: Created/Started/Due/Finished dates
- **Description**: Free text (no subheadings allowed)
- **Sections**: Subtasks, Notes, Results, Modified files

See [detailed guide](references/detailed-guide.md) for complete format specification and examples.