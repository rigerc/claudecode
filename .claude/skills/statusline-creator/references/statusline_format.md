# Statusline Format Reference

Complete guide to statusline configuration format, variables, ANSI codes, and customization options for Claude Code.

## Configuration Structure

Statuslines are configured in `~/.claude/settings.json`:

```json
{
  "statusline": {
    "format": "your statusline string here"
  }
}
```

## Dynamic Variables

Variables that can be embedded in statuslines using the `{variable}` syntax:

### Git Variables

- `{git_branch}` - Current git branch name
- `{git_status}` - Short status indicator (✓ for clean, symbols for changes)
- `{git_ahead}` - Commits ahead of remote
- `{git_behind}` - Commits behind remote
- `{git_modified}` - Count of modified files
- `{git_staged}` - Count of staged files
- `{git_untracked}` - Count of untracked files

### System Variables

- `{pwd}` - Current working directory (full path)
- `{pwd_short}` - Current directory name only
- `{user}` - Current username
- `{host}` - Hostname
- `{time}` - Current time (HH:MM:SS)
- `{date}` - Current date (YYYY-MM-DD)
- `{load}` - System load average
- `{memory}` - Memory usage percentage

### Environment Variables

- `{env:VAR_NAME}` - Any environment variable
- Example: `{env:PROJECT_NAME}` reads $PROJECT_NAME

## ANSI Color Codes

### Basic Colors (30-37 for foreground, 40-47 for background)

```
\x1b[30m  Black text
\x1b[31m  Red text
\x1b[32m  Green text
\x1b[33m  Yellow text
\x1b[34m  Blue text
\x1b[35m  Magenta text
\x1b[36m  Cyan text
\x1b[37m  White text
\x1b[0m   Reset to default
```

### Bright Colors (90-97)

```
\x1b[90m  Bright black (gray)
\x1b[91m  Bright red
\x1b[92m  Bright green
\x1b[93m  Bright yellow
\x1b[94m  Bright blue
\x1b[95m  Bright magenta
\x1b[96m  Bright cyan
\x1b[97m  Bright white
```

### Text Styles

```
\x1b[1m   Bold
\x1b[2m   Dim
\x1b[3m   Italic
\x1b[4m   Underline
\x1b[7m   Reverse (swap fg/bg)
\x1b[22m  Normal intensity
\x1b[23m  Not italic
\x1b[24m  Not underlined
```

### 256 Color Mode

```
\x1b[38;5;COLORm    Foreground color (COLOR = 0-255)
\x1b[48;5;COLORm    Background color (COLOR = 0-255)
```

Examples:
- `\x1b[38;5;208m` - Orange text
- `\x1b[38;5;27m` - Blue text
- `\x1b[48;5;240m` - Dark gray background

### RGB True Color Mode

```
\x1b[38;2;R;G;Bm    Foreground RGB
\x1b[48;2;R;G;Bm    Background RGB
```

Examples:
- `\x1b[38;2;255;100;50m` - Orange text
- `\x1b[48;2;30;30;30m` - Dark background

## Shell Command Substitution

Execute shell commands dynamically using `$(command)` or `` `command` ``:

```bash
# Git branch from command
"$(git branch --show-current 2>/dev/null)"

# Time from command
"$(date +%H:%M:%S)"

# Custom script output
"$(~/.claude/scripts/my_custom_info.sh)"
```

**Important**: Ensure commands are fast (<100ms) to avoid statusline lag.

## Unicode Symbols

Common symbols used in statuslines:

### Status Indicators
- ✓ (U+2713) - Check mark (clean/success)
- ✗ (U+2717) - X mark (error/failed)
- ⚠ (U+26A0) - Warning sign
- ● (U+25CF) - Bullet (indicator)
- ○ (U+25CB) - Circle outline

### Git Symbols
- ± (U+00B1) - Modified files
- + (U+002B) - Added files
- − (U+2212) - Deleted files
- ↑ (U+2191) - Ahead of remote
- ↓ (U+2193) - Behind remote
- ⇡ (U+21E1) - Push needed
- ⇣ (U+21E3) - Pull needed
- ⎇ (U+2387) - Branch symbol
- ⌥ (U+2325) - Alternative branch

### Separators
- │ (U+2502) - Vertical line
- ┃ (U+2503) - Heavy vertical line
- ║ (U+2551) - Double vertical line
- ❯ (U+276F) - Triangle right
- ❮ (U+276E) - Triangle left
- » (U+00BB) - Right guillemet
- « (U+00AB) - Left guillemet
- ⟫ (U+27EB) - Mathematical right angle
- ⟪ (U+27EA) - Mathematical left angle

### Time/System
- ⏰ (U+23F0) - Clock
- ⚡ (U+26A1) - Lightning (load/performance)
- 💾 (U+1F4BE) - Floppy disk (storage)
- 🖥 (U+1F5A5) - Desktop computer

## Example Patterns

### Minimal
```
{pwd_short} {git_branch}
```
Output: `my-project main`

### Git-Focused
```
\x1b[36m{git_branch}\x1b[0m {git_status} \x1b[90m{pwd}\x1b[0m
```
Output: `main ✓ ~/workspace/project` (with colors)

### Full-Featured
```
\x1b[1m{user}@{host}\x1b[0m │ \x1b[34m{pwd_short}\x1b[0m │ \x1b[32m⎇ {git_branch}\x1b[0m {git_status} │ \x1b[90m{time}\x1b[0m
```
Output: `user@machine │ project │ ⎇ main ✓ │ 14:23:45`

### Powerline-Style
```
\x1b[38;2;255;255;255m\x1b[48;2;30;30;30m {pwd_short} \x1b[0m\x1b[38;2;30;30;30m\x1b[48;2;60;60;60m❯\x1b[0m\x1b[38;2;255;255;255m\x1b[48;2;60;60;60m {git_branch} \x1b[0m
```

### Conditional Display

Use scripts to conditionally show information:

```bash
"$([ -n \"$(git rev-parse --git-dir 2>/dev/null)\" ] && echo \"⎇ $(git branch --show-current)\")"
```

Shows git branch only when in a git repository.

## Performance Considerations

1. **Command Execution Time**: Keep all commands under 100ms
2. **Caching**: Consider caching expensive operations
3. **Conditional Logic**: Only fetch data when needed
4. **Async Updates**: Some implementations support async statusline updates

## Escaping

When using special characters in settings.json:

- Backslashes: Use `\\` for literal backslash
- Quotes: Use `\"` for literal quotes
- ANSI codes: `\\x1b` or `\\033`
- Newlines: `\\n`

JSON example:
```json
{
  "statusline": {
    "format": "\\x1b[32m{git_branch}\\x1b[0m {pwd}"
  }
}
```

## Testing

Use the test script to validate statuslines before installing:

```bash
./scripts/test_statusline.py "your statusline" --preview
```

## Resources

- ANSI color table: https://en.wikipedia.org/wiki/ANSI_escape_code
- Unicode symbols: https://unicode-table.com/
- Git prompt customization: https://git-scm.com/book/en/v2/Appendix-A%3A-Git-in-Other-Environments-Git-in-Bash
