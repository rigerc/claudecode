# Integration Examples

This directory contains examples demonstrating how the statusline-creator skill integrates with advanced Claude Code features.

## Slash Command Integration

**File**: `statusline.md`

This slash command provides a quick way to launch statusline creation sessions.

### Installation

```bash
cp examples/statusline.md ~/.claude/commands/statusline.md
```

### Usage

In Claude Code, simply type:

```
/statusline
```

This will:
1. Trigger the statusline-creator skill
2. Prompt for your preferences
3. Create a customized statusline
4. Install it automatically

### Benefits

- **Quick access**: No need to remember skill syntax
- **Guided experience**: Follows a structured workflow
- **Consistency**: Always uses best practices from the skill

## Hooks Integration

**File**: `hooks.json`

Example hook configuration for performance optimization.

### What It Does

This hook caches git information when you change directories, enabling:
- Faster statusline rendering
- Reduced git command overhead
- Smoother terminal experience

### Installation

1. Create or edit `~/.claude/hooks.json`
2. Add the hook from `examples/hooks.json`:

```json
{
  "onDirectoryChange": {
    "command": "~/.claude/skills/statusline-creator/scripts/get_git_info.sh --format statusline > /tmp/claude_statusline_cache",
    "description": "Cache git info on directory change"
  }
}
```

3. Update your statusline to use the cache:

```json
{
  "statusline": {
    "format": "$(cat /tmp/claude_statusline_cache 2>/dev/null || echo '')"
  }
}
```

### Benefits

- **Performance**: Pre-computed git info
- **Responsiveness**: No lag on statusline refresh
- **Efficiency**: Only updates when directory changes

## Subagent Workflow

While not a file example, the SKILL.md demonstrates how to use subagents for complex statusline design.

### When to Use

- Multiple design iterations needed
- Complex requirements with many components
- Testing across different configurations
- Performance optimization required

### How It Works

1. User requests comprehensive statusline
2. Launch general-purpose subagent
3. Subagent uses this skill to:
   - Design multiple options
   - Test each variation
   - Optimize performance
   - Generate documentation
4. Subagent presents final recommendations

### Benefits

- **Parallel exploration**: Try multiple approaches simultaneously
- **Isolated testing**: Test without affecting main session
- **Comprehensive results**: Full analysis and recommendations
- **Documentation**: Complete explanation of choices

## Helper Scripts Integration

All scripts in `scripts/` are designed to be called from statuslines or hooks.

### Direct Usage

In statuslines:
```bash
"$(~/.claude/skills/statusline-creator/scripts/get_git_info.sh --format statusline)"
```

### With Hooks

Pre-cache data:
```json
{
  "onGitCommit": {
    "command": "~/.claude/skills/statusline-creator/scripts/get_git_info.sh --format json > ~/.cache/git_info.json"
  }
}
```

Read cache in statusline:
```bash
"$(cat ~/.cache/git_info.json | jq -r '.branch')"
```

## Template Customization

Templates in `assets/templates/` can be:

1. **Installed as-is**:
   ```bash
   ./scripts/install_statusline.sh minimal
   ```

2. **Used as starting points**:
   ```bash
   # Install template
   ./scripts/install_statusline.sh git-focused

   # Edit ~/.claude/settings.json to customize
   # Test with:
   ./scripts/test_statusline.py --config ~/.claude/settings.json --preview
   ```

3. **Combined**:
   Extract elements from multiple templates to create hybrid designs.

## Complete Workflow Example

Here's how all features work together:

### 1. Initial Setup
```bash
# User invokes slash command
/statusline
```

### 2. Skill Activation
Statusline-creator skill loads and asks preferences.

### 3. Design Phase
```bash
# Skill uses references to design statusline
# Tests with test_statusline.py
# Presents preview to user
```

### 4. Installation
```bash
# Installs with backup
./scripts/install_statusline.sh "custom statusline" --backup

# Sets up hook for caching
# Adds hook to ~/.claude/hooks.json
```

### 5. Optimization
```bash
# If complex design needed, launches subagent
# Subagent iterates and optimizes
# Returns final configuration
```

### 6. Maintenance
```bash
# User can re-run /statusline to update
# Or manually edit settings.json
# Or use skill directly for refinements
```

## Advanced Patterns

### Dynamic Statuslines

Change statusline based on context:

```bash
# In hooks.json
{
  "onVirtualEnvActivate": {
    "command": "sed -i 's/^  \"format\".*/  \"format\": \"🐍 $(basename $VIRTUAL_ENV) │ ...\"/' ~/.claude/settings.json"
  }
}
```

### Conditional Loading

Load different statuslines for different projects:

```bash
# In hooks.json
{
  "onDirectoryChange": {
    "command": "[ -f .statusline ] && cat .statusline > ~/.claude/settings.json.statusline || true"
  }
}
```

### Multi-Line Statuslines

For complex displays:

```bash
{
  "statusline": {
    "format": "Line 1: Project info\\nLine 2: Git info\\nLine 3: System info"
  }
}
```

## Testing Integration

Always test integrations:

```bash
# Test slash command
/statusline

# Test hooks (manually trigger)
~/.claude/skills/statusline-creator/scripts/get_git_info.sh --format statusline

# Test statusline with live data
./scripts/test_statusline.py --config ~/.claude/settings.json --live --skill-dir ./

# Test performance
time ~/.claude/skills/statusline-creator/scripts/get_git_info.sh --format statusline
```

## Troubleshooting

### Slash Command Not Found
- Ensure `statusline.md` is in `~/.claude/commands/`
- Restart Claude Code
- Check YAML frontmatter syntax

### Hooks Not Firing
- Verify `hooks.json` syntax
- Check hook command permissions
- Test hook command manually

### Script Errors
- Ensure scripts are executable: `chmod +x scripts/*.sh`
- Test scripts directly: `./scripts/get_git_info.sh --format statusline`
- Check for missing dependencies

## More Information

- **Skill documentation**: See `SKILL.md` for complete usage guide
- **Format reference**: See `references/statusline_format.md`
- **Best practices**: See `references/best_practices.md`
- **Templates**: See `assets/templates/README.md`
