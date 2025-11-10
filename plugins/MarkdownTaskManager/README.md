# MarkdownTaskManager Plugin

A comprehensive AI-driven task management system that brings discipline and transparency to your development workflow. This plugin implements a Kanban-style task management system using local Markdown files, providing complete traceability of AI work through strict task creation and documentation practices.

**🔗 External Integration**: This plugin is designed to work seamlessly with the [MarkdownTaskManager web application](https://github.com/ioniks/MarkdownTaskManager/tree/master), providing a powerful drag-and-drop interface for managing your tasks.

## 🌟 Key Features

### 📋 **Kanban-Style Task Management**
- **Four-Column Board**: 📝 To Do → 🚀 In Progress → 👀 In Review → ✅ Done
- **Visual Workflow**: Clear progression of tasks through development stages
- **Drag-and-Drop Interface**: Web-based board from the external GitHub repository
- **Archive System**: Separate storage for completed tasks

### 🤖 **AI-Driven Workflow**
- **Task-Before-Coding**: Enforces the golden rule of planning before implementation
- **Complete Documentation**: Requires detailed notes and results for every task
- **Git Integration**: References tasks in commits and branches for full traceability
- **Multi-AI Support**: Compatible with Claude, ChatGPT, Copilot, and other AI assistants

### 🔧 **Advanced Task Features**
- **Auto-Generated IDs**: Unique TASK-XXX numbering system
- **Rich Metadata**: Priority, category, user assignments, dates, and tags
- **Subtask Support**: Break down complex work into manageable steps
- **Progress Tracking**: Real-time status updates and completion notes
- **Search & Filter**: Organize tasks by category, assignee, or tags

### 🚀 **Zero-Config Setup**
- **Automatic Installation**: SessionStart hooks create required files
- **Template System**: Pre-built templates for immediate use
- **External Integration**: Automatically downloads web interface
- **Skip Existing**: Preserves your current configuration

## 🛠️ Getting Started

### Automatic Setup (Recommended)
The plugin automatically configures itself when installed:

1. **SessionStart Hook**: Creates required files if they don't exist
2. **Template Creation**: Copies `kanban.md`, `archive.md`, and `AI_WORKFLOW.MD`
3. **External Download**: Fetches `task-manager.html` from GitHub repository
4. **AI Instructions**: Sets up `CLAUDE.md` with task manager references

### Manual Setup
If automatic setup fails, create these files manually:

```bash
# Create basic structure
touch kanban.md archive.md AI_WORKFLOW.MD

# Download web interface (optional)
curl -o task-manager.html https://raw.githubusercontent.com/ioniks/MarkdownTaskManager/master/task-manager.html
```

### First Use
1. **Enable the Skill**: Use `skill: "markdown-task-manager"` in your Claude session
2. **Create First Task**: Ask Claude to create a task for your next feature
3. **Follow the Workflow**: Move tasks through columns as work progresses
4. **Document Everything**: Add completion notes and modified file lists

## 📋 Task Management System

### Task Structure
Each task follows a strict format for compatibility with the web interface:

```markdown
- 📝 **TASK-042**: Implement user authentication system <!-- Status: To Do -->
  - **Priority**: High 🚨
  - **Category**: Feature Development
  - **Assignee**: @developer-name
  - **Created**: 2025-01-10
  - **Due**: 2025-01-15
  - **Tags**: #authentication, #security, #api
  - **Subtasks**:
    - [ ] Design authentication flow
    - [ ] Implement JWT tokens
    - [ ] Add login/logout endpoints
  - **Notes**: Initial implementation using OAuth 2.0
  - **Result**: [Added after completion]
  - **Modified files**: [Added after completion]
```

### Task Lifecycle

#### 1. **Creation** 📝
- Unique auto-generated ID (TASK-XXX)
- Initial placement in "To Do" column
- Required metadata fields filled
- Subtasks and initial notes added

#### 2. **In Progress** 🚀
- Status emoji changes to 🚀
- Subtasks tracked as completed
- Progress notes added
- Active development phase

#### 3. **In Review** 👀
- Status emoji changes to 👀
- Ready for code review or testing
- Additional notes added as needed
- Preparation for completion

#### 4. **Done** ✅
- Status emoji changes to ✅
- Final result documentation added
- List of modified files included
- Task stays in Done until archived

#### 5. **Archive** 📦
- Moved to `archive.md` on user request
- Never auto-archived (preserves visibility)
- Maintains complete history
- Searchable for future reference

### Configuration
The `kanban.md` file includes configuration for task ID management:

```markdown
<!-- Config: Last Task ID: 42 -->
```

This auto-increments with each new task but can be manually adjusted.

## 🔗 External Integration

### GitHub Repository
This plugin integrates with [ioniks/MarkdownTaskManager](https://github.com/ioniks/MarkdownTaskManager/tree/master):

- **Web Interface**: `task-manager.html` provides drag-and-drop Kanban board
- **Format Compatibility**: HTML parser understands specific Markdown structure
- **Advanced Features**: Priority badges, filters, multilingual support
- **Local Usage**: Works entirely offline after initial download

### Git Workflow Integration
Enhance your version control with task references:

```bash
# Feature branches
git checkout -b feature/TASK-042-user-authentication

# Commits with task references
git commit -m "feat: implement JWT authentication (TASK-042 - 2/3)"

# Pull requests
git commit -m "docs: update API documentation (TASK-042 - 3/3) 🤖 Generated with [Claude Code]"
```

### AI Assistant Integration
The plugin works with multiple AI assistants:

- **Claude**: Native skill integration with automatic setup
- **ChatGPT**: Manual task creation following the format
- **GitHub Copilot**: Task comments in code for context
- **Others**: Compatible with any AI that follows Markdown format

## 📁 File Structure

### Required Files

#### `kanban.md` - Active Task Board
```markdown
# Kanban Board

<!-- Config: Last Task ID: 42 -->

## 📝 To Do (3)
## 🚀 In Progress (1)
## 👀 In Review (2)
## ✅ Done (15)
```

#### `archive.md` - Completed Tasks
```markdown
# Archived Tasks

## 📦 Completed Tasks (127)

### 2025-01
- ✅ **TASK-041**: Fix login redirect issue...
- ✅ **TASK-040**: Add user profile page...
```

#### `AI_WORKFLOW.MD` - Workflow Guidelines
Comprehensive rules and guidelines for task management, including:
- Golden rules and compliance requirements
- Format specifications and examples
- Git integration patterns
- Best practices and anti-patterns

#### `task-manager.html` - Web Interface
Automatically downloaded from GitHub repository provides:
- Drag-and-drop Kanban board
- Task filtering and search
- Priority badges and visual indicators
- Multilingual support

### Optional Files

#### `CLAUDE.md` - AI Instructions
Auto-generated template containing:
- Task manager skill reference
- Workflow rules specific to AI assistants
- Format compliance guidelines

#### Custom AI Configuration Files
- `ChatGPT.md`, `Copilot.md`, etc.
- Customized instructions for different AI assistants
- Consistent format across all tools

## 💡 Usage Examples

### Creating Your First Task
```
Claude, please create a task for implementing user registration
```

Result:
```markdown
- 📝 **TASK-043**: Implement user registration system <!-- Status: To Do -->
  - **Priority**: High 🚨
  - **Category**: Feature Development
  - **Assignee**: @claude
  - **Created**: 2025-01-10
  - **Tags**: #authentication, #user-management
  - **Subtasks**:
    - [ ] Create registration form
    - [ ] Implement email validation
    - [ ] Add password strength requirements
    - [ ] Create user database model
  - **Notes**: Need to integrate with existing authentication system
```

### Completing a Task
When Claude finishes working on a task, it automatically:
1. Updates the status to ✅ Done
2. Adds completion notes
3. Lists all modified files
4. Documents any challenges or solutions

Example result:
```markdown
  - **Result**: Successfully implemented user registration with email validation and password strength requirements. Integrated with existing JWT authentication system. Added comprehensive error handling and validation messages.
  - **Modified files**:
    - `src/controllers/authController.js` (added register method)
    - `src/models/User.js` (new user model)
    - `src/middleware/validation.js` (email and password validation)
    - `routes/auth.js` (registration endpoint)
```

### Using the Web Interface
1. Open `task-manager.html` in your browser
2. Drag tasks between columns to update status
3. Use filters to view specific categories or assignees
4. Search tasks by title, tags, or content
5. Export data for reporting or backup

## 🎯 Best Practices

### Golden Rules
1. **Create Tasks BEFORE Coding**: Never start work without a task
2. **Document Everything**: Add detailed notes and results
3. **Follow Format Strictly**: No nested headings or custom formatting
4. **Keep Tasks in Done**: Archive only when explicitly requested

### Format Compliance
- Use exact field names (`**Priority**:**, `**Category**:**, etc.)
- Never use `##` or `###` inside task descriptions
- Maintain the comment format for status tracking
- Preserve the configuration section in `kanban.md`

### Workflow Tips
- **Break Down Large Tasks**: Use subtasks for complex features
- **Update Progress**: Mark subtasks as completed during development
- **Be Specific**: Include detailed descriptions and acceptance criteria
- **Tag Consistently**: Use standardized tags for better organization

### Git Integration
- Reference tasks in commits: `(TASK-XXX - n/m)`
- Use descriptive branch names: `feature/TASK-XXX-description`
- Include task context in pull requests
- Maintain traceability throughout development

## 🔧 Advanced Features

### Archive Management
```markdown
# Move completed tasks to archive
Claude, please archive tasks TASK-038, TASK-039, and TASK-040
```

### Task Search and Filtering
The web interface supports:
- **Text Search**: Find tasks by title, description, or notes
- **Tag Filtering**: View tasks with specific hashtags
- **Category Filtering**: Show tasks by category
- **Assignee Filtering**: View tasks assigned to specific users
- **Status Filtering**: Focus on specific columns

### Multi-Language Support
The web interface supports multiple languages:
- English (default)
- Spanish
- French
- German
- Chinese

## ❓ Troubleshooting

### Common Issues

#### Tasks Not Showing in Web Interface
- **Check Format**: Ensure strict adherence to the task structure
- **Verify Status**: Confirm the `<!-- Status: Column -->` comment is correct
- **Validate Headers**: Use exact column headers in `kanban.md`

#### Auto-Incrementing IDs Not Working
- **Check Config**: Verify the `<!-- Config: Last Task ID: XXX -->` line exists
- **Update Manually**: Set the correct ID number if it gets out of sync
- **File Permissions**: Ensure write permissions on `kanban.md`

#### Hook Setup Failed
- **Manual Setup**: Create files manually using the templates provided
- **Check Permissions**: Verify Claude Code has permission to create files
- **Reinstall Plugin**: Remove and reinstall the plugin to trigger hooks again

### Format Validation
Use this checklist to validate task format:

- [ ] Task ID format: `TASK-XXX` (where XXX is a number)
- [ ] Status emoji matches column: 📝, 🚀, 👀, ✅
- [ ] Status comment: `<!-- Status: ColumnName -->`
- [ ] Required fields: Priority, Category, Created, Tags
- [ ] No nested headings within task descriptions
- [ ] Proper markdown list formatting with `- ` prefix

### Getting Help
- **Check AI_WORKFLOW.MD**: Contains detailed guidelines and examples
- **Review Web Interface**: Open `task-manager.html` to understand expected format
- **Validate Configuration**: Ensure `kanban.md` has the correct setup
- **Test with Simple Task**: Create a minimal task to test the system

## 🚀 Quick Reference

### Essential Commands
```
# Create a new task
"Create a task for [feature description]"

# Update task status
"Move TASK-XXX to In Progress"

# Archive completed tasks
"Archive tasks TASK-XXX, TASK-XXX"

# Search tasks
"Show me all tasks with #bug tag"
```

### File Locations
- `kanban.md` - Active tasks board
- `archive.md` - Completed tasks
- `AI_WORKFLOW.MD` - Workflow guidelines
- `task-manager.html` - Web interface (auto-downloaded)
- `.claude-plugin/` - Plugin configuration

### External Links
- **GitHub Repository**: https://github.com/ioniks/MarkdownTaskManager/tree/master
- **Web Interface**: `task-manager.html` (local file)
- **Plugin Source**: `/plugins/MarkdownTaskManager/`

---

**🎉 Enjoy transparent, organized, and traceable task management with MarkdownTaskManager!**