# 📚 Markdown Format and Examples

This folder contains complete example files for the Markdown Task Manager, along with detailed documentation of the Markdown format used.

## 📁 Example Files

```
examples/
├── kanban.md      # Main file with config and active tasks
├── archive.md     # Archive of completed tasks
└── README.md      # This file (format documentation)
```

## 🎯 Overview

The Markdown Task Manager uses **two Markdown files** to organize your tasks:

| File | Role | Loading |
|------|------|---------|
| `kanban.md` | Configuration + Active tasks | At startup |
| `archive.md` | Archived tasks | On demand |

---

## 📄 Structure of `kanban.md`

### 1. Configuration Comment (required)

```markdown
# Kanban Board

<!-- Config: Last Task ID: 42 -->
```

- **Required**: Auto-incremented ID counter
- The application reads this number to generate the next task ID
- Automatically modified by the application

### 2. Configuration Section (required)

```markdown
## ⚙️ Configuration

**Columns**: 📝 To Do (todo) | 🚀 In Progress (in-progress) | 👀 In Review (in-review) | ✅ Done (done)

**Categories**: Frontend, Backend, Design, DevOps, Tests, Documentation

**Users**: @alice (Alice Martin), @bob (Bob Smith), @charlie (Charlie Brown)

**Priorities**: 🔴 Critical | 🟠 High | 🟡 Medium | 🟢 Low

**Tags**: #bug #feature #ui #backend #urgent #refactor #docs #test #performance

---
```

#### Column Format

```
{Emoji} {Display Name} ({unique-id})
```

- **Emoji**: Optional but recommended for the interface
- **Display Name**: Text visible in the Kanban
- **Unique ID**: Internal identifier (letters, numbers, hyphens)

**Examples**:
```markdown
📝 To Do (todo)
🚀 In Progress (in-progress)
✅ Done (done)
```

#### Category Format

Comma-separated list:
```markdown
**Categories**: Frontend, Backend, Design
```

#### User Format

```
@username (Full Name), @other (Other Name)
```

- **@username**: Short identifier for mentions
- **Full Name**: Complete name in parentheses

#### Priority Format

```
{Emoji} {Name} | {Emoji} {Name} | ...
```

The 4 standard priorities:
```markdown
🔴 Critical | 🟠 High | 🟡 Medium | 🟢 Low
```

#### Tag Format

List of space-separated tags:
```markdown
**Tags**: #bug #feature #ui #backend
```

### 3. Column Sections

Each Kanban column has its own section:

```markdown
## 📝 To Do

{Tasks for this column...}

## 🚀 In Progress

{Tasks for this column...}

## ✅ Done

{Tasks for this column...}
```

**Important**:
- The section title must match the name defined in the configuration
- The order of sections defines the display order in the Kanban

---

## 📝 Task Format

### Complete Structure

```markdown
### TASK-001 | My Task Title

**Priority**: High | **Category**: Frontend | **Assigned**: @alice, @bob
**Created**: 2025-01-20 | **Due**: 2025-02-15
**Tags**: #feature #ui

Detailed task description in Markdown.

You can use **all standard Markdown**:
- Lists
- **Bold** and *italic*
- `Inline code`
- [Links](https://example.com)

**Subtasks**:
- [ ] First step to do
- [x] Completed step
- [ ] Last step

**Notes**:
Additional notes or context...

---
```

### Required Fields

| Field | Format | Description |
|-------|--------|-------------|
| **ID** | `TASK-XXX` | Unique auto-incremented number |
| **Title** | Text after `\|` | Short task title |
| **Priority** | Critical\|High\|Medium\|Low | Priority level |
| **Category** | Free text | Category/project |
| **Created** | YYYY-MM-DD | Creation date |

### Optional Fields

| Field | Format | Description |
|-------|--------|-------------|
| **Assigned** | `@user1, @user2` | Assigned users (comma-separated) |
| **Started** | YYYY-MM-DD | Actual start date |
| **Due** | YYYY-MM-DD | Deadline |
| **Completed** | YYYY-MM-DD | Completion date |
| **Tags** | `#tag1 #tag2` | Tags (with #, space-separated) |
| **Subtasks** | `- [ ]` or `- [x]` | Markdown checklist |
| **Notes** | Free text | Additional notes |

### Inline Metadata (Priority Line)

```markdown
**Priority**: High | **Category**: Backend | **Assigned**: @alice, @bob
```

- Separated by ` | ` (pipe surrounded by spaces)
- Flexible order
- Missing fields are omitted

### Dates (Created Line)

```markdown
**Created**: 2025-01-20 | **Started**: 2025-01-22 | **Due**: 2025-02-15
```

- **Required** format: `YYYY-MM-DD` (ISO 8601)
- Separated by ` | `
- Only `**Created**` is mandatory

### Tags

```markdown
**Tags**: #bug #urgent #frontend
```

- Start with `#`
- Space-separated
- No commas

### Subtasks

```markdown
**Subtasks**:
- [ ] Unstarted task
- [x] Completed task
- [ ] Another task
```

- Standard Markdown checkbox format
- `[ ]` = not done
- `[x]` = done
- The application automatically calculates progress

### End Separator

```markdown
---
```

- **Required** between each task
- Three hyphens on a single line
- Allows the parser to delimit tasks

---

## 🗄️ Structure of `archive.md`

```markdown
# Task Archive

> This file contains all completed and archived tasks.

## ✅ January 2025

### TASK-098 | Archived Task

**Priority**: High | **Category**: Frontend | **Assigned**: @alice
**Created**: 2024-12-20 | **Started**: 2024-12-28 | **Completed**: 2025-01-05
**Tags**: #feature #ui

Task description...

**Result**:
The task was completed successfully.

---

### TASK-097 | Another Archived Task

...

---

## ✅ December 2024

### TASK-090 | Older Task

...
```

### Chronological Organization

- **Sections by month**: `## ✅ January 2025`
- **Most recent on top**: New months are added at the top
- **Tasks per month**: Sorted by completion date descending

### Differences from kanban.md

1. **No Configuration section**: Not needed
2. **Sections by date**: Rather than by column
3. **Completed field required**: Task end date
4. **Deferred loading**: File not read at startup

---

## 🔧 Manual Editing

### Create a New Task

1. Open `kanban.md` in your editor
2. Find the comment `<!-- Config: Last Task ID: X -->`
3. Note the number (e.g., 42)
4. Go to the appropriate column section (e.g., `## 📝 To Do`)
5. Copy this template:

```markdown
### TASK-043 | My New Title

**Priority**: Medium | **Category**: Backend | **Assigned**: @alice
**Created**: 2025-01-20 | **Due**: 2025-02-01
**Tags**: #feature

Description of my new task...

**Subtasks**:
- [ ] Step 1
- [ ] Step 2

---
```

6. Increment the counter in the comment: `<!-- Config: Last Task ID: 43 -->`
7. Save

### Move a Task Between Columns

1. Cut the entire section (from `###` to `---` inclusive)
2. Paste into another column section
3. Optional: Add `**Started**` if moving to "In Progress"
4. Save

### Archive a Task

1. Cut the complete task from `kanban.md`
2. Open `archive.md`
3. Find or create the month section (e.g., `## ✅ January 2025`)
4. Paste the task
5. Add the `**Completed**: 2025-01-20` field in the dates line
6. Save both files

### Mark a Subtask as Completed

Replace `[ ]` with `[x]`:

```markdown
**Subtasks**:
- [x] Completed step
- [ ] Step in progress
```

---

## 🎨 Customization

### Custom Columns

You can create your own columns:

```markdown
**Columns**: 📋 Backlog (backlog) | 📝 To Do (todo) | 🏗️ Dev (dev) | 🧪 Test (test) | ✅ Prod (prod)
```

Then create the corresponding sections:

```markdown
## 📋 Backlog

...

## 📝 To Do

...
```

### Custom Categories

Adapt categories to your project:

```markdown
**Categories**: Interface, API, Database, Security, Documentation, Infrastructure
```

### Custom Tags

Create your own tag conventions:

```markdown
**Tags**: #p0 #p1 #p2 #sprint-5 #customer-request #tech-debt #security
```

---

## 📊 Complete Examples

### Simple Task

```markdown
### TASK-001 | Fix Login Bug

**Priority**: Critical | **Category**: Backend | **Assigned**: @bob
**Created**: 2025-01-20 | **Due**: 2025-01-21
**Tags**: #bug #urgent

Users cannot log in since this morning.

---
```

### Task with Subtasks

```markdown
### TASK-002 | Implement OAuth Authentication

**Priority**: High | **Category**: Backend | **Assigned**: @alice, @bob
**Created**: 2025-01-15 | **Started**: 2025-01-18 | **Due**: 2025-02-01
**Tags**: #feature #security

Add OAuth 2.0 support for Google and GitHub.

**Subtasks**:
- [x] Research libraries
- [x] Setup passport.js
- [ ] Implement Google OAuth
- [ ] Implement GitHub OAuth
- [ ] Integration tests
- [ ] Documentation

**Notes**:
Use passport-google-oauth20 and passport-github2

---
```

### Archived Task

```markdown
### TASK-050 | PostgreSQL Migration

**Priority**: High | **Category**: Infrastructure | **Assigned**: @charlie
**Created**: 2024-12-01 | **Started**: 2024-12-05 | **Completed**: 2024-12-20
**Tags**: #database #migration

Complete migration from MySQL to PostgreSQL 14.

**Result**:
- Successful migration without data loss
- 40% performance improvement
- All tests passing

---
```

---

## 🔍 Parsing the Format (for Developers)

### Extract Configuration

```javascript
// Last Task ID
const idMatch = content.match(/<!-- Config: Last Task ID: (\d+) -->/);
const lastTaskId = idMatch ? parseInt(idMatch[1]) : 0;

// Columns
const colMatch = content.match(/\*\*Columns\*\*:\s*(.+)/);
const columns = colMatch[1].split('|').map(col => {
    const match = col.trim().match(/(.+?)\s*\(([^)]+)\)/);
    return {
        name: match ? match[1].trim() : col.trim(),
        id: match ? match[2].trim() : col.trim().toLowerCase()
    };
});

// Categories
const catMatch = content.match(/\*\*Categories\*\*:\s*(.+)/);
const categories = catMatch ? catMatch[1].split(',').map(c => c.trim()) : [];

// Users
const userMatch = content.match(/\*\*Users\*\*:\s*(.+)/);
const users = userMatch[1].split(',').map(u => {
    const match = u.trim().match(/@(\w+)\s*\(([^)]+)\)/);
    return match ? { id: match[1], name: match[2] } : { id: u.trim(), name: u.trim() };
});
```

### Extract Tasks

```javascript
// Split by column sections
const sections = content.split(/^## /m).slice(1);

// For each section
sections.forEach(section => {
    const [header, ...taskLines] = section.split('\n');
    const columnMatch = header.match(/[📝🚀👀✅]\s*(.+)/);
    const columnName = columnMatch ? columnMatch[1].trim() : header.trim();

    // Split by tasks
    const taskContent = taskLines.join('\n');
    const tasks = taskContent.split(/^### TASK-/m).slice(1);

    tasks.forEach(taskText => {
        const task = parseTask('TASK-' + taskText);
        // ...
    });
});
```

### Parse a Task

```javascript
function parseTask(content) {
    // ID and title
    const titleMatch = content.match(/^(\d+)\s*\|\s*(.+)/m);
    const id = 'TASK-' + titleMatch[1];
    const title = titleMatch[2].trim();

    // Priority, category, assignees
    const metaMatch = content.match(/\*\*Priority\*\*:\s*(\w+)(?:\s*\|\s*\*\*Category\*\*:\s*([^|]+))?(?:\s*\|\s*\*\*Assigned\*\*:\s*([^\n]+))?/);
    const priority = metaMatch[1];
    const category = metaMatch[2] ? metaMatch[2].trim() : '';
    const assignees = metaMatch[3] ? metaMatch[3].split(',').map(a => a.trim()) : [];

    // Dates
    const dateMatch = content.match(/\*\*Created\*\*:\s*(\d{4}-\d{2}-\d{2})(?:\s*\|\s*\*\*Started\*\*:\s*(\d{4}-\d{2}-\d{2}))?(?:\s*\|\s*\*\*Due\*\*:\s*(\d{4}-\d{2}-\d{2}))?/);
    const created = dateMatch[1];
    const started = dateMatch[2] || null;
    const due = dateMatch[3] || null;

    // Tags
    const tagsMatch = content.match(/\*\*Tags\*\*:\s*(.+)/);
    const tags = tagsMatch ? tagsMatch[1].split(/\s+/).map(t => t.replace('#', '')) : [];

    // Description
    const descMatch = content.match(/\*\*Tags\*\*:.*?\n\n([\s\S]*?)(?:\n\*\*|---)/);
    const description = descMatch ? descMatch[1].trim() : '';

    // Subtasks
    const subtasks = [];
    const subtaskMatches = content.matchAll(/- \[([ x])\] (.+)/g);
    for (const match of subtaskMatches) {
        subtasks.push({ completed: match[1] === 'x', text: match[2] });
    }

    return { id, title, priority, category, assignees, created, started, due, tags, description, subtasks };
}
```

---

## ⚡ Performance

### Recommendations

| File | Max Size | Max Tasks | Parsing |
|------|----------|-----------|---------|
| kanban.md | 500 KB | 1000 | < 100ms |
| archive.md | Unlimited | Unlimited | Lazy load |

### Optimizations

- **Regular archiving**: Move old tasks to archive.md
- **Short sections**: No more than 200-300 tasks per column
- **Cache**: The application keeps tasks in memory
- **Lazy loading**: archive.md is only loaded on demand

---

## ✅ Format Validation

### Checklist

- [ ] Comment `<!-- Config: Last Task ID: X -->` present
- [ ] Section `## ⚙️ Configuration` with all columns
- [ ] Each column has its section `## {Column Name}`
- [ ] Each task starts with `### TASK-{num} |`
- [ ] All tasks have Priority, Category, Created
- [ ] Dates in YYYY-MM-DD format
- [ ] Separator `---` after each task
- [ ] No duplicate IDs

---

## 💡 Tips and Best Practices

1. **Sequential IDs**: Never skip a number, never reuse one
2. **ISO Dates**: Always YYYY-MM-DD for consistency
3. **Regular archiving**: At least once a month
4. **Git-friendly**: Commit after each batch of modifications
5. **Consistent categories**: Define them in the config first
6. **Normalized tags**: Create a convention for your team
7. **Backup**: Your MD files are precious, back them up

---

**Format Version**: 1.0
**Last Updated**: 2025-11-08