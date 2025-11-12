# Development Workflow

Guide to developing, testing, validating, and distributing Claude Code plugins.

## Example Scenarios

Understanding concrete usage scenarios before building helps determine the right plugin structure and components.

### Scenario 1: Single Command Plugin

**User request:** "Create a /format-json command that prettifies JSON"

**Workflow:**
1. **Understanding** - Command takes JSON input, outputs formatted version
2. **Planning** - Commands only, no other components needed
3. **Implementation** - `python scripts/init_plugin.py json-formatter`
4. **Customization** - Delete unused components (agents/, skills/, hooks/, .mcp.json), update plugin.json, customize commands/format-json.md with JSON parsing logic
5. **Testing** - Install via local marketplace, test with sample JSON

**Components:** Commands only

### Scenario 2: Multi-Component Development Plugin

**User request:** "Create a plugin for AWS deployments with commands and agents"

**Workflow:**
1. **Understanding** - Commands: /deploy, /rollback, /status; Agent: Delegates AWS-specific operations; MCP: AWS CLI integration
2. **Planning** - Commands + Agents + MCP servers
3. **Implementation** - `python scripts/init_plugin.py aws-deploy-tools`
4. **Customization** - Delete skills/, update plugin.json, add 3 commands, customize agents/aws-agent.md, configure .mcp.json for AWS CLI
5. **Testing** - Test each command, verify agent delegation, confirm MCP integration

**Components:** Commands, Agents, MCP servers

### Scenario 3: Event-Driven Plugin

**User request:** "Auto-format Python files when I edit them"

**Workflow:**
1. **Understanding** - Hook triggers after Edit tool, runs formatter
2. **Planning** - Hooks only
3. **Implementation** - `python scripts/init_plugin.py python-formatter`
4. **Customization** - Delete unused components (commands/, agents/, skills/, .mcp.json), update plugin.json, configure hooks/hooks.json for PostToolUse(Edit) event
5. **Testing** - Edit a .py file, verify formatting occurs automatically

**Components:** Hooks only

## Development Phases

0. **Understanding** - Gather concrete usage examples
1. **Planning** - Design structure and components
2. **Implementation** - Create plugin files
3. **Local Testing** - Test via local marketplace
4. **Validation** - Verify structure and functionality
5. **Distribution** - Share via git and marketplace

## Phase 0: Understanding

Before planning the structure, gather concrete examples of how the plugin will be used.

**Ask clarifying questions:**
- What is the plugin for? What specific tasks will it support?
- Can you provide 2-3 examples of how users will interact with the plugin?
- What workflows does the plugin need to enable?

**Example questions for different plugin types:**

For command plugins:
- "What commands do you need?" (/deploy, /test, /format, etc.)
- "What should each command do?"
- "What inputs will the commands accept?"

For automation plugins:
- "What events should trigger the plugin?" (file saves, tool usage, etc.)
- "What actions should happen automatically?"
- "Are there conditions for when it should run?"

For integration plugins:
- "What external service are you integrating with?"
- "What operations need to be available?"
- "Are there API credentials or configuration needed?"

**Outcome:** Clear understanding of plugin purpose and usage patterns that inform component selection.

## Phase 1: Planning

**Define purpose:**
- Identify problems the plugin solves
- Choose needed components (commands/agents/skills/hooks/MCP)

**Plan structure:**
```
my-plugin/
├── .claude-plugin/plugin.json
├── commands/
├── agents/
├── skills/
├── hooks/
├── .mcp.json
└── README.md
```

## Phase 2: Implementation

**Initialize plugin structure:**

Execute the initialization script to create complete plugin scaffold:

```bash
python scripts/init_plugin.py my-plugin [--path ~/plugins]
```

This creates:
- Standard directory structure (.claude-plugin/, commands/, agents/, skills/, hooks/)
- plugin.json manifest with all component types registered
- Example components from templates for each type
- Local development marketplace (.dev-marketplace/)
- README template

**Customize the generated plugin:**

1. **Remove unused components** - Delete directories for components you don't need (e.g., delete agents/ if no agents required)

2. **Update plugin.json** - Remove references to deleted components, add metadata:
```json
{
  "name": "my-plugin",
  "version": "0.1.0",
  "description": "Clear description of what the plugin does",
  "author": {
    "name": "Your Name"
  },
  "repository": "https://github.com/username/my-plugin",
  "license": "MIT"
}
```

3. **Customize components** - Replace example content with actual functionality:
   - Follow [component-specifications.md](./component-specifications.md)
   - Use proper YAML frontmatter
   - Follow naming conventions (kebab-case for files)

4. **Add resources** - Create any scripts, templates, or reference docs needed

**Understanding templates:**

The initialization script generates example components from templates located in `assets/`. These templates provide starting points:

- **skill-template.md** - Skill structure with YAML frontmatter, bundled resources sections (scripts/, references/, assets/), and best practices
- **command-template.md** - Slash command with YAML frontmatter, usage examples, and argument handling patterns
- **agent-template.md** - Specialized agent with delegation patterns, tool restrictions, and workflow structure
- **hooks-template.json** - Configuration examples for all 8 hook event types with shell command patterns
- **mcp-template.json** - MCP server configurations for Node.js, Python, and custom binaries with environment variables
- **marketplace-template.json** - Marketplace structure with plugin entries and metadata

Templates are automatically copied during initialization and should be customized with actual functionality. For more comprehensive examples showing real-world implementations, see [complete-examples.md](./complete-examples.md).

**Manual creation alternative:**

Manual creation is only needed for custom initialization requirements. For standard plugins, always use the initialization script.

## Phase 3: Local Testing

The initialization script automatically creates a local development marketplace at `.dev-marketplace/` with proper configuration. Use this for testing.

**Add marketplace and install:**
```bash
/plugin marketplace add /full/path/to/my-plugin/.dev-marketplace
/plugin install my-plugin@local-dev
```

**Test components:**
- Commands: `/help` to verify, then `/command-name` to test
- Agents: `/agents` to list, trigger via natural delegation
- Skills: Invoke through natural language
- Hooks: Trigger events, verify actions execute
- MCP: `/mcp` to list servers, use provided tools

**Iteration cycle:**
1. Make changes
2. `/plugin uninstall my-plugin`
3. `/plugin install my-plugin@local-dev`
4. Test
5. Repeat

**Note:** Restart Claude Code for MCP server changes.

## Phase 4: Validation

**Validate structure:**
```bash
claude plugin validate /path/to/my-plugin
```

Checks:
- plugin.json exists and valid
- Required `name` field present
- JSON syntax correct
- Component directories at plugin root
- Proper component structure

**Debug issues:**
```bash
claude --debug              # Enable debug mode
/help                       # Verify commands appear
/agents                     # Verify agents listed
```

See [troubleshooting.md](./troubleshooting.md) for common issues.

## Phase 5: Distribution

**Prepare release:**

1. Update version in plugin.json:
```json
{
  "version": "1.0.0"
}
```

2. Write README.md with installation, usage, features, configuration

3. Add LICENSE file (MIT, Apache-2.0, etc.)

4. Document dependencies (environment variables, external tools)

**Create git repository:**
```bash
git init
echo ".dev-marketplace/" > .gitignore
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/username/my-plugin
git push -u origin main
```

**Create marketplace:**

See [marketplace-guide.md](./marketplace-guide.md) for details.

Quick steps:
1. Create marketplace repository
2. Add marketplace.json:
```json
{
  "name": "my-marketplace",
  "description": "My plugin marketplace",
  "plugins": [
    {
      "name": "my-plugin",
      "version": "1.0.0",
      "description": "Plugin description",
      "repository": "https://github.com/username/my-plugin",
      "installCommand": "git clone https://github.com/username/my-plugin"
    }
  ]
}
```
3. Push to git
4. Share marketplace URL

**User installation:**
```bash
/plugin marketplace add username/marketplace-repo
/plugin install my-plugin@my-marketplace
```

## Best Practices

**Development:**
- Validate frequently with `claude plugin validate`
- Test incrementally as components are added
- Use version control with clear commit messages
- Document as you build

**Testing:**
- Test realistic scenarios and edge cases
- Get user feedback
- Iterate using uninstall/reinstall cycle

**Distribution:**
- Use semantic versioning (MAJOR.MINOR.PATCH)
- Maintain changelog for version updates
- Write clear README with installation instructions
- Choose appropriate open source license

**Maintenance:**
- Monitor user-reported issues
- Update for Claude Code changes
- Increment version with each release
- Maintain backward compatibility

## Useful Commands

**Marketplace:**
```bash
/plugin marketplace add <source>
/plugin marketplace list
/plugin marketplace update <name>
/plugin marketplace remove <name>
```

**Plugins:**
```bash
/plugin install <name>@<marketplace>
/plugin uninstall <name>
/plugin enable <name>@<marketplace>
/plugin disable <name>@<marketplace>
/plugin list
```

**Development:**
```bash
claude plugin validate <path>
claude --debug
/help
/agents
/mcp
```
