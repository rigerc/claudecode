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