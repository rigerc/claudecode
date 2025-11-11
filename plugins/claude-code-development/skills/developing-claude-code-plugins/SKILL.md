---
name: developing-claude-code-plugins
description: Use when working on Claude Code plugins (creating, modifying, testing, releasing, or maintaining) - provides streamlined workflows, patterns, and examples for the complete plugin lifecycle
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - TodoWrite
---

# Developing Claude Code Plugins

## Overview

This skill provides efficient workflows for creating Claude Code plugins. Use it to make plugin development fast and correct - it synthesizes official docs into actionable steps and provides working examples.

## When to Use

Use this skill when:
- Creating a new Claude Code plugin from scratch
- Adding components to an existing plugin (skills, commands, hooks, MCP servers)
- Setting up a development marketplace for testing
- Troubleshooting plugin structure issues
- Understanding plugin architecture and patterns
- Releasing a plugin (versioning, tagging, marketplace distribution)
- Publishing updates or maintaining existing plugins

**For comprehensive official documentation**, use the `working-with-claude-code` skill to access full docs.

## Quick Reference

| Need to... | Read This | Official Docs |
|-----------|-----------|---------------|
| Understand directory structure | `references/plugin-structure.md` | `plugins.md` |
| Choose a plugin pattern | `references/common-patterns.md` | `plugins.md` |
| Debug plugin issues | `references/troubleshooting.md` | Various |
| See working examples | `examples/` directory | N/A |

## Plugin Development Workflow

### Phase 1: Plan

Before writing code:

1. **Define your plugin's purpose**
   - What problem does it solve?
   - Who will use it?
   - What components will it need?

2. **Choose your pattern** (read `references/common-patterns.md`)
   - Simple plugin with one skill?
   - MCP integration with guidance?
   - Command collection?
   - Full-featured platform?

3. **Review examples**
   - `examples/simple-greeter-plugin/` - Minimal plugin
   - `examples/full-featured-plugin/` - All components
   - Installed plugins in `~/.claude/plugins/`

### Phase 2: Create Structure

1. **Create directories** (see `references/plugin-structure.md` for details):
   ```bash
   mkdir -p my-plugin/.claude-plugin
   mkdir -p my-plugin/skills
   # Add other component directories as needed
   ```

2. **Write plugin.json** (required):
   ```json
   {
     "name": "my-plugin",
     "version": "1.0.0",
     "description": "What your plugin does",
     "author": {"name": "Your Name"}
   }
   ```
   See `references/plugin-structure.md` for complete format.

3. **Create development marketplace** (for local testing):

   Create `.claude-plugin/marketplace.json`:
   ```json
   {
     "name": "my-dev",
     "plugins": [{
       "name": "my-plugin",
       "source": "./"
     }]
   }
   ```

   See `references/plugin-structure.md` for complete format.

### Phase 3: Add Components

Use TodoWrite to track component creation:

**Example:**
```
- Create skill: main-workflow
- Add command: /hello
- Configure hooks
- Write README
- Test installation
```

For each component type, see:
- **Format/syntax**: `references/plugin-structure.md`
- **When to use**: `references/common-patterns.md`
- **Working code**: `examples/` directory

### Phase 4: Test Locally

1. **Install for testing**:
   ```bash
   /plugin marketplace add /path/to/my-plugin
   /plugin install my-plugin@my-dev
   ```
   Then restart Claude Code.

2. **Test each component**:
   - Skills: Ask for tasks matching skill descriptions
   - Commands: Run `/your-command`
   - MCP servers: Check tools are available
   - Hooks: Trigger relevant events

3. **Iterate**:
   ```bash
   /plugin uninstall my-plugin@my-dev
   # Make changes
   /plugin install my-plugin@my-dev
   # Restart Claude Code
   ```

### Phase 5: Debug and Refine

If something doesn't work, read `references/troubleshooting.md` for:
- Plugin not loading
- Skill not triggering
- Command not appearing
- MCP server not starting
- Hooks not firing

Common issues are usually:
- Wrong directory structure
- Hardcoded paths (use `${CLAUDE_PLUGIN_ROOT}`)
- Forgot to restart Claude Code
- Missing executable permissions on scripts

### Phase 6: Release and Distribute

1. **Write README** with:
   - What the plugin does
   - Installation instructions
   - Usage examples
   - Component descriptions

2. **Version your release** using semantic versioning:
   - Update `version` in `.claude-plugin/plugin.json`
   - Document changes in CHANGELOG.md or RELEASE-NOTES.md
   - Example: `"version": "1.2.1"` (major.minor.patch)

3. **Commit and tag your release**:
   ```bash
   git add .
   git commit -m "Release v1.2.1: [brief description]"
   git tag v1.2.1
   git push origin main
   git push origin v1.2.1
   ```

4. **Choose distribution method**:

   **Option A: Direct GitHub distribution**
   - Users add: `/plugin marketplace add your-org/your-plugin-repo`
   - Your plugin.json serves as the manifest

   **Option B: Marketplace distribution** (recommended for multi-plugin collections)
   - Create separate marketplace repository
   - Add `.claude-plugin/marketplace.json` with plugin references:
     ```json
     {
       "name": "my-marketplace",
       "owner": {"name": "Your Name"},
       "plugins": [{
         "name": "your-plugin",
         "source": {
           "source": "url",
           "url": "https://github.com/your-org/your-plugin.git"
         },
         "version": "1.2.1",
         "description": "Plugin description"
       }]
     }
     ```
   - Users add: `/plugin marketplace add your-org/your-marketplace`
   - Update marketplace manifest for each plugin release

   **Option C: Private/team distribution**
   - Configure in team's `.claude/settings.json`:
     ```json
     {
       "extraKnownMarketplaces": {
         "team-tools": {
           "source": {"source": "github", "repo": "your-org/plugins"}
         }
       }
     }
     ```

5. **Test the release**:
   ```bash
   # Test fresh installation
   /plugin marketplace add your-marketplace-source
   /plugin install your-plugin@marketplace-name
   # Verify functionality, then clean up
   /plugin uninstall your-plugin@marketplace-name
   ```

6. **Announce and maintain**:
   - GitHub releases (optional)
   - Team notifications
   - Monitor for issues and user feedback
   - Plan maintenance updates

## Critical Rules

**Always follow these** (from `references/plugin-structure.md`):

1. **`.claude-plugin/` contains ONLY manifests** (`plugin.json` and optionally `marketplace.json`)
   - ❌ Don't put skills, commands, or other components inside
   - ✅ Put them at plugin root

2. **Use `${CLAUDE_PLUGIN_ROOT}` for all paths in config files**
   - Makes plugin portable across systems
   - Required for hooks, MCP servers, scripts

3. **Use relative paths in `plugin.json`**
   - Start with `./`
   - Relative to plugin root

4. **Make scripts executable**
   - `chmod +x script.sh`
   - Required for hooks and MCP servers

## Resources in This Skill

- **`references/plugin-structure.md`** - Directory layout, file formats, component syntax
- **`references/common-patterns.md`** - When to use each plugin pattern, examples
- **`references/troubleshooting.md`** - Debug guide for common issues
- **`examples/simple-greeter-plugin/`** - Minimal working plugin (one skill)
- **`examples/full-featured-plugin/`** - Complete plugin with all components

## Cross-References

For deep dives into official documentation, use the `working-with-claude-code` skill to access:
- `plugins.md` - Plugin development overview
- `plugins-reference.md` - Complete API reference
- `skills.md` - Skill authoring guide
- `slash-commands.md` - Command format
- `hooks.md`, `hooks-guide.md` - Hook system
- `mcp.md` - MCP server integration
- `plugin-marketplaces.md` - Distribution

## Best Practices

1. **Start simple** - Begin with minimal structure, add complexity when needed
2. **Test frequently** - Install → test → uninstall → modify → repeat
3. **Use examples** - Copy patterns from working plugins
4. **Follow conventions** - Match style of existing plugins
5. **Document everything** - Clear README helps users and future you
6. **Version properly** - Use semantic versioning (major.minor.patch)

## Troubleshooting

### Plugin Installation Issues

**Problem**: Plugin not appearing after installation
- **Cause**: Missing or incorrect `plugin.json` manifest
- **Solution**: Verify JSON syntax and required fields (name, version, description)
- **Check**: `jq . plugin.json` to validate JSON format

**Problem**: Plugin installs but skills/commands don't work
- **Cause**: Incorrect directory structure or file paths
- **Solution**: Ensure components are at plugin root, not in `.claude-plugin/`
- **Check**: Tree structure matches `references/plugin-structure.md`

**Problem**: Installation fails with "plugin not found"
- **Cause**: Marketplace configuration error or source URL incorrect
- **Solution**: Verify marketplace.json format and source URLs
- **Test**: Access the repository URL directly in browser

### Runtime Errors

**Problem**: Skills not triggering for relevant tasks
- **Cause**: Skill description doesn't match user request patterns
- **Solution**: Review skill descriptions and add common keyword variations
- **Test**: Use exact phrases from skill descriptions

**Problem**: Commands appearing with "command is running" but no response
- **Cause**: Script execution errors or missing required permissions
- **Solution**: Check script permissions (`chmod +x`) and test manually
- **Debug**: Run command script directly to see error output

**Problem**: MCP server not starting or tools not available
- **Cause**: Server configuration errors or missing dependencies
- **Solution**: Verify `${CLAUDE_PLUGIN_ROOT}` variable usage and executable paths
- **Test**: Run MCP server manually to check startup errors

### Development Workflow Issues

**Problem**: Changes not reflected after modification
- **Cause**: Claude Code cache or plugin not reloaded
- **Solution**: Always restart Claude Code after plugin changes
- **Verify**: Check plugin version with `/plugin list`

**Problem**: Git hooks not working in plugin development
- **Cause**: Hook scripts not executable or incorrect paths
- **Solution**: Use absolute paths or `${CLAUDE_PLUGIN_ROOT}` variable
- **Test**: Run hook script manually with sample input

### Performance Issues

**Problem**: Plugin loading slowly or causing timeouts
- **Cause**: Large binary dependencies or inefficient startup scripts
- **Solution**: Optimize startup time and lazy-load heavy dependencies
- **Monitor**: Use timing logs to identify bottlenecks

**Problem**: Memory usage increasing over time
- **Cause**: Resource leaks in long-running processes
- **Solution**: Review MCP server code for proper resource cleanup
- **Profile**: Monitor memory usage during extended sessions

### Marketplace and Distribution Issues

**Problem**: Users can't install from marketplace
- **Cause**: Incorrect marketplace.json format or missing plugin metadata
- **Solution**: Validate marketplace.json and verify plugin URLs are accessible
- **Test**: Install from fresh environment (different machine/user)

**Problem**: Version conflicts during updates
- **Cause**: Improper semantic versioning or breaking changes in patches
- **Solution**: Follow semantic versioning strictly and document breaking changes
- **Prevent**: Use major version bumps for breaking changes

### Debugging Tools and Commands

```bash
# Check plugin installation status
/plugin list

# Verify plugin manifest
cat .claude-plugin/plugin.json | jq .

# Test script permissions
find . -name "*.sh" -exec ls -la {} \;

# Check marketplace configuration
cat .claude-plugin/marketplace.json | jq .

# Monitor plugin logs (if available)
tail -f ~/.claude/logs/claude-code.log
```

### Common Error Messages and Solutions

**"Plugin not found in marketplace"**
- Verify marketplace is added: `/plugin marketplace list`
- Check plugin name spelling and version
- Ensure marketplace URL is accessible

**"Permission denied" for script execution**
- Run: `chmod +x path/to/script.sh`
- Check script shebang: `#!/bin/bash` or `#!/usr/bin/env bash`
- Verify script is not in Windows format (use `dos2unix` if needed)

**"JSON parse error" in plugin.json**
- Validate JSON: `jq . plugin.json`
- Check for trailing commas
- Ensure strings are properly quoted

**"Skill timeout" errors**
- Reduce skill complexity or break into smaller steps
- Add progress indicators for long operations
- Check infinite loops or blocking operations

### Getting Help

1. **Check this skill's references**: `references/troubleshooting.md`
2. **Review official docs**: Use `working-with-claude-code` skill
3. **Examine working examples**: `examples/` directory
4. **Test in isolation**: Create minimal reproduction case
5. **Check community resources**: GitHub issues, forums, Discord

## Performance Considerations

### Plugin Loading Performance

**Minimize Startup Time**
- Keep plugin.json lightweight and focused
- Avoid heavy computations in skill initialization
- Use lazy loading for expensive resources
- Consider caching frequently accessed data

**Optimize MCP Server Startup**
- Defer database connections and network requests until needed
- Pre-validate configuration before starting services
- Use connection pooling for external resources
- Implement graceful degradation for missing dependencies

### Memory Management

**Monitor Resource Usage**
- Track memory consumption in long-running MCP servers
- Clean up temporary files and cache directories
- Avoid memory leaks in persistent connections
- Use weak references where appropriate for cached data

**Optimize Skill Performance**
- Break complex skills into smaller, focused subtasks
- Use streaming for large data processing
- Implement progress feedback for long operations
- Consider timeout handling for external API calls

### Scalability Considerations

**Design for Multiple Users**
- Use per-user configuration directories when applicable
- Implement proper isolation between user sessions
- Consider concurrent access patterns for shared resources
- Design stateless operations where possible

**Handle Large Codebases**
- Implement incremental scanning and processing
- Use file change notifications for efficient updates
- Consider database storage for large metadata sets
- Implement pagination for large result sets

### Optimization Guidelines

**Caching Strategies**
- Cache API responses with appropriate TTL
- Store computed results for expensive operations
- Use file system caching for downloaded resources
- Implement cache invalidation for dynamic content

**Async Operations**
- Use non-blocking operations for network requests
- Implement concurrent processing for independent tasks
- Consider worker threads for CPU-intensive operations
- Use promises/async patterns for better responsiveness

**Resource Cleanup**
- Implement proper cleanup in MCP server shutdown
- Remove temporary files after processing
- Close network connections and database handles
- Clean up background tasks and timers

### Performance Monitoring

**Key Metrics to Track**
- Plugin loading time: `/usr/bin/time -v claude-code`
- Memory usage: `ps aux | grep claude-code`
- MCP server response times: Add timing logs
- Skill execution duration: Log start/end times

**Debugging Performance Issues**
```bash
# Profile plugin loading
strace -c -p $(pgrep claude-code)

# Monitor memory usage
watch -n 1 'ps aux | grep claude-code'

# Check file descriptor usage
lsof -p $(pgrep claude-code) | wc -l

# Profile MCP server
time -v python your-mcp-server.py
```

### Best Practices for High Performance

1. **Profile Early**: Measure performance before optimization
2. **Optimize Hot Paths**: Focus on frequently used operations
3. **Use Appropriate Data Structures**: Choose algorithms wisely
4. **Minimize I/O Operations**: Batch file operations when possible
5. **Implement Caching**: Cache expensive computations and results
6. **Monitor and Iterate**: Continuously measure and improve performance

## Workflow Summary

```
Plan → Choose pattern, review examples
Create → Make structure, write manifests
Add → Build components (skills, commands, etc.)
Test → Install via dev marketplace
Debug → Use troubleshooting guide
Release → Version, tag, distribute via marketplace
Maintain → Monitor, update, support users
```

**The correct path is the fast path.** Use references, follow patterns, test frequently.
