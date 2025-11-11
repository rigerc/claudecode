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

## 📁 File Structure

### kanban.md

```markdown
# Kanban Board

<!-- Config: Last Task ID: 42 -->

## ⚙️ Configuration

**Columns**: 📝 To Do | 🚀 In Progress | 👀 Review | ✅ Done
**Categories**: Frontend, Backend, DevOps
**Users**: @alice, @bob
**Tags**: #bug, #feature, #docs

---

## 📝 To Do

### TASK-001 | Title
[...]

## 🚀 In Progress

## 👀 Review

## ✅ Done

### TASK-003 | Completed task
[...]
```

### archive.md

```markdown
# Task Archive

> Archived tasks

## ✅ Archives

### TASK-001 | Archived task
[... full content ...]

---

### TASK-002 | Another archived task
[... full content ...]
```

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

## 📝 Complete Examples

### Simple Task

```markdown
### TASK-001 | Fix login bug

**Priority**: Critical | **Category**: Backend | **Assigned**: @bob
**Created**: 2025-01-20 | **Due**: 2025-01-21
**Tags**: #bug #urgent

Users cannot log in. Error 500 in logs.

**Notes**:
Check Redis, related to yesterday's deployment.
```

### Complete Task with Result

```markdown
### TASK-042 | Notification system

**Priority**: High | **Category**: Backend | **Assigned**: @alice
**Created**: 2025-01-15 | **Started**: 2025-01-18 | **Finished**: 2025-01-22
**Tags**: #feature

Real-time notifications with WebSockets.

**Subtasks**:
- [x] Setup WebSocket server
- [x] REST API
- [x] Email sending
- [x] Notifications UI
- [x] E2E tests

**Notes**:

**Result**:
✅ Functional system with WebSocket, REST API and emails.

**Modified files**:
- src/websocket/server.js (lines 1-150)
- src/api/notifications.js (lines 20-85)

**Technical decisions**:
- Socket.io for WebSockets
- SendGrid for emails
- 30-day history in MongoDB

**Tests performed**:
- ✅ 100 simultaneous connections
- ✅ Auto-reconnection
- ✅ Emails < 2s
```

## 🛠️ Skill Functions

When using this skill, you must:

1. **Read kanban.md** to understand current state and get last ID
2. **Create tasks** following strict format
3. **Update tasks** by moving between sections
4. **Check off subtasks** progressively
5. **Document result** in Notes before marking Done
6. **Increment Last Task ID** in config comment
7. **Never archive** unless explicitly requested

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

## Troubleshooting

### File and Format Issues

**Problem**: kanban.md or archive.md files don't exist
- **Cause**: Initial setup not completed or files deleted accidentally
- **Solution**: Run automatic setup via SessionStart hook or manual setup script
- **Manual fix**: Copy template files from assets/ directory to project root
- **Verification**: Ensure both kanban.md and archive.md exist in project directory

**Problem**: Tasks not displaying correctly in task-manager.html
- **Cause**: Format violations, especially using `##` or `###` headings inside tasks
- **Solution**: Review task format and remove any nested headings
- **Check**: Ensure strict adherence to the mandatory template format
- **Fix**: Replace nested headings with bold subsections like `**Technical decisions**:`

**Problem**: Task ID not incrementing correctly
- **Cause**: Last Task ID comment not updated or formatted incorrectly
- **Solution**: Verify `<!-- Config: Last Task ID: XXX -->` format is exact
- **Check**: Ensure comment is at the top of kanban.md file
- **Fix**: Manually update the comment with the correct last used ID

### Task Management Issues

**Problem**: Cannot find specific task in kanban.md
- **Cause**: Task moved to wrong section or ID formatting issues
- **Solution**: Search for task ID using grep: `grep "TASK-XXX" kanban.md`
- **Debug**: Check all column sections and archive.md for missing tasks
- **Prevention**: Always move tasks using complete task blocks

**Problem**: Duplicate task IDs in the system
- **Cause**: Manual editing errors or concurrent task creation conflicts
- **Solution**: Identify duplicate IDs and renumber affected tasks
- **Fix**: Update Last Task ID comment to reflect highest actual task ID
- **Prevention**: Always check current last ID before creating new tasks

**Problem**: Subtasks not being tracked correctly
- **Cause**: Incorrect checkbox format or missing `**Subtasks**:` section
- **Solution**: Use proper Markdown checkbox format: `- [ ]` and `- [x]`
- **Check**: Ensure `**Subtasks**:` section exists and is properly formatted
- **Example**:
  ```markdown
  **Subtasks**:
  - [ ] First incomplete subtask
  - [x] Completed subtask
  ```

### Performance and Scalability Issues

**Problem**: kanban.md file becoming too large and slow to process
- **Cause**: Too many active tasks or insufficient archiving
- **Solution**: Regularly archive completed tasks to keep active list manageable
- **Maintenance**: Set threshold (e.g., archive tasks older than 30 days)
- **Optimization**: Archive tasks in batches to maintain performance

**Problem**: Web interface (task-manager.html) loading slowly
- **Cause**: Large kanban.md file with many tasks and complex formatting
- **Solution**: Optimize task descriptions and archive old completed tasks
- **Performance**: Limit active tasks to under 50 for optimal web interface performance
- **Alternative**: Consider splitting large projects into multiple kanban files

### Integration Issues

**Problem**: Git integration not working properly
- **Cause**: Inconsistent commit message format or missing task references
- **Solution**: Always include task ID in commit messages: `(TASK-XXX)`
- **Best practice**: Use format: `type: description (TASK-XXX - progress)`
- **Branch naming**: Use consistent pattern: `feature/TASK-XXX-description`

**Problem**: SessionStart hook not running automatically
- **Cause**: Plugin not enabled or hook configuration issues
- **Solution**: Verify MarkdownTaskManager plugin is enabled in Claude Code
- **Debug**: Check hook logs for any error messages
- **Manual**: Run setup script manually: `.claude/hooks/scripts/auto-setup.sh`

### Data Integrity Issues

**Problem**: Corrupted kanban.md due to editing conflicts
- **Cause**: Simultaneous edits or merge conflicts in version control
- **Solution**: Restore from backup or manually reconstruct using git history
- **Prevention**: Use file locking or coordinate editing sessions
- **Recovery**: Check git reflog for previous versions if needed

**Problem**: Archive.md becoming disorganized
- **Cause**: Inconsistent archiving process or missing separators
- **Solution**: Ensure proper `---` separators between archived tasks
- **Maintenance**: Regularly review and reorganize archive structure
- **Format**: Maintain consistent date ordering within archives

### Browser Compatibility Issues

**Problem**: task-manager.html not displaying correctly in certain browsers
- **Cause**: Browser compatibility issues or JavaScript errors
- **Solution**: Test in modern browsers and check browser console for errors
- **Debug**: Open browser developer tools to identify specific issues
- **Alternative**: Use text-based task management if web interface unavailable

### Common Error Messages and Solutions

**"Task not found" errors**
- Verify task ID exists in kanban.md
- Check for ID formatting (TASK-XXX with leading zeros)
- Search in archive.md if task might be archived
- Review recent commits for task references

**"Invalid format" warnings**
- Check for nested headings inside task descriptions
- Verify `**Subtasks**:` and `**Notes**:` sections use colons
- Ensure no `##` or `###` headings within task content
- Review mandatory template compliance

**"File not found" errors**
- Confirm kanban.md and archive.md exist in project root
- Check file permissions and accessibility
- Run setup script if files are missing
- Verify working directory is correct

### Performance Optimization Tips

**File Management**
- Archive completed tasks regularly (keep only last 30 days in active)
- Use concise task descriptions to minimize file size
- Implement batch archiving for efficiency
- Consider separate kanban files for very large projects

**Workflow Optimization**
- Create task templates for common task types
- Use batch operations for multiple similar tasks
- Implement regular maintenance schedules
- Use consistent naming and categorization patterns

**Web Interface Performance**
- Limit active tasks to under 50 for optimal performance
- Use task filtering and search features in task-manager.html
- Clear browser cache periodically
- Consider browser extensions for better Markdown rendering

### Getting Help

1. **File verification**: Check kanban.md format using template examples
2. **Setup verification**: Run manual setup script to verify installation
3. **Log analysis**: Check Claude Code logs for hook or plugin errors
4. **Template reference**: Review complete examples in skill documentation
5. **Community support**: Check plugin repository for known issues and solutions

## Performance Considerations

### File Processing Performance

**Efficient File Operations**
- Read kanban.md once per operation and cache content in memory
- Use streaming reads for large kanban files with many tasks
- Implement incremental updates to avoid rewriting entire files
- Use atomic file operations to prevent corruption during updates

**Memory Management**
- Process tasks in batches for very large kanban files (1000+ tasks)
- Clear unused data structures after task operations complete
- Use generators for task iteration instead of loading all tasks into memory
- Monitor memory usage during task creation and archiving operations

### Task Management Scalability

**Large Project Organization**
```markdown
# Performance guidelines for large projects:

## Optimal Task Count
- Active tasks: Keep under 50 for optimal performance
- Total tasks: Consider splitting projects with 500+ tasks
- Archive regularly: Move tasks older than 30 days to archive.md

## Task Description Length
- Recommended: Keep under 500 characters per task description
- Maximum: Avoid 1000+ character descriptions
- Subtasks: Limit to 20 subtasks per task
- Notes: Keep technical notes concise and focused
```

**Multi-Project Strategies**
- Use separate kanban files for different project domains
- Implement cross-project task linking with unique prefixes
- Create summary kanban for high-level project overview
- Use consistent ID schemes across multiple kanban files

### Web Interface Performance

**HTML Rendering Optimization**
- Lazy loading of archived tasks for large archives
- Implement client-side filtering and search functionality
- Use virtual scrolling for long task lists
- Cache rendered HTML to avoid reprocessing on every visit

**Browser Performance Tips**
```javascript
// Performance monitoring for task-manager.html
const performanceMonitor = {
  init: function() {
    this.startTime = performance.now();
    this.taskCount = document.querySelectorAll('h3[id^="TASK-"]').length;
  },

  logMetrics: function() {
    const renderTime = performance.now() - this.startTime;
    console.log(`Rendered ${this.taskCount} tasks in ${renderTime.toFixed(2)}ms`);

    if (renderTime > 1000) {
      console.warn('Slow rendering detected. Consider archiving old tasks.');
    }
  }
};
```

### Automation and Scripting Performance

**Bulk Operations Optimization**
```bash
# Efficient bulk task operations
archive_completed_tasks() {
  # Process in batches to avoid memory issues
  batch_size=50
  while grep -q "✅ Done" kanban.md; do
    # Archive first 50 completed tasks
    head -n $(grep -n "## ✅ Done" kanban.md | tail -1) kanban.md | \
    grep -A $batch_size "^### TASK-" | \
    sed '/^--$/q' >> archive.md
  done
}

# Performance monitoring
monitor_kanban_size() {
  kanban_size=$(wc -l < kanban.md)
  if [ $kanban_size -gt 5000 ]; then
    echo "Warning: kanban.md is large (${kanban_size} lines)"
    echo "Consider archiving completed tasks to improve performance"
  fi
}
```

**Git Integration Performance**
- Use selective git operations to avoid unnecessary file processing
- Implement task-based commits rather than per-operation commits
- Batch multiple task updates into single commits
- Use git hooks for automated task tracking

### Database Alternative for Large Scale

**When to Consider Database Storage**
- Projects with 1000+ active tasks
- Complex task relationships and dependencies
- Multiple users accessing same task system
- Need for advanced querying and reporting

**Migration Strategies**
```python
# Example migration script from Markdown to database
import re
import sqlite3
from datetime import datetime

def migrate_kanban_to_sqlite(kanban_file, db_file):
    """Convert kanban.md to SQLite database for better performance"""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
        CREATE TABLE tasks (
            id TEXT PRIMARY KEY,
            title TEXT,
            status TEXT,
            priority TEXT,
            category TEXT,
            assigned TEXT,
            created TEXT,
            started TEXT,
            due TEXT,
            finished TEXT,
            tags TEXT,
            description TEXT,
            subtasks TEXT,
            notes TEXT,
            result TEXT,
            modified_files TEXT
        )
    ''')

    # Parse and insert tasks
    with open(kanban_file, 'r') as f:
        content = f.read()
        tasks = parse_tasks_from_markdown(content)

        for task in tasks:
            cursor.execute('INSERT INTO tasks VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                          (task['id'], task['title'], task['status'], task['priority'],
                           task['category'], task['assigned'], task['created'], task['started'],
                           task['due'], task['finished'], task['tags'], task['description'],
                           task['subtasks'], task['notes'], task['result'], task['modified_files']))

    conn.commit()
    conn.close()
```

### Monitoring and Metrics

**Performance Metrics to Track**
- Task creation time (time to add new task to kanban.md)
- File processing time (time to read and parse kanban.md)
- Web interface rendering time (task-manager.html load time)
- Archive operation time (time to archive completed tasks)
- Memory usage during task operations

**Performance Monitoring Script**
```python
import time
import psutil
import os

class KanbanPerformanceMonitor:
    def __init__(self, kanban_file='kanban.md'):
        self.kanban_file = kanban_file
        self.process = psutil.Process()

    def measure_operation(self, operation_name, operation_func, *args, **kwargs):
        """Measure performance of a kanban operation"""
        start_time = time.time()
        start_memory = self.process.memory_info().rss

        result = operation_func(*args, **kwargs)

        end_time = time.time()
        end_memory = self.process.memory_info().rss

        execution_time = end_time - start_time
        memory_delta = (end_memory - start_memory) / 1024 / 1024  # MB

        print(f"{operation_name}: {execution_time:.3f}s, {memory_delta:.2f}MB")

        # Performance warnings
        if execution_time > 5.0:
            print(f"WARNING: {operation_name} took {execution_time:.3f}s")

        if memory_delta > 100:
            print(f"WARNING: {operation_name} used {memory_delta:.2f}MB additional memory")

        return result

    def get_kanban_stats(self):
        """Get current kanban.md statistics"""
        if not os.path.exists(self.kanban_file):
            return None

        with open(self.kanban_file, 'r') as f:
            content = f.read()

        task_count = len(re.findall(r'^### TASK-\d+', content, re.MULTILINE))
        file_size = os.path.getsize(self.kanban_file) / 1024  # KB

        return {
            'tasks': task_count,
            'file_size_kb': file_size,
            'file_path': self.kanban_file
        }

# Usage example
monitor = KanbanPerformanceMonitor()
stats = monitor.get_kanban_stats()

if stats:
    print(f"Kanban stats: {stats['tasks']} tasks, {stats['file_size_kb']:.1f}KB")

    if stats['tasks'] > 100:
        print("PERFORMANCE NOTE: Consider archiving completed tasks")
```

### Best Practices for High Performance

1. **Regular Maintenance**: Archive completed tasks weekly
2. **Task Limit Management**: Keep active tasks under 50
3. **File Size Monitoring**: Monitor kanban.md file size
4. **Batch Operations**: Group multiple task updates together
5. **Template Usage**: Use predefined task templates for consistency
6. **Performance Testing**: Monitor operation times for degradation
7. **Memory Awareness**: Track memory usage during bulk operations

---

**This skill ensures complete traceability and total transparency of work done by AI.**