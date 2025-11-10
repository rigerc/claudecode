# Skills Auto-Discovery Plugin

Automatically discovers and injects all available skills into session context when Claude Code starts.

## Overview

This plugin eliminates the need to manually discover what skills are available in your Claude Code environment. It scans all skill sources (personal, project, and plugins) and automatically injects a comprehensive overview into your session context.

## Features

- **Zero Configuration**: Works immediately after installation
- **Comprehensive Discovery**: Scans personal, project, and plugin skill sources
- **Intelligent Caching**: Only rescans when skills are added/modified
- **Performance Optimized**: Minimal impact on session start time
- **Error Resilient**: Gracefully handles missing or malformed skill files

## How It Works

### Skill Sources Scanned

1. **Personal Skills**: `~/.claude/skills/*/SKILL.md`
2. **Project Skills**: `.claude/skills/*/SKILL.md`
3. **Plugin Skills**: `~/.claude/plugins/**/skills/*/SKILL.md`

### Hook Integration

The plugin uses a `SessionStart` hook that:
1. Triggers on session startup, resume, clear, and compact
2. Runs the discovery script with a 15-second timeout
3. Injects formatted skill overview into session context
4. Caches results for fast subsequent sessions

### Output Format

```
## 🎯 Available Skills (Auto-Discovered)

### 📁 Personal Skills
- **skill-name**: Description of what this skill does
  *Tools: tool1, tool2*

### 📂 Project Skills
- **skill-name**: Description of what this skill does
  *Tools: tool1, tool2*

### 🔌 Plugin Skills
#### Plugin Name
- **skill-name**: Description of what this skill does
  *Tools: tool1, tool2*

---
*Found X skills across personal, project, plugins sources.*
*Skills are model-invoked based on your requests and descriptions.*
```

## Installation

### Option 1: Install to User Plugins

```bash
# Clone or copy this plugin to your user plugins directory
cp -r skills-auto-discovery ~/.claude/plugins/
```

### Option 2: Add to Marketplace

Add this plugin to an existing marketplace or create a new one.

### Option 3: Project-Specific Installation

```bash
# Add to project plugins for team sharing
cp -r skills-auto-discovery .claude/plugins/
```

## Usage

Once installed, the plugin works automatically:

1. **Start a new Claude Code session**
   - Skills are automatically discovered and injected into context
   - See the skills overview at the beginning of your session

2. **Session Resume/Clear**
   - Skills are rediscovered if the cache is invalid
   - Updated skills appear automatically

3. **Manual Cache Refresh**
   ```bash
   # Force refresh of skills cache
   python ~/.claude/plugins/skills-auto-discovery/scripts/discover-skills.py --force-refresh --test
   ```

## Configuration

### Hook Timeout

The default hook timeout is 15 seconds. You can modify this in `hooks/hooks.json`:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume|clear|compact",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/discover-skills.py",
            "timeout": 30  // Increase to 30 seconds if needed
          }
        ]
      }
    ]
  }
}
```

### Cache Location

Cache is stored at: `~/.claude/cache/skills-discovery.json`

To clear the cache:
```bash
rm ~/.claude/cache/skills-discovery.json
```

## Testing

### Test Discovery Script

```bash
# Test the discovery script directly
cd ~/.claude/plugins/skills-auto-discovery
python scripts/discover-skills.py --test

# Force refresh cache
python scripts/discover-skills.py --force-refresh --test
```

### Verify Hook Registration

```bash
# Check if the hook is registered
claude /hooks

# Look for SessionStart hook with discover-skills.py command
```

## Troubleshooting

### Skills Not Appearing

1. **Check Hook Registration**
   ```bash
   claude /hooks
   ```

2. **Test Script Directly**
   ```bash
   python ~/.claude/plugins/skills-auto-discovery/scripts/discover-skills.py --test
   ```

3. **Check File Permissions**
   ```bash
   chmod +x ~/.claude/plugins/skills-auto-discovery/scripts/discover-skills.py
   ```

4. **Clear Cache**
   ```bash
   rm ~/.claude/cache/skills-discovery.json
   ```

### Performance Issues

1. **Increase Timeout**: Modify `hooks/hooks.json` to increase timeout
2. **Check Plugin Count**: Large numbers of plugins may increase discovery time
3. **Verify Cache**: Cache should prevent rescanning on subsequent sessions

### YAML Parsing Errors

The plugin gracefully handles missing `yaml` package:
- Without `yaml`: Only basic skill info (name, directory) is extracted
- With `yaml`: Full metadata including descriptions and tool permissions

Install PyYAML for full functionality:
```bash
pip install PyYAML
```

## Development

### Plugin Structure

```
skills-auto-discovery/
├── .claude-plugin/
│   └── plugin.json          # Plugin metadata
├── hooks/
│   └── hooks.json           # SessionStart hook configuration
├── scripts/
│   └── discover-skills.py   # Main discovery script
└── README.md               # This documentation
```

### Modifying the Discovery Script

The `discover-skills.py` script is modular:
- `SkillsDiscovery.discover_all_skills()`: Main discovery orchestration
- `scan_directory()`: Scan personal/project skill directories
- `scan_plugin_skills()`: Scan plugin marketplace directories
- `extract_skill_metadata()`: Parse SKILL.md files
- `format_skills_overview()`: Generate markdown output

### Adding New Skill Sources

To add new skill sources, modify the `discover_all_skills()` method:

```python
def discover_all_skills(self) -> Dict[str, Any]:
    skills = {
        "personal": self.scan_directory(Path.home() / ".claude" / "skills"),
        "project": self.scan_directory(Path(".claude") / "skills"),
        "plugins": self.scan_plugin_skills(),
        "custom": self.scan_directory(Path("/custom/skills/path")),  # New source
    }
    # ... rest of method
```

## License

MIT License - feel free to modify and distribute.

## Contributing

Contributions welcome! Please ensure:
1. Code follows Python best practices
2. Error handling is robust
3. Performance impact is minimal
4. Documentation is updated

---

**Note**: This plugin is designed for end-users and works with Claude Code's standard skill discovery mechanisms. It enhances visibility of available skills without modifying core Claude Code functionality.