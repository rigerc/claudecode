# Slash Commands Creator

Use this Skill to create, review, and maintain Claude Code custom slash commands
based on our official slash command guidelines.

## Purpose

Standardize how we define `/...` commands so they:
- Follow the documented syntax and frontmatter format
- Use arguments correctly (`$ARGUMENTS`, `$1`, `$2`, etc.)
- Respect `allowed-tools` constraints
- Integrate cleanly as project or personal commands

## How to use this Skill

When I ask you to create or update a slash command, you should:

1. Confirm command type
   - Ask whether it should be:
     - Project command (`.claude/commands/`)
     - Personal command (`~/.claude/commands/`)
     - Plugin command (`commands/` inside a plugin)

2. Design the command
   - Name: derive from desired `/command-name`
   - Behavior: restate what the command should do in 1–3 lines
   - Arguments:
     - Decide between:
       - `$ARGUMENTS` for free-form input
       - `$1`, `$2`, ... for structured parameters
     - Suggest `argument-hint` where appropriate
   - Tools:
     - Propose minimal `allowed-tools` set if bash execution is needed
     - Default to read-only unless write/exec is clearly required

3. Generate the file
   - Output a complete `.md` definition, following:

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

4. Validate against the reference

Ensure each generated command:
- Conforms to the syntax described in:
  - `@plugins/claude-code-development/skills/working-with-claude-code/references/slash-commands.md`
- Is concise, deterministic, and safe
- Avoids unsupported patterns (e.g., wildcards in MCP permissions)
- Uses plugin prefixes (`/plugin-name:command`) only when needed

## Examples

### Simple reusable review command

```markdown
---
description: Review code for correctness, security, and clarity
---

Review this code for:
- Logical and edge-case bugs
- Security issues
- Readability and maintainability problems
Provide concrete, actionable suggestions.
```

### Structured PR review command

```markdown
---
description: Review a pull request by number
argument-hint: [pr-number] [priority] [assignee]
---

Review PR #$1 with priority $2 and assign to $3.
Focus on:
- Security vulnerabilities
- Performance regressions
- Test coverage and failure risks
Return a concise, structured summary.
```

When asked to "create a slash command":
- Follow the workflow above
- Show the final `.md` content ready to be saved in the correct directory
- Do not auto-create files unless explicitly instructed
