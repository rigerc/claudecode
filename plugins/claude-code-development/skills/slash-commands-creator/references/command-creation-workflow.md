# Slash Command Creation Workflow

## Step-by-Step Process

When creating or updating a slash command, follow this workflow:

### 1. Confirm Command Type

Ask whether the command should be:
- **Project command**: `.claude/commands/` (shared with team)
- **Personal command**: `~/.claude/commands/` (local to user)
- **Plugin command**: `commands/` inside a plugin

### 2. Design the Command

**Name**: Derive from desired `/command-name`

**Behavior**: Restate what the command should do in 1–3 lines

**Arguments**:
- Decide between:
  - `$ARGUMENTS` for free-form input
  - `$1`, `$2`, ... for structured parameters
- Suggest `argument-hint` where appropriate

**Tools**:
- Propose minimal `allowed-tools` set if bash execution is needed
- Default to read-only unless write/exec is clearly required

### 3. Generate the File

Output a complete `.md` definition, following this template:

```markdown
---
description: Brief, clear description of what the command does
argument-hint: [optional argument usage hint]
allowed-tools: [optional, e.g. Bash(git status:*), Bash(git diff:*)]
model: [optional override; otherwise inherit]
---

# <Command label or instructions>

<Exact instructions Claude should follow when this command runs.>
Use $ARGUMENTS and/or $1, $2 etc. as needed.
Include any context gathering, file references with @, or bash snippets with !`...`.
```

### 4. Validate Against Reference

Ensure each generated command:
- Conforms to the syntax described in:
  - `@plugins/claude-code-development/skills/working-with-claude-code/references/slash-commands.md`
- Is concise, deterministic, and safe
- Avoids unsupported patterns (e.g., wildcards in MCP permissions)
- Uses plugin prefixes (`/plugin-name:command`) only when needed

## Important Notes

When asked to "create a slash command":
- Follow the workflow above
- Show the final `.md` content ready to be saved in the correct directory
- Do not auto-create files unless explicitly instructed
