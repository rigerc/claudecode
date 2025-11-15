---
name: gum
# IMPORTANT: Keep description on ONE line for Claude Code compatibility
# prettier-ignore
description: Use when working with charmbracelet/gum for creating interactive, glamorous shell scripts. Provides expertise in gum commands for input, selection, styling, and user interaction.
---

# Gum

## Quick Start

Create an interactive git commit prompt with gum:

```bash
TYPE=$(gum choose "fix" "feat" "docs" "style" "refactor" "test")
SCOPE=$(gum input --placeholder "scope")
SUMMARY=$(gum input --placeholder "Summary of changes")
DESCRIPTION=$(gum write --placeholder "Detailed description (Ctrl+D to finish)")
gum confirm "Commit changes?" && git commit -m "$TYPE($SCOPE): $SUMMARY" -m "$DESCRIPTION"
```

## Core Principles

- **Composable**: Each gum command does one thing well and can be combined with others
- **No Code Required**: Create interactive TUIs without writing Go or complex scripts
- **Themeable**: Customize appearance via flags or environment variables

## Common Commands

- `gum choose` - Select from list of options
- `gum input` - Single-line text input (supports --password)
- `gum write` - Multi-line text input (Ctrl+D to finish)
- `gum confirm` - Yes/no confirmation (exits 0 for yes, 1 for no)
- `gum filter` - Fuzzy search/filter items
- `gum spin` - Show spinner while running commands
- `gum style` - Apply colors, borders, padding to text
- `gum format` - Process markdown, templates, emojis

## Reference Files

For detailed documentation, see:
- [command-reference.md](references/command-reference.md) - All gum commands with examples
- [styling-guide.md](references/styling-guide.md) - Theming and customization

## Notes

- Installation: `brew install gum` or `go install github.com/charmbracelet/gum@latest`
- All commands support customization via `--flags` or `$GUM_*` environment variables
- Combine with standard Unix tools for powerful interactive scripts

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
