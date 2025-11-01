# Statusline Design Best Practices

Guidelines and recommendations for creating effective, performant, and beautiful statuslines.

## Design Principles

### 1. Clarity Over Complexity

**Good**: Clear, scannable information
```
~/project │ main ✓ │ 14:23
```

**Avoid**: Too much information, hard to parse
```
user@host[load:1.23|mem:45%|cores:8]~/very/long/path/to/project/src/components[git:main|+3~2?1|ahead:5|behind:2]14:23:45.123
```

**Guideline**: Aim for 3-5 distinct pieces of information maximum.

### 2. Visual Hierarchy

Use color and styling to create visual priority:

1. **Primary** (brightest/bold): Most important info (current location, git branch)
2. **Secondary** (normal): Supporting info (status indicators)
3. **Tertiary** (dimmed): Contextual info (time, host)

Example:
```
\x1b[1;34m~/project\x1b[0m │ \x1b[32mmain\x1b[0m ✓ │ \x1b[90m14:23\x1b[0m
```

### 3. Consistency

Maintain consistent patterns:
- Always use the same separator (│, |, ❯, etc.)
- Use consistent color meanings (green = success, red = error)
- Keep symbol usage predictable

### 4. Responsive Design

Consider statusline length in different contexts:
- **Short terminals** (< 80 chars): Show only essentials
- **Medium terminals** (80-120 chars): Add secondary info
- **Wide terminals** (> 120 chars): Include tertiary info

Implement with conditional scripts:
```bash
COLS=$(tput cols)
if [ $COLS -lt 80 ]; then
    echo "{pwd_short} {git_branch}"
else
    echo "{user}@{host} │ {pwd} │ {git_branch} {git_status} │ {time}"
fi
```

## Information Prioritization

### Essential (Always Show)
- Current working directory or project name
- Git branch (when in a git repository)

### Important (Show When Relevant)
- Git status indicators (when repository is dirty)
- Critical system alerts (low disk space, high load)

### Nice-to-Have (Space Permitting)
- Current time
- Username/hostname (useful when SSH-ing)
- System metrics (load, memory)

## Color Best Practices

### Semantic Colors

Use colors with consistent meaning:
- 🟢 **Green**: Success, clean state, normal operation
- 🔴 **Red**: Errors, critical issues, warnings
- 🔵 **Blue**: Information, directories, navigation
- 🟡 **Yellow**: Warnings, modified state, attention needed
- ⚪ **Gray/Dim**: Less important, background info

### Accessibility

1. **Sufficient contrast**: Ensure text is readable on various terminal backgrounds
2. **Don't rely solely on color**: Use symbols + color for important states
3. **Test on different terminals**: Colors render differently across terminals

Good example (color + symbol):
```
\x1b[32m✓\x1b[0m clean    # Green check
\x1b[31m✗\x1b[0m error    # Red X
```

Bad example (color only):
```
\x1b[32mstatus\x1b[0m    # What does green mean?
```

## Performance Guidelines

### Command Execution Speed

- **Target**: < 50ms per command
- **Maximum**: < 100ms total for entire statusline
- **Optimization strategies**:
  - Cache expensive operations
  - Use built-in shell commands over external programs
  - Parallelize independent operations

### Profiling Commands

Time your commands:
```bash
time ~/.claude/scripts/get_git_info.sh --format statusline
```

### Optimization Techniques

1. **Avoid redundant git calls**:
   ```bash
   # Bad: Multiple git calls
   $(git branch --show-current) $(git status --short | wc -l)

   # Good: Single script with all git info
   $(~/.claude/scripts/get_git_info.sh --format statusline)
   ```

2. **Cache static information**:
   ```bash
   # Cache hostname (doesn't change)
   HOSTNAME=$(hostname)
   ```

3. **Use git plumbing over porcelain**:
   ```bash
   # Faster: Plumbing command
   git symbolic-ref --short HEAD

   # Slower: Porcelain command
   git branch --show-current
   ```

## Symbol Selection

### Git Status Symbols

Common conventions:
- `✓` or `✔` - Clean working directory
- `±` or `~` - Modified files
- `+` - Added files
- `−` or `-` - Deleted files
- `?` - Untracked files
- `↑` - Commits ahead
- `↓` - Commits behind
- `⎇` - Branch indicator

### Separator Symbols

Choose separators based on visual weight:

**Light separators** (minimal design):
- `|` - Simple pipe
- `·` - Middle dot

**Medium separators** (balanced):
- `│` - Box drawing vertical
- `❯` - Triangle

**Heavy separators** (strong divisions):
- `║` - Double vertical
- `⟫` - Math angle

## Layout Patterns

### Left-Heavy (Most Common)
```
~/project │ main ✓ │ 14:23
└─────┬──────┘    └──┬──┘
    primary      secondary
```

Information flows left to right, primary → secondary → tertiary.

### Bookend Style
```
user@host │ ~/project │ main ✓ │ 14:23 │ load:1.2
└───┬────┘                               └───┬───┘
 context                                  system
```

Context on left, system info on right.

### Segmented
```
 ~/project  main ✓  14:23
└────┬────┘└───┬──┘└──┬──┘
   segment  segment segment
```

Clear visual segments with backgrounds.

## Context-Aware Display

### Git Repository Detection

Only show git information when in a repository:
```bash
$(git rev-parse --git-dir >/dev/null 2>&1 && ~/.claude/scripts/get_git_info.sh --format statusline)
```

### SSH Session Highlighting

Show hostname prominently when SSH'd:
```bash
$([ -n "$SSH_CLIENT" ] && echo "\x1b[1;33m@$(hostname)\x1b[0m │ ")
```

### Environment-Specific Info

Show environment indicators for different contexts:
```bash
$([ -n "$VIRTUAL_ENV" ] && echo "🐍 $(basename $VIRTUAL_ENV) │ ")
$([ -n "$NODE_ENV" ] && echo "⬢ $NODE_ENV │ ")
```

## Testing Checklist

Before finalizing a statusline design:

- [ ] Test in narrow terminal (< 80 columns)
- [ ] Test in wide terminal (> 120 columns)
- [ ] Test in git repository (clean state)
- [ ] Test in git repository (dirty state)
- [ ] Test outside git repository
- [ ] Test with long directory paths
- [ ] Verify all commands execute under 100ms
- [ ] Check rendering in different terminal emulators
- [ ] Verify colors work on light and dark backgrounds
- [ ] Ensure no visual glitches (overlapping text, cursor position)

## Common Mistakes to Avoid

1. **Too much information**: Don't try to show everything
2. **Slow commands**: Commands > 100ms cause noticeable lag
3. **Unbalanced ANSI codes**: Always reset colors with `\x1b[0m`
4. **Hard-coded paths**: Use variables and relative paths
5. **No fallbacks**: Handle cases where commands fail
6. **Emoji overuse**: Use sparingly for maximum impact
7. **Inconsistent styling**: Pick a style and stick with it

## Example Progressions

### Minimal → Medium → Full

**Minimal** (< 40 chars):
```
~/project main ✓
```

**Medium** (40-80 chars):
```
\x1b[34m~/project\x1b[0m │ \x1b[32mmain\x1b[0m ✓ │ \x1b[90m14:23\x1b[0m
```

**Full** (80+ chars):
```
\x1b[1mdev@machine\x1b[0m │ \x1b[34m~/workspace/project\x1b[0m │ \x1b[32m⎇ main\x1b[0m ✓ │ \x1b[33mload:1.2\x1b[0m │ \x1b[90m14:23:45\x1b[0m
```

## Maintenance

1. **Periodic review**: Reassess what info you actually use
2. **Performance monitoring**: Check if commands slow down over time
3. **Update scripts**: Keep helper scripts optimized
4. **Clean up**: Remove unused variables and commands
