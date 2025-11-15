---
name: fish-shell
# IMPORTANT: Keep description on ONE line for Claude Code compatibility
# prettier-ignore
description: Use when working with Fish Shell for interactive usage, scripting, configuration, automation, and intelligent completions
---

# Fish Shell

## Quick Start

Fish is a modern, user-friendly shell with intelligent completions and syntax highlighting.

```fish
# Set Fish as default shell
chsh -s /usr/bin/fish

# Create custom prompt function
function fish_prompt
    set_color $fish_color_cwd
    echo -n (prompt_pwd)
    set_color normal
    echo -n ' > '
end

# Save function permanently
funcsave fish_prompt
```

## Core Principles

- **Usability First**: Fish works out of the box with no configuration required
- **Smart Completions**: Context-aware tab completions for commands, files, and options
- **Clean Syntax**: Simple, readable scripting language without cryptic symbols
- **Web Configuration**: `fish_config` provides browser-based customization

## Common Patterns

### Function Creation

Define reusable shell functions for automation and aliases. Use `funcsave` to persist across sessions.

### Configuration Management

Set environment variables and shell preferences in `~/.config/fish/config.fish`. Use universal variables for persistent settings.

## Reference Files

For detailed documentation, see:
- [references/fish-shell-guide.md](references/fish-shell-guide.md) - Complete Fish Shell guide
- [references/](references/) - Additional examples and patterns

## Notes

- Fish syntax differs from Bash - avoid `$(( ))` arithmetic, use `math` command instead
- Use `string` command for text manipulation instead of external tools like `sed`/`awk`
- Functions are the preferred way to create aliases with parameters

<!--
PROGRESSIVE DISCLOSURE GUIDELINES:
- Keep this file ~50 lines total (max ~150 lines)
- Use 1-2 code blocks only (recommend 1)
- Keep description <200 chars for Level 1 efficiency
- Move detailed docs to references/ for Level 3 loading
- This is Level 2 - quick reference ONLY, not a manual

LLM WORKFLOW (when editing this file):
1. Write/edit SKILL.md
2. Format (if formatter available)
3. Run: claude-skills-cli validate <path>
4. If multi-line description warning: run claude-skills-cli doctor <path>
5. Validate again to confirm
-->
