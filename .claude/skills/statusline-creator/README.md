# Statusline Creator Skill

A comprehensive Claude Code skill for creating beautiful, performant, and customizable statuslines. This skill showcases the full power of Claude skills by integrating helper scripts, slash commands, template assets, comprehensive documentation, hooks, and subagent workflows.

## Features

- 🎨 **Pre-built Templates** - 6 ready-to-use statusline designs
- 🛠️ **Helper Scripts** - Dynamic git and system info extraction
- 📚 **Comprehensive Documentation** - Format reference and best practices
- ⚡ **Performance Optimized** - Fast execution with caching support
- 🔌 **Advanced Integrations** - Slash commands, hooks, and subagent examples
- ✅ **Testing & Validation** - Built-in preview and validation tools

## Quick Start

### Installation

1. Extract the skill to your Claude Code skills directory:
   ```bash
   unzip statusline-creator.zip -d ~/.claude/skills/
   ```

2. Make scripts executable:
   ```bash
   chmod +x ~/.claude/skills/statusline-creator/scripts/*.sh
   ```

### Basic Usage

#### Option 1: Use a Template

Install a pre-built template:

```bash
cd ~/.claude/skills/statusline-creator
./scripts/install_statusline.sh minimal --backup
```

Available templates:
- `minimal` - Basic (directory + git branch)
- `git-focused` - Git-centric with status
- `full-featured` - Complete info display
- `powerline` - Segmented modern design
- `modern-clean` - Elegant balanced design
- `developer` - Dev-focused with metrics

#### Option 2: Custom Design with Claude

Ask Claude to create a custom statusline:

```
Use the statusline-creator skill to design a statusline that shows my git branch,
current time, and uses a blue color scheme
```

Claude will:
1. Read the format reference
2. Design your statusline
3. Test it
4. Install it with backup

#### Option 3: Slash Command (Recommended)

1. Install the slash command:
   ```bash
   cp ~/.claude/skills/statusline-creator/examples/statusline.md ~/.claude/commands/
   ```

2. Use it in Claude Code:
   ```
   /statusline
   ```

   This launches an interactive guided session.

## What's Included

### Scripts (`scripts/`)

**Helper Scripts for Dynamic Data**:

- `get_git_info.sh` - Comprehensive git repository information
  - Formats: json, text, statusline
  - Data: branch, status, ahead/behind counts, file counts

- `get_system_info.sh` - System metrics and environment data
  - Components: time, user, host, load, memory, pwd
  - Flexible output formatting

**Utility Scripts**:

- `test_statusline.py` - Validate and preview statuslines
  - Check ANSI codes, length, performance
  - Preview with sample or live data
  - Identify common issues

- `install_statusline.sh` - Deploy statuslines with backup
  - Template or custom string installation
  - Automatic settings.json merge
  - Timestamped backups

### References (`references/`)

**Comprehensive Documentation**:

- `statusline_format.md` - Complete format specification
  - ANSI color codes (basic, 256-color, RGB)
  - Shell command substitution
  - Unicode symbols guide
  - Variable syntax
  - Example patterns

- `best_practices.md` - Design and optimization guidelines
  - Design principles (clarity, hierarchy, consistency)
  - Performance optimization techniques
  - Color and accessibility best practices
  - Common layout patterns
  - Testing checklist
  - Common mistakes to avoid

### Templates (`assets/templates/`)

**Ready-to-Use Statusline Designs**:

Six professionally designed templates covering different use cases:

| Template | Style | Best For |
|----------|-------|----------|
| minimal | Clean, simple | Distraction-free work |
| git-focused | Git-centric | Version control workflows |
| full-featured | Comprehensive | Maximum information |
| powerline | Segmented backgrounds | Modern aesthetics |
| modern-clean | Elegant, balanced | Daily development |
| developer | Metrics-rich | Performance monitoring |

Each template is a JSON configuration ready to install.

### Examples (`examples/`)

**Integration Examples**:

- `statusline.md` - Slash command for quick access
- `hooks.json` - Hook configuration for caching
- `README.md` - Complete integration guide

Demonstrates:
- Slash command integration
- Hooks for performance optimization
- Subagent workflows
- Advanced patterns

## Advanced Features

### 1. Dynamic Data with Helper Scripts

Instead of inline shell commands, use optimized helper scripts:

```bash
# In your statusline:
"$(~/.claude/skills/statusline-creator/scripts/get_git_info.sh --format statusline)"
```

Benefits:
- Faster execution
- Better error handling
- Consistent formatting
- Maintainable code

### 2. Hooks Integration

Cache data on events for instant statusline updates:

```json
{
  "onDirectoryChange": {
    "command": "~/.claude/skills/statusline-creator/scripts/get_git_info.sh --format statusline > /tmp/git_cache"
  }
}
```

Statusline reads from cache (no git overhead):
```bash
"$(cat /tmp/git_cache 2>/dev/null)"
```

### 3. Slash Command Workflow

The included slash command provides a guided experience:

1. Invocation: `/statusline`
2. Preference gathering (style, info, colors)
3. Recommendation (template vs. custom)
4. Testing and preview
5. Installation with backup
6. Customization guidance

### 4. Subagent Workflows

For complex designs, Claude can launch a subagent to:
- Explore multiple design options
- Test different configurations
- Optimize performance
- Generate comprehensive documentation

Just ask Claude to design a complex statusline, and it may use a subagent automatically.

### 5. Testing & Validation

Always test before deploying:

```bash
# Preview statusline
./scripts/test_statusline.py "your statusline" --preview

# Validate current settings
./scripts/test_statusline.py --config ~/.claude/settings.json

# Test with live data
./scripts/test_statusline.py "your statusline" --live --skill-dir ./
```

## Examples

### Example 1: Quick Minimal Setup

```bash
cd ~/.claude/skills/statusline-creator
./scripts/install_statusline.sh minimal --backup
```

Result: `project main`

### Example 2: Custom Git-Focused

Ask Claude:
```
Use statusline-creator to design a statusline showing:
- Current directory (blue)
- Git branch with status (green if clean, yellow if modified)
- Current time (gray)
```

Claude will create, test, and install:
```
workspace/project │ ⎇ main ✓ │ 14:23
```

### Example 3: Developer Powerline

```bash
./scripts/install_statusline.sh developer --backup
```

Result: `project │ main +3~2 │ 14:23 │ 1.2`

Shows: directory, git branch, changes (+3 staged, ~2 modified), time, system load

## Performance Tips

1. **Use helper scripts** instead of multiple inline git calls
2. **Cache with hooks** for instant updates
3. **Profile commands**: `time command` to check speed
4. **Keep it under 100ms** total execution time
5. **Use git plumbing** commands (faster than porcelain)

See `references/best_practices.md` for detailed optimization techniques.

## Troubleshooting

**Statusline not appearing**
- Restart Claude Code
- Check `~/.claude/settings.json` syntax

**Colors not showing**
- Verify terminal supports ANSI codes
- Check escape sequence format (`\x1b[` vs `\033[`)

**Slow rendering**
- Profile commands: `time script.sh`
- Use caching with hooks
- Simplify statusline

**Script errors**
- Ensure scripts are executable: `chmod +x scripts/*.sh`
- Test scripts directly: `./scripts/get_git_info.sh`

**Git info missing**
- Run from git repository
- Check git installation
- Test: `git branch --show-current`

## Documentation

- **SKILL.md** - Complete skill usage guide for Claude
- **references/statusline_format.md** - Format specification
- **references/best_practices.md** - Design and optimization guide
- **assets/templates/README.md** - Template documentation
- **examples/README.md** - Integration examples

## Architecture

This skill demonstrates professional skill development practices:

1. **Progressive Disclosure**
   - Metadata triggers skill activation
   - SKILL.md loaded when skill runs
   - References loaded as needed
   - Scripts executed without context load

2. **Resource Organization**
   - `scripts/` - Executable automation
   - `references/` - Documentation for Claude
   - `assets/` - Templates for output
   - `examples/` - Integration guides

3. **Integration Showcase**
   - Slash commands for UX
   - Hooks for performance
   - Subagents for complexity
   - Helper scripts for reliability

4. **Testing & Validation**
   - Built-in validation tool
   - Preview functionality
   - Performance profiling
   - Backup protection

## Use Cases

- **Development Workflows** - Show git status, branch, project info
- **System Monitoring** - Display load, memory, time
- **SSH Sessions** - Highlight remote connections
- **Project Context** - Show environment, virtualenv, node version
- **Aesthetic Customization** - Match terminal theme and personal style

## Contributing

To extend this skill:

1. **Add Templates**
   - Create new JSON in `assets/templates/`
   - Document in templates README
   - Test thoroughly

2. **Enhance Scripts**
   - Add features to existing scripts
   - Create new helper scripts
   - Maintain format compatibility

3. **Improve Documentation**
   - Add examples to references
   - Document new features
   - Share best practices

## Credits

Created to demonstrate the full capabilities of Claude Code skills, showcasing:
- Multi-layered resource architecture
- Advanced feature integration
- Professional documentation practices
- Production-ready tooling

## Version

**v1.0.0** - Initial release

Features complete statusline creation system with templates, scripts, documentation, and advanced integrations.

## License

This skill is provided as an example and demonstration of Claude Code skill capabilities.

---

For questions or issues, consult the documentation or ask Claude using the statusline-creator skill!
