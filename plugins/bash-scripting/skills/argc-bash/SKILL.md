---
name: argc-bash
# IMPORTANT: Keep description on ONE line for Claude Code compatibility
# prettier-ignore
description: Use when creating Bash CLIs with argc framework. Provides expertise in argc comment tags, parameter types, dynamic values, nested subcommands, and Argcfile.sh project automation.
---

# Argc Bash

Build CLIs using argc's comment-based parameter system.

## Quick Start

```bash
#!/usr/bin/env bash
# @describe File transfer CLI

# @cmd Upload file to server
# @flag -f --force              Override existing file
# @option -t --timeout <SEC>    Timeout in seconds
# @arg target!                  File to upload
upload() {
    echo "Uploading: $argc_target (force=$argc_force)"
}

eval "$(argc --argc-eval "$0" "$@")"
```

## Core Concepts

- **Comment Tags**: `@cmd`, `@arg`, `@option`, `@flag`, `@env` define CLI
- **Variables**: Access as `$argc_<name>` (e.g., `$argc_target`)
- **Modifiers**: `!`=required, `*`=multiple, `=val`=default, `[a|b]`=choices
- **Eval Line**: Always end with `eval "$(argc --argc-eval "$0" "$@")"`

## Reference Files

- [references/quick-reference.md](references/quick-reference.md) - Parameter syntax cheatsheet
- [references/framework-guide.md](references/framework-guide.md) - Complete documentation
- [references/argcfile-patterns.md](references/argcfile-patterns.md) - Project automation

<!--
PROGRESSIVE DISCLOSURE GUIDELINES:
- Keep this file ~50 lines total (max ~150 lines)
- Use 1-2 code blocks only (recommend 1)
- Keep description <200 chars for Level 1 efficiency
- Move detailed docs to references/ for Level 3 loading
- This is Level 2 - quick reference ONLY, not a manual
-->
