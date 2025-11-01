---
name: statusline-creator
description: Create and customize beautiful, informative statuslines for Claude Code. Use this skill when users request statusline design, customization, or configuration. Triggers on requests like "create a statusline", "customize my statusline", "design a statusline showing git info", or "make a minimal statusline". This skill showcases advanced Claude Code features including helper scripts, slash commands, template assets, and reference documentation.
---

# Statusline Creator

## Overview

This skill enables creating sophisticated, performant, and beautiful statuslines for Claude Code through a complete toolkit of templates, scripts, references, and automation. It demonstrates the power of Claude skills by integrating multiple advanced features: helper scripts for dynamic data, comprehensive reference documentation, template assets, and slash commands for quick setup.

## Core Capabilities

### 1. Quick Template Installation

For users who want ready-made statuslines, use the pre-built templates in `assets/templates/`:

Available templates:
- **minimal** - Clean, distraction-free (just directory + branch)
- **git-focused** - Emphasizes version control information
- **full-featured** - Comprehensive info (user, host, git, time)
- **powerline** - Modern segmented design with backgrounds
- **modern-clean** - Balanced elegance with subtle styling
- **developer** - Dev-focused with metrics and change counts

To install a template:
```bash
./scripts/install_statusline.sh <template-name> --backup
```

The `--backup` flag creates a timestamped backup of existing settings.

**Example workflow**:
```
User: "Create a minimal statusline for me"

1. Review available templates in assets/templates/
2. Recommend the 'minimal' template
3. Execute: ./scripts/install_statusline.sh minimal --backup
4. Inform user that statusline is installed
```

### 2. Custom Statusline Design

For users with specific requirements, design custom statuslines using the comprehensive format reference.

**Design process**:

1. **Gather requirements** - Ask about:
   - Information priorities (git, time, system metrics, etc.)
   - Visual preferences (minimal vs. rich, color usage)
   - Terminal width (determines information density)
   - Use case (development, SSH sessions, specific workflows)

2. **Consult references** - Load relevant documentation:
   - `references/statusline_format.md` - Format syntax, ANSI codes, variables
   - `references/best_practices.md` - Design principles, performance guidelines

3. **Compose statusline** - Build using:
   - ANSI color codes for styling (e.g., `\x1b[32m` for green)
   - Shell command substitution for dynamic data (e.g., `$(git branch --show-current)`)
   - Unicode symbols for visual elements (e.g., `│`, `⎇`, `✓`)
   - Helper scripts for complex data (see capability #3)

4. **Test and validate** - Use test script:
   ```bash
   ./scripts/test_statusline.py "your statusline string" --preview
   ```

5. **Install** - Deploy the custom statusline:
   ```bash
   ./scripts/install_statusline.sh "your custom statusline string" --backup
   ```

**Example workflow**:
```
User: "Design a statusline that shows my git branch, current time, and uses a blue color scheme"

1. Read references/statusline_format.md to understand ANSI codes and variables
2. Compose: "\x1b[34m$(basename \"$PWD\")\x1b[0m │ \x1b[36m$(git branch --show-current)\x1b[0m │ \x1b[90m$(date +%H:%M)\x1b[0m"
3. Test: ./scripts/test_statusline.py "..." --preview
4. Install: ./scripts/install_statusline.sh "..." --backup
5. Explain the components and color choices to the user
```

### 3. Dynamic Data Integration with Helper Scripts

For statuslines requiring complex or frequently-needed data, leverage the bundled helper scripts instead of writing inline shell commands. This improves performance and maintainability.

**Available scripts**:

#### `scripts/get_git_info.sh`
Comprehensive git repository information.

Formats:
- `--format json` - Structured data with all fields
- `--format text` - Human-readable output
- `--format statusline` - Compact format optimized for statuslines

Output includes: branch name, modified/added/deleted counts, ahead/behind counts, clean status.

Usage in statusline:
```bash
"$(~/.claude/skills/statusline-creator/scripts/get_git_info.sh --format statusline)"
```

#### `scripts/get_system_info.sh`
System metrics and information.

Options:
- `--format [json|text|statusline]` - Output format
- `--components component1,component2,...` - Select specific info

Available components: time, user, host, load, memory, pwd

Usage in statusline:
```bash
"$(~/.claude/skills/statusline-creator/scripts/get_system_info.sh --format statusline --components time,load)"
```

#### `scripts/test_statusline.py`
Validate and preview statuslines before deployment.

Options:
- `--preview` - Show visual preview with sample data
- `--live` - Preview with actual script data
- `--skill-dir <path>` - Path to skill directory for live testing

Usage:
```bash
./scripts/test_statusline.py "statusline string" --preview
./scripts/test_statusline.py --config ~/.claude/settings.json --live --skill-dir ./
```

**Example workflow**:
```
User: "Create a statusline with detailed git information and system load"

1. Use get_git_info.sh for comprehensive git data
2. Use get_system_info.sh for system metrics
3. Compose statusline using script calls:
   "$(~/.claude/skills/statusline-creator/scripts/get_git_info.sh --format statusline) │ load: $(~/.claude/skills/statusline-creator/scripts/get_system_info.sh --format statusline --components load)"
4. Test with live data:
   ./scripts/test_statusline.py "..." --live --skill-dir ./
5. Install with backup
```

### 4. Iterative Refinement

Support users in refining their statuslines through testing and feedback.

**Refinement workflow**:

1. **Preview** - Show what the statusline will look like:
   ```bash
   ./scripts/test_statusline.py "statusline" --preview
   ```

2. **Validate** - Check for common issues:
   - Unbalanced ANSI codes
   - Performance problems (slow commands)
   - Excessive length
   - Missing symbols or formatting errors

3. **Iterate** - Adjust based on:
   - User feedback on appearance
   - Validation warnings/errors
   - Performance measurements
   - Best practices from `references/best_practices.md`

4. **Test in context** - Have user test in their actual workflow

5. **Fine-tune** - Make adjustments for edge cases

**Example workflow**:
```
User: "The statusline is too long and the colors don't look right"

1. Run test script to validate current statusline
2. Review output for validation warnings
3. Consult references/best_practices.md for length guidelines
4. Suggest specific adjustments:
   - Shorten directory display to basename only
   - Adjust color codes for better contrast
   - Remove less critical information
5. Generate updated version
6. Test and preview
7. Deploy updated version
```

### 5. Advanced Customization

For power users, implement sophisticated statusline features.

**Advanced techniques**:

#### Conditional Display
Show information only when relevant:
```bash
$(git rev-parse --git-dir >/dev/null 2>&1 && echo "git: $(git branch --show-current)")
```

#### Context-Aware Styling
Change appearance based on context:
```bash
$([ -n "$SSH_CLIENT" ] && echo "\x1b[1;33m@$(hostname)\x1b[0m" || echo "")
```

#### Environment Integration
Display environment-specific info:
```bash
$([ -n "$VIRTUAL_ENV" ] && echo "🐍 $(basename $VIRTUAL_ENV) │ ")
```

#### Performance Optimization
Cache expensive operations, use fast git plumbing commands, parallelize independent data fetching.

Consult `references/best_practices.md` for detailed optimization strategies.

**Example workflow**:
```
User: "Make my statusline show my Python virtual environment when active and highlight when I'm SSH'd into a remote machine"

1. Read references/best_practices.md for context-aware patterns
2. Compose conditional logic:
   - Check $SSH_CLIENT for SSH session
   - Check $VIRTUAL_ENV for Python environment
3. Design highlighted SSH indicator
4. Create statusline with both features
5. Test in different contexts (local, SSH, with/without venv)
6. Install and explain the conditional behavior
```

## Slash Command Integration

This skill pairs with a slash command for quick statusline setup. Users can invoke:

```
/statusline
```

This launches an interactive statusline creation session.

To create the slash command, place this in `~/.claude/commands/statusline.md`:

```markdown
---
description: Create or customize a Claude Code statusline
---

Help me create a beautiful, functional statusline for Claude Code.

Use the statusline-creator skill to:
1. Ask about my preferences (minimal vs. full-featured, what info to show, color preferences)
2. Recommend an approach (template vs. custom)
3. Create and install the statusline
4. Explain how to further customize it

Focus on creating something that matches my workflow and aesthetic preferences.
```

## Hooks Integration Example

Statuslines can integrate with Claude Code hooks for dynamic updates. Example hook in `~/.claude/hooks.json`:

```json
{
  "onDirectoryChange": {
    "command": "~/.claude/skills/statusline-creator/scripts/get_git_info.sh --format statusline > /tmp/statusline_cache",
    "description": "Update statusline git info on directory change"
  }
}
```

This caches git info when changing directories, which can be read by the statusline for faster rendering.

## Subagent Workflow Example

For complex statusline design involving multiple iterations and testing, consider using a subagent:

```
When user requests comprehensive statusline design with multiple requirements:
1. Launch a general-purpose subagent to handle the full design process
2. Provide the subagent with:
   - This skill context
   - User requirements
   - Access to references and scripts
3. Subagent performs:
   - Design iterations
   - Testing with different configurations
   - Performance validation
   - Final installation
4. Subagent reports back with final statusline and documentation
```

This demonstrates how skills can leverage subagents for complex, multi-step workflows.

## Best Practices

When using this skill, follow these guidelines:

1. **Start simple** - Begin with templates or minimal designs, then add complexity
2. **Test early** - Use test_statusline.py before installation
3. **Always backup** - Use `--backup` flag when installing
4. **Prioritize performance** - Commands should execute under 100ms total
5. **Consider context** - Design for the user's terminal size and workflow
6. **Use references** - Consult bundled documentation for format details and design principles
7. **Leverage scripts** - Use helper scripts for complex data instead of inline commands
8. **Validate thoroughly** - Check for ANSI code balance, length, and rendering

## Troubleshooting

Common issues and solutions:

**Statusline not appearing**: Restart Claude Code or check settings.json syntax

**Colors not showing**: Verify terminal supports ANSI codes, check escape sequences

**Slow rendering**: Profile commands with `time`, optimize or cache expensive operations

**Garbled text**: Check for unbalanced ANSI codes with test_statusline.py

**Git info missing**: Ensure scripts are executable: `chmod +x scripts/*.sh`

## Resources Summary

This skill includes comprehensive resources demonstrating best practices for skill development:

### scripts/
- `get_git_info.sh` - Comprehensive git repository information extraction
- `get_system_info.sh` - System metrics and environment data
- `test_statusline.py` - Validation and preview tool
- `install_statusline.sh` - Deployment automation with backup support

**Usage**: Execute scripts directly or reference in statusline strings for dynamic data.

### references/
- `statusline_format.md` - Complete format specification, ANSI codes, variables, examples
- `best_practices.md` - Design principles, performance guidelines, patterns, common mistakes

**Usage**: Read these documents when designing custom statuslines or troubleshooting issues.

### assets/templates/
- `minimal.json` - Basic statusline template
- `git-focused.json` - Git-centric design
- `full-featured.json` - Comprehensive information display
- `powerline.json` - Modern segmented styling
- `modern-clean.json` - Elegant balanced design
- `developer.json` - Development workflow focused
- `README.md` - Template documentation

**Usage**: Install templates directly or use as starting points for customization.

## Example Interactions

### Scenario 1: Quick Setup
```
User: "Create a minimal statusline"
→ Install minimal template using install_statusline.sh
→ Explain installed statusline components
→ Offer customization options
```

### Scenario 2: Custom Design
```
User: "Design a statusline showing git branch, project name, and time with a blue theme"
→ Read references/statusline_format.md for ANSI codes
→ Compose custom statusline with blue color scheme
→ Test with test_statusline.py --preview
→ Install with backup
→ Explain customization possibilities
```

### Scenario 3: Advanced Features
```
User: "Create a statusline that shows detailed git stats and only displays when in a repo"
→ Use get_git_info.sh script for comprehensive data
→ Add conditional logic to check for git repository
→ Compose statusline with script integration
→ Test in both git and non-git directories
→ Optimize for performance using references/best_practices.md
→ Install and document behavior
```

### Scenario 4: Refinement
```
User: "My statusline is too long and slow"
→ Run test_statusline.py on current configuration
→ Review validation warnings
→ Consult references/best_practices.md for optimization
→ Profile individual commands for performance
→ Suggest specific optimizations (caching, shorter paths, faster commands)
→ Implement improvements
→ Verify performance gains
→ Reinstall
```

This skill demonstrates how to build comprehensive, production-ready skills that showcase the full power of Claude Code's advanced features.
