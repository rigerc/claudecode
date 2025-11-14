---
name: markdown-task-manager
description: Use when managing tasks, the system is a Kanban task manager based on local Markdown files (`kanban.md` and `archive.md`). It follows a strict format compatible with the task-manager.html web application.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - TodoWrite
---

## 🛠️ Skill Functions

When using this skill, you must:

1. **Read kanban.md** to understand current state and get last ID
2. **Create tasks** following strict format
3. **Update tasks** by moving between sections
4. **Check off subtasks** progressively
5. **Document result** in Notes before marking Done
6. **Increment Last Task ID** in config comment
7. **Never archive** unless explicitly requested

## 🔧 User Commands

### Planning
- "Plan [feature]"
- "Create roadmap for 3 months"

### Execution
- "Do TASK-XXX"
- "Continue TASK-XXX"

### Tracking
- "Where are we?"
- "Weekly status"

### Modifications
- "Break down TASK-XXX"
- "Add subtask to TASK-XXX"

### Search
- "Search in archives: [keyword]"

### Maintenance
- "Archive completed tasks"

## 📘 Git Integration

```bash
# Commits with reference
git commit -m "feat: Add feature (TASK-042 - 3/5)"
git commit -m "fix: Bug fix (TASK-001)"

# Branches
git checkout -b feature/TASK-042-notifications
```

## ⚠️ Critical Points of Attention

1. **Markdown Format**: Strictly respect format (no `##` inside tasks)
2. **ID Increment**: Always increment `<!-- Config: Last Task ID: XXX -->`
3. **Columns**: Use exact column names defined in Configuration
4. **Archiving**: NEVER archive automatically, only on request
5. **Documentation**: Always fill `**Notes**:` with Result, Modified files, etc.

## 🎓 Usage

### Initialization

Before using the skill, the project must contain:
- `kanban.md` (required)
- `archive.md` (required)
- `AI_WORKFLOW.md` (optional but recommended)
- `CLAUDE.md` (optional - will be created/updated by setup script)
- `task-manager.html` (optional web interface)

**Automatic Setup (Hook):**
When the MarkdownTaskManager plugin is enabled, it automatically sets up the necessary files via a SessionStart hook. The hook runs silently on startup and will:

- Copy template files from `assets/` to the project root if they don't exist
- Create or update `CLAUDE.md` with task manager instructions if needed
- Download `task-manager.html` from the official repository if missing
- Skip any files that already exist (except CLAUDE.md which gets appended if missing the task manager reference)

**Manual Setup:**
If you need to run setup manually or want verbose output:
```bash
# From project dir (CLAUDE_PROJECT_DIR)
.claude/hooks/scripts/auto-setup.sh
```

### First Use

```
"Use the markdown-task-manager skill to create a task for [feature]"
```

### Invocation Examples

```
"Skill markdown-task-manager: create a task to implement authentication"
"Skill markdown-task-manager: update TASK-007 with results"
"Skill markdown-task-manager: list all tasks in progress"
"Skill markdown-task-manager: archive completed tasks"
```

## 🔍 Implementation Details

### Reading kanban.md

Always start by reading `kanban.md` to:
- Get the last task ID from `<!-- Config: Last Task ID: XXX -->`
- Understand existing columns structure
- Check current tasks in each column

### Creating a New Task

1. Calculate new ID: `last_id + 1`
2. Format as `TASK-XXX` (3 digits with leading zeros)
3. Add to "📝 To Do" section
4. Update `<!-- Config: Last Task ID: XXX -->` comment
5. Use today's date for `**Created**:`

### Moving Tasks Between Columns

When moving a task:
1. Copy entire task content (from `### TASK-XXX` to blank line before next task)
2. Paste in target column section
3. Delete from original location
4. Update dates accordingly (`**Started**:` or `**Finished**:`)

### Completing Tasks

Before moving to "✅ Done":
1. Ensure all subtasks are checked `[x]`
2. Add `**Finished**: YYYY-MM-DD`
3. Fill in `**Notes**:` section with:
   - `**Result**:` describing what was accomplished
   - `**Modified files**:` listing changed files with line ranges
   - `**Technical decisions**:` if any choices were made
   - `**Tests performed**:` if tests were run

### Archiving Tasks

Only when user explicitly requests archiving:
1. Read task from "✅ Done" section in `kanban.md`
2. Append task to "## ✅ Archives" section in `archive.md`
3. Add separator `---` between archived tasks
4. Remove task from `kanban.md`