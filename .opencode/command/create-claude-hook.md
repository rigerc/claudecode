---
description: "Set up Claude Code hooks for automation and validation workflows"
argument-hint: "<hook-type> <hook-name> <description>"
allowed-tools: "Write, Edit, Read, Bash(mkdir, ls, cat, test)"

---

# Create Claude Hook

Sets up Claude Code hooks for automating validation, security checks, and workflow automation. Hooks allow you to execute custom scripts before or after tool use events. Before proceeding to planning or implementation, research using Context7 (`anthropics/claude-code`).


## Usage:

`/create-claude-hook <hook-type> <hook-name> "<description>"`

## Parameters:

- **hook-type**: Type of hook (PreToolUse, PostToolUse, UserPromptSubmit, Notification, Stop, SubagentStop, PreCompact, SessionStart, SessionEnd)
- **hook-name**: Descriptive name for the hook (e.g., security-scan, lint-check, deploy-validation)
- **description**: What the hook does and when it should trigger

## Hook Types:

### PreToolUse
Executes before a tool is used. Ideal for:
- Security validation
- Permission checks
- Input sanitization
- Resource availability checks

### PostToolUse
Executes after a tool completes. Ideal for:
- Code formatting
- Test execution
- Notification sending
- Cleanup operations

### UserPromptSubmit
Processes user prompts before Claude handles them. Ideal for:
- Prompt validation and filtering
- Context injection
- Audit logging
- Content moderation

### Notification
Triggers when Claude needs permission or input has been idle. Ideal for:
- Custom permission handling
- Idle timeout management
- User interaction workflows

### Stop
Runs when the main agent response finishes. Ideal for:
- Completion notifications
- Result processing
- Session cleanup
- AI-generated feedback

### SubagentStop
Runs when sub-agent responses finish. Ideal for:
- Sub-agent result validation
- Parallel task coordination
- Workflow synchronization

### PreCompact
Executes before compact operations (manual or automatic). Ideal for:
- Context preservation
- Selective compaction
- Data archiving

### SessionStart
Manages session initialization. Ideal for:
- Environment setup
- Context loading
- Project initialization
- Development environment preparation

### SessionEnd
Manages session termination. Ideal for:
- Cleanup operations
- State saving
- Resource release
- Session summary generation

## Process:

1. **Hook Configuration Analysis**
   - Determine appropriate hook type and trigger conditions
   - Identify required tools and permissions
   - Plan validation logic and error handling

2. **Hook File Creation**
   - Create hook configuration in `.claude/hooks.json` or project settings
   - Set up hook script or command
   - Configure matcher patterns for tool/command selection

3. **Implementation Setup**
   - Create hook script or validation logic
   - Set up proper file permissions
   - Test hook functionality

4. **Documentation**
   - Document hook purpose and behavior
   - Provide usage examples
   - Include troubleshooting information

## Examples:

```bash
# Create a security validation hook
/create-claude-hook PreToolUse security-scan "Validate commands for security risks before execution"

# Create a code formatting hook
/create-claude-hook PostToolUse auto-format "Automatically format code after file edits"

# Create a prompt validation hook
/create-claude-hook UserPromptSubmit prompt-filter "Filter and validate user prompts for security"

# Create a session initialization hook
/create-claude-hook SessionStart context-loader "Load project context and development environment"

# Create a completion notification hook
/create-claude-hook Stop completion-notifier "Send notifications when tasks complete"
```

## Hook Configuration Structure:

The command creates hooks in this format:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/validation-script.sh",
            "description": "Security validation for bash commands",
            "timeout": 30
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "npm run lint -- --fix $FILE_PATH",
            "description": "Auto-format and lint code after edits",
            "timeout": 60
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python3 /path/to/prompt-validator.py",
            "description": "Validate user prompts for security"
          }
        ]
      }
    ]
  }
}
```

### Configuration Options:

- **matcher**: Tool pattern to match (empty string matches all tools)
- **type**: Always "command" for shell command execution
- **command**: Shell command to execute
- **description**: Human-readable description of hook purpose
- **timeout**: Optional timeout in seconds (default: 30)

## Hook Input Schema:

Hooks receive JSON input via stdin with the following structure:

```json
{
  "session_id": "uuid-string",
  "transcript_path": "/path/to/transcript.json",
  "cwd": "/current/working/directory",
  "permission_mode": "acceptEdits|prompt",
  "tool_name": "Bash|Edit|Read|Write|...",
  "tool_input": {
    // Tool-specific input data
  },
  "event_specific_data": {
    // Event-specific data varies by hook type
  }
}
```

### Tool-Specific Input Examples:

**Bash Tool Input:**
```json
{
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm install",
    "timeout": 120000
  }
}
```

**Edit Tool Input:**
```json
{
  "tool_name": "Edit",
  "tool_input": {
    "file_path": "/path/to/file.js",
    "old_string": "old code",
    "new_string": "new code"
  }
}
```

**UserPromptSubmit Input:**
```json
{
  "prompt": "Help me debug this issue",
  "session": {
    "id": "uuid-string"
  }
}
```

## Available Environment Variables:

Hooks can access these environment variables:
- `$CLAUDE_PROJECT_DIR`: Current project directory
- `$CLAUDE_PLUGIN_ROOT`: Plugin root directory (if applicable)
- `$FILE_PATH`: Path to file being edited (for Edit tools)
- `$COMMAND`: Command being executed (for Bash tools)
- `$TOOL_NAME`: Name of the tool being used

## Exit Code Reference:

Hooks communicate results through exit codes:

- **Exit Code 0**: Success - Operation continues normally
- **Exit Code 1**: Warning - Operation continues but stderr is shown to user
- **Exit Code 2**: Blocking Error - Operation is halted, stderr shown to user

### Exit Code Usage Examples:

```python
#!/usr/bin/env python3
import json
import sys

# Read hook input
input_data = json.load(sys.stdin)

# Example: Block dangerous commands
if input_data.get("tool_name") == "Bash":
    command = input_data.get("tool_input", {}).get("command", "")
    if "rm -rf" in command:
        print("BLOCKED: Dangerous command detected", file=sys.stderr)
        sys.exit(2)  # Block operation

# Example: Warning for deprecated syntax
if "deprecated_function()" in command:
    print("WARNING: Using deprecated function", file=sys.stderr)
    sys.exit(1)  # Show warning but continue

sys.exit(0)  # Success
```

## Hook Output Options:

### Standard Output (stdout)
- Informational messages
- Data to be logged
- Non-blocking feedback

### Standard Error (stderr)
- Warning messages (exit code 1)
- Error messages (exit code 2)
- Blocking notifications

### JSON Output (Advanced)
For advanced control, hooks can output JSON responses:

```json
{
  "status": "success|warning|error",
  "message": "Human-readable message",
  "data": {
    "additional": "context data"
  }
}
```

## Real Hook Examples:

### Example 1: PreToolUse Security Validation Hook

```python
#!/usr/bin/env python3
import json
import sys
import re

def is_dangerous_command(command):
    """Check for dangerous command patterns."""
    dangerous_patterns = [
        r'rm\s+-rf\s+/',           # rm -rf /
        r'sudo\s+rm',              # sudo rm
        r'chmod\s+777',           # chmod 777
        r'curl.*\|\s*sh',         # curl | sh
    ]

    for pattern in dangerous_patterns:
        if re.search(pattern, command, re.IGNORECASE):
            return True
    return False

# Read JSON input from stdin
input_data = json.load(sys.stdin)
tool_name = input_data.get('tool_name', '')
tool_input = input_data.get('tool_input', {})

# Check Bash commands for security issues
if tool_name == 'Bash':
    command = tool_input.get('command', '')
    if is_dangerous_command(command):
        print(f"BLOCKED: Dangerous command detected: {command}", file=sys.stderr)
        sys.exit(2)  # Block execution

sys.exit(0)  # Allow execution
```

### Example 2: UserPromptSubmit Logging Hook

```python
#!/usr/bin/env python3
import json
import sys
from pathlib import Path
from datetime import datetime

# Read input
input_data = json.load(sys.stdin)
prompt = input_data.get('prompt', '')
session_id = input_data.get('session', {}).get('id', 'unknown')

# Log to file
log_dir = Path('logs')
log_dir.mkdir(exist_ok=True)
log_file = log_dir / 'prompts.json'

log_entry = {
    'timestamp': datetime.utcnow().isoformat() + 'Z',
    'session_id': session_id,
    'prompt': prompt[:500],  # Truncate long prompts
    'prompt_length': len(prompt)
}

# Append to log file
if log_file.exists():
    logs = json.loads(log_file.read_text())
else:
    logs = []

logs.append(log_entry)
log_file.write_text(json.dumps(logs, indent=2))

print(f"Logged prompt from session {session_id}")
sys.exit(0)
```

### Example 3: PostToolUse Auto-Formatting Hook

```bash
#!/bin/bash
# PostToolUse hook for automatic code formatting

# Read JSON input
input_json=$(cat)
file_path=$(echo "$input_json" | jq -r '.tool_input.file_path // empty')

# Only process certain file types
case "$file_path" in
    *.js|*.ts|*.jsx|*.tsx)
        # JavaScript/TypeScript formatting
        if command -v prettier >/dev/null 2>&1; then
            prettier --write "$file_path"
            echo "Formatted JavaScript/TypeScript file: $file_path"
        fi
        ;;
    *.py)
        # Python formatting
        if command -v black >/dev/null 2>&1; then
            black "$file_path"
            echo "Formatted Python file: $file_path"
        fi
        ;;
    *.go)
        # Go formatting
        if command -v gofmt >/dev/null 2>&1; then
            gofmt -w "$file_path"
            echo "Formatted Go file: $file_path"
        fi
        ;;
esac

exit 0
```

### Example 4: SessionStart Context Loading Hook

```python
#!/usr/bin/env python3
import json
import sys
import subprocess
from pathlib import Path

# Read session start input
input_data = json.load(sys.stdin)
source = input_data.get('source', 'unknown')
cwd = input_data.get('cwd', '')

# Only load context for new sessions
if source == 'startup':
    context_lines = []

    # Get git status
    try:
        result = subprocess.run(
            ['git', 'status', '--short'],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0 and result.stdout.strip():
            context_lines.append("## Git Status")
            context_lines.append("```")
            context_lines.append(result.stdout)
            context_lines.append("```")
    except:
        pass

    # Read context files
    for context_file in ['README.md', 'CONTEXT.md', 'TODO.md']:
        file_path = Path(cwd) / context_file
        if file_path.exists():
            content = file_path.read_text()[:1000]  # Limit length
            context_lines.append(f"\n## {context_file}")
            context_lines.append(content)

    # Output context for Claude to see
    if context_lines:
        print("\n## Development Context Loaded")
        print("\n".join(context_lines))

sys.exit(0)
```

### Example 5: Stop Hook with Completion Notification

```python
#!/usr/bin/env python3
import json
import sys
import subprocess
from datetime import datetime

# Read stop hook input
input_data = json.load(sys.stdin)

# Generate completion message
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
message = f"Task completed at {timestamp}"

# Try to send notification (macOS/Linux)
try:
    if sys.platform == "darwin":
        # macOS notification
        subprocess.run([
            'osascript', '-e',
            f'display notification "{message}" with title "Claude Code"'
        ], check=False)
    elif sys.platform.startswith("linux"):
        # Linux notification (requires libnotify)
        subprocess.run([
            'notify-send', 'Claude Code', message
        ], check=False)
except:
    pass

print(f"✓ {message}")
sys.exit(0)
```

## Best Practices:

1. **Keep hooks fast** - Avoid long-running operations that block workflow
2. **Handle errors gracefully** - Don't break the main workflow
3. **Use descriptive names** - Make hook purposes clear
4. **Test thoroughly** - Ensure hooks work as expected
5. **Document behavior** - Include clear descriptions and examples
6. **Consider permissions** - Ensure hooks have necessary tool access
7. **Validate inputs** - Always validate hook input JSON structure
8. **Use appropriate exit codes** - 0 for success, 1 for warnings, 2 to block
9. **Log for debugging** - Include helpful logging for troubleshooting
10. **Handle timeouts** - Set appropriate timeouts for hook operations

## Notes:

- Hooks can be configured at global level (`~/.claude/settings.json`) or project level (`.claude/settings.json`, or `.claude/settings.local.json`)
- Project-level hooks override global hooks
- Use `matcher` patterns to selectively apply hooks to specific tools or commands
- Hook scripts should be executable and have proper error handling
- Test hooks in safe environments before deploying to critical workflows
- Hooks receive JSON input via stdin and should use appropriate exit codes
- Consider security implications - hooks execute arbitrary shell commands
