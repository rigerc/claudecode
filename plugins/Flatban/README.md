# Flatban Plugin for Claude Code

A Claude Code plugin that enables integration with [Flatban](https://github.com/gelform/flatban) - a filesystem-based Kanban project management system designed for AI-assisted development.

## Overview

Flatban is a git-friendly, zero-dependency task management system that stores tasks as markdown files with YAML frontmatter. This plugin allows you to manage your Flatban boards directly from Claude Code using natural language commands.

## Features

- **AI-Native Task Management**: Create, update, and manage tasks using natural language
- **Filesystem-Based**: All tasks stored as markdown files in `.flatban/` directory
- **Git-Friendly**: Version control your entire task history
- **Zero Dependencies**: No external databases or services required
- **CLI Integration**: Full Flatban CLI command support
- **Natural Language Workflow**: Simply say "do the next task" or "create a task for fixing the login bug"

## Installation

1. Install Flatban globally:
```bash
npm install -g flatban
```

2. The plugin should already be available in your Claude Code installation under `@plugins/Flatban/`.

## Quick Start

1. Initialize a Flatban board in your project:
```bash
flatban init
```

2. Start managing tasks with the `/flatban` slash command:
```
/flatban
```

3. Once in Flatban mode, use natural language:
- "Create a task for implementing user authentication"
- "Show me the board"
- "Do the next task"
- "Move the auth task to in progress"

## Usage

### Starting Flatban Mode

Use the slash command to enter Flatban mode:
```
/flatban
```

Once activated, Claude Code remains in Flatban mode for the rest of the conversation, interpreting natural language as task management commands.

### Task Creation

Create tasks using natural language descriptions:

```bash
# Simple task creation
"Create a task for fixing the login bug"

# With specific details
"Create a high-priority task for adding password reset functionality"

# Complex features (will be broken into multiple tasks)
"I need to add authentication to the app"
```

### Task Management

```bash
# View your board
"Show me the board"

# List tasks in specific columns
"Show me all todo tasks"
"What's in the review column?"

# Work on tasks
"Do the next task"
"Work on task abc1234"

# Move tasks between columns
"Move the auth task to in progress"
"Mark task abc1234 as done"
```

### Workflow Rules

The plugin follows strict workflow rules:

1. **New tasks** always go to `todo` column (unless explicitly specified)
2. Tasks must be moved to `in-progress` before work begins
3. Completed tasks go to `review` for verification (never directly to `done`)
4. Only users can move tasks from `review` to `done`

## Task Structure

Tasks are stored as markdown files in `.flatban/<column>/<id>-<slug>.md`:

```markdown
---
id: abc1234
title: "Fix login authentication bug"
priority: high
tags: [backend, bug, auth]
assigned: username
---

## Description

Users are unable to log in with valid credentials due to token validation issue.

## Notes

- Check authentication middleware
- Verify JWT token generation
- Add error logging for debugging

## History
- 2025-01-15 10:30: Task created
- 2025-01-15 14:45: Moved to in-progress
```

## Available Commands

### CLI Commands (used automatically)

- `flatban create "title" [options]` - Create new tasks
- `flatban move <task-id> <column>` - Move tasks between columns
- `flatban list [column]` - List tasks with filtering
- `flatban show <task-id>` - Show full task details
- `flatban board [--compact]` - Display the kanban board
- `flatban sync` - Rebuild index after manual edits

### Natural Language Examples

```bash
# Task creation
"Create a task for optimizing database queries"
"Add a critical task for security audit"
"Create tasks for the new feature: user profiles"

# Task management
"What's the next task to work on?"
"Show me all high-priority tasks"
"Move task abc123 to review"

# Working on tasks
"Do the next backend task"
"Complete task abc1234"
"I'm working on the authentication feature now"
```

## Advanced Features

### Task Attributes

Tasks support rich metadata:

- **Priority**: low, medium, high, critical
- **Tags**: Categorize tasks (frontend, backend, bug, feature, etc.)
- **Assignment**: Assign tasks to team members
- **Descriptions**: Detailed task information
- **Notes**: Implementation considerations and technical details

### Web UI

For a visual board interface:
```bash
flatban serve
```

This provides a web-based kanban board at `http://localhost:3000`.

### Git Integration

Since tasks are just markdown files:
- Track task history with git
- Collaborate with team members through pull requests
- Review task changes alongside code changes
- Sync with `flatban sync` after pulling changes

## Plugin Structure

```
@plugins/Flatban/
├── plugin.json          # Plugin metadata
├── commands/
│   └── flatban.md      # Slash command definition
└── skills/
    └── flatban.md      # AI skill implementation
```

## Examples

### Feature Development Workflow

```bash
User: "I need to add user profiles to the app"

AI: I'll create tasks for implementing user profiles:

flatban create "Design user profile database schema" --priority=high --tags=backend,planning
flatban create "Implement profile API endpoints" --priority=high --tags=backend,api
flatban create "Create profile UI components" --priority=high --tags=frontend
flatban create "Add profile photo upload" --priority=medium --tags=frontend,storage
flatban create "Write profile feature tests" --priority=medium --tags=testing

Created 5 tasks in todo column. Would you like me to do the first task?
```

### Bug Fixing Workflow

```bash
User: "Do the next task"

AI: flatban list todo

Found task: abc1234 - "Fix login authentication bug" (high priority)
Should I work on this task?

User: Yes

AI: flatban move abc1234 in-progress
flatban show abc1234

[Reads task details and implements the fix]

flatban move abc1234 review

Task completed! Please review the changes and move to done when verified.
```

## Contributing

This plugin is part of the Claude Code ecosystem. To contribute:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request with your changes

## License

This plugin follows the same license as Claude Code.

## Support

For issues with:
- **Flatban CLI**: Visit [flatban GitHub](https://github.com/gelform/flatban)
- **Claude Code Plugin**: Check Claude Code documentation
- **Usage Questions**: Refer to the examples above or use `/flatban help`

---

**Flatban Plugin** - Bridging AI assistants with practical task management.