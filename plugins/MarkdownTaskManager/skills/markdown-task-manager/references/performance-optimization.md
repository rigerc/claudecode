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