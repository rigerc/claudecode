# Troubleshooting Guide

Common issues and solutions for Claude Code plugin development.

## Plugin Not Loading

**Symptoms:** Plugin doesn't appear, commands unavailable, skills not triggering

**Solutions:**
1. Verify manifest exists: `ls .claude-plugin/plugin.json`
2. Validate structure: `claude plugin validate /path/to/plugin`
3. Check plugin name is kebab-case: `my-plugin` (not `My Plugin` or `my_plugin`)
4. Validate JSON: `cat .claude-plugin/plugin.json | jq .`
5. Ensure required `name` field exists in plugin.json
6. Restart Claude Code
7. Enable debug mode: `claude --debug`

## Commands Not Found

**Symptoms:** `/command-name` says not found, doesn't appear in `/help`

**Solutions:**
1. Verify commands at plugin root: `ls commands/`
2. Check `.md` extension: `ls commands/*.md`
3. Verify frontmatter:
```markdown
---
name: command-name
description: Command description
---
```
4. Use kebab-case in `name` field
5. Validate plugin: `claude plugin validate /path/to/plugin`
6. Reinstall: `/plugin uninstall plugin-name && /plugin install plugin-name@marketplace`

## Agents Not Appearing

**Symptoms:** Agent missing from `/agents`, no delegation

**Solutions:**
1. Verify agents at plugin root: `ls agents/`
2. Check `.md` extension: `ls agents/*.md`
3. Verify required frontmatter:
```markdown
---
description: Specific agent specialty
capabilities:
  - Capability 1
  - Capability 2
---
```
4. Make description specific (Claude uses it for delegation)
5. Check YAML syntax and indentation
6. Reinstall plugin

## Skills Not Triggering

**Symptoms:** Skill doesn't activate, content not loading

**Solutions:**
1. Verify SKILL.md location (nested structure):
   - `skills/skill-name/SKILL.md`
   - Reference in plugin.json: `"skills": ["./skills/skill-name/SKILL.md"]`
2. Verify frontmatter:
```markdown
---
name: skill-identifier
description: Specific trigger description
---
```
3. Make description trigger-specific
4. Use lowercase, numbers, hyphens only (max 64 chars)
5. Test explicitly: "Use the skill-name skill to..."
6. Reinstall plugin

## Hooks Not Firing

**Symptoms:** Hook doesn't execute, no output

**Solutions:**
1. Verify location: `ls hooks/hooks.json`
2. Validate JSON: `cat hooks/hooks.json | jq .`
3. Check event names (case-sensitive):
   - PreToolUse, PostToolUse, UserPromptSubmit
   - SessionStart, SessionEnd, Stop, SubagentStop
   - Notification, PreCompact
4. Verify matcher: `"Bash"`, `"Edit"`, `"Write"`, or `"*"`
5. Check action structure:
```json
{
  "type": "command",
  "command": "echo 'Hook executed'"
}
```
6. Test command manually
7. Add logging: `"command": "echo 'Hook fired' >> /tmp/hook-log.txt"`
8. Restart Claude Code

## MCP Server Not Starting

**Symptoms:** Server missing from `/mcp`, tools unavailable

**Solutions:**
1. Verify location: `ls .mcp.json`
2. Validate JSON: `cat .mcp.json | jq .`
3. Check configuration:
```json
{
  "server-name": {
    "command": "${CLAUDE_PLUGIN_ROOT}/server/executable",
    "args": ["arg1"],
    "env": {"VAR": "value"}
  }
}
```
4. Use absolute paths or `${CLAUDE_PLUGIN_ROOT}`
5. Test command manually: `/path/to/server/command arg1`
6. Verify environment variables use `${VAR}` or `${VAR:-default}`
7. Enable debug mode: `claude --debug`
8. Restart Claude Code (required for MCP changes)

## Validation Errors

**Common issues:**

**"plugin.json not found"**
- Create `.claude-plugin/plugin.json` at exact path

**"name field is required"**
```json
{
  "name": "plugin-name"
}
```

**"Invalid JSON syntax"**
- Check missing/trailing commas
- Verify quote matching
- Use `jq` to validate

**"Component directory not at root"**
- Move `commands/`, `agents/`, `skills/`, `hooks/` to plugin root
- Don't nest inside `.claude-plugin/`

**"Invalid path in plugin.json"**
- Use relative paths starting with `./`
- Verify paths exist

**"Frontmatter missing required field"**
- Commands: need `name`, `description`
- Agents: need `description`, `capabilities`
- Skills: need `name`, `description`

## Marketplace Issues

**Plugin not appearing:**
1. Validate marketplace.json: `cat .claude-plugin/marketplace.json | jq .`
2. Check plugins array has `name`, `version`, `description`, `source`
3. Verify path is relative to marketplace.json location
4. Refresh: `/plugin marketplace update marketplace-name`

**Installation fails:**
1. Check git repository access (public or credentials work)
2. Verify repository URL correct
3. Test install command manually: `git clone https://github.com/user/plugin`

## General Debugging

**Enable debug mode:**
```bash
claude --debug
```
Shows plugin loading, manifest parsing, component registration, errors

**Check structure:**
```bash
tree -L 2 my-plugin/
```
Verify:
- `.claude-plugin/plugin.json` exists
- Component directories at root
- Proper file extensions (`.md`, `.json`)

**Validate frequently:**
```bash
claude plugin validate /path/to/plugin
```
Run after every significant change

**Test incrementally:**
- Add one component at a time
- Test after each addition
- Isolate issues quickly

**Getting help:**
1. Validate structure thoroughly
2. Check [official docs](https://code.claude.com/docs)
3. Enable debug mode for detailed errors
4. Simplify - remove components until it works, then add back
5. Compare with working plugin examples
