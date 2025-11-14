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

## When to Use This Skill

- Create tasks to document work to be done
- Plan complex features
- Track project progress
- Archive completed tasks
- Generate status reports

## 📋 STRICT Task Format

### Mandatory Template

```markdown
### TASK-XXX | Task title

**Priority**: [Critical|High|Medium|Low] | **Category**: [Value] | **Assigned**: @user1, @user2
**Created**: YYYY-MM-DD | **Started**: YYYY-MM-DD | **Due**: YYYY-MM-DD | **Finished**: YYYY-MM-DD
**Tags**: #tag1 #tag2 #tag3

Free text description. **NO `##` or `###` headings allowed**.

**Subtasks**:
- [ ] First subtask
- [x] Completed subtask

**Notes**:
Additional notes with subsections `**Title**:`.

**Result**:
What was done.

**Modified files**:
- file.js (lines 42-58)
```

### ❌ FORBIDDEN

- `## Title` or `### Title` inside a task
- `**Subtasks**` or `**Notes**` without `:`
- Automatic archiving (only on user request)

**Why?** The HTML parser of the application does not recognize `##` inside tasks.

## 🔄 Workflow

### 1. New Request
1. Read `kanban.md` to get the last task ID
2. Create task in `kanban.md` → "📝 To Do" section
3. Unique ID (TASK-XXX) auto-incremented
4. Break down into subtasks if needed
5. Increment counter in `<!-- Config: Last Task ID: XXX -->`

### 2. Start Work
1. Move task → "🚀 In Progress" section
2. Add `**Started**: YYYY-MM-DD`
3. Check off subtasks progressively

### 3. Finish Work
1. Move → "✅ Done" section
2. Add `**Finished**: YYYY-MM-DD`
3. Document in `**Notes**:`:
   - `**Result**:` - What was done
   - `**Modified files**:` - List with line numbers
   - `**Technical decisions**:` - Choices made
   - `**Tests performed**:` - Validated tests

### 4. Archiving

**⚠️ Tasks are NOT archived immediately!**

- Completed tasks remain in "✅ Done"
- **Only on user request** → move to `archive.md`
- **Never archive directly at end of work**

## 🎯 Golden Rules

### ✅ ALWAYS

1. Create task BEFORE coding
2. Strict format (no `##` inside tasks)
3. Break down if complex (3+ steps)
4. Update in real-time
5. Document result in `**Notes**:`
6. Reference tasks in commits (`TASK-XXX`)
7. Leave in "Done" (archive only on user request)

### ❌ NEVER

1. `## Title` inside a task
2. Code without creating task
3. Forget to check off subtasks
4. Archive immediately (stay in "Done")
5. Forget to document the result