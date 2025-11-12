# Plugin Marketplace Guide

Guide to creating and managing Claude Code plugin marketplaces for development and distribution.

## Overview

Marketplaces are JSON catalogs enabling plugin discovery, installation, version management, and distribution.

## Marketplace Types

**Local Development** - Test plugins during development
```bash
/plugin marketplace add ./path/to/.dev-marketplace
/plugin install my-plugin@local-dev
```

**Public Distribution** - Share via git repositories
```bash
/plugin marketplace add owner/marketplace-repo
/plugin install plugin-name@marketplace-name
```

**Team Marketplace** - Organization-wide distribution via `.claude/settings.json`:
```json
{
  "extraKnownMarketplaces": {
    "team-tools": {
      "source": {"source": "github", "repo": "org/claude-plugins"}
    }
  }
}
```

## Creating a Marketplace

### Directory Structure

```
my-marketplace/
└── .claude-plugin/
    └── marketplace.json
```

### Marketplace Schema

**Minimal:**
```json
{
  "name": "marketplace-name",
  "owner": {
    "name": "Your Name",
    "email": "you@example.com"
  },
  "plugins": [
    {
      "name": "plugin-name",
      "source": "plugin-source"
    }
  ]
}
```

**With metadata:**
```json
{
  "name": "marketplace-name",
  "owner": {
    "name": "Your Name",
    "email": "you@example.com"
  },
  "metadata": {
    "description": "Brief marketplace overview",
    "version": "1.0.0",
    "pluginRoot": "./plugins"
  },
  "plugins": [...]
}
```

**Fields:**
- `name` (required) - Marketplace identifier (kebab-case)
- `owner` (required) - Maintainer info (name, email)
- `metadata.description` (optional) - Marketplace overview
- `metadata.version` (optional) - Marketplace version (semantic)
- `metadata.pluginRoot` (optional) - Base path for relative sources
- `plugins` (required) - Array of plugin definitions

## Plugin Entry Schema

**Minimal:**
```json
{
  "name": "plugin-name",
  "source": "./plugins/my-plugin"
}
```

**Complete:**
```json
{
  "name": "plugin-name",
  "source": "./plugins/my-plugin",
  "version": "1.0.0",
  "description": "What this plugin does",
  "author": {
    "name": "Author Name",
    "email": "author@example.com"
  },
  "repository": "https://github.com/author/plugin",
  "license": "MIT",
  "keywords": ["tag1", "tag2"]
}
```

**Advanced (custom paths):**
```json
{
  "name": "plugin-name",
  "source": "./plugins/my-plugin",
  "commands": ["./custom-commands/"],
  "agents": ["./custom-agents/"],
  "hooks": "./config/hooks.json",
  "mcpServers": "./mcp-config.json",
  "strict": false
}
```

**strict field:**
- `true` (default) - Requires plugin.json; marketplace supplements it
- `false` - Marketplace serves as complete manifest if no plugin.json

## Plugin Sources

**Relative path:**
```json
{
  "name": "my-plugin",
  "source": "./plugins/my-plugin"
}
```

**GitHub:**
```json
{
  "name": "my-plugin",
  "source": {
    "source": "github",
    "repo": "username/plugin-repo",
    "ref": "v1.0.0"
  }
}
```

**Git URL:**
```json
{
  "name": "my-plugin",
  "source": {
    "source": "url",
    "url": "https://gitlab.com/company/plugin.git",
    "ref": "main"
  }
}
```

## Local Development Marketplace

**Create structure:**
```bash
mkdir -p my-plugin/.dev-marketplace/.claude-plugin
```

**Create .dev-marketplace/.claude-plugin/marketplace.json:**
```json
{
  "name": "local-dev",
  "owner": {
    "name": "Developer",
    "email": "dev@example.com"
  },
  "plugins": [
    {
      "name": "my-plugin",
      "version": "0.1.0",
      "description": "Plugin under development",
      "source": ".."
    }
  ]
}
```

**Use:**
```bash
/plugin marketplace add ./my-plugin/.dev-marketplace
/plugin install my-plugin@local-dev

# Test changes
/plugin uninstall my-plugin
/plugin install my-plugin@local-dev
```

## Public Distribution Marketplace

**Create:**
```bash
mkdir my-marketplace && cd my-marketplace
git init
mkdir -p .claude-plugin
```

**Create .claude-plugin/marketplace.json:**
```json
{
  "name": "my-marketplace",
  "owner": {
    "name": "Your Name",
    "email": "you@example.com"
  },
  "metadata": {
    "description": "Curated plugins for X",
    "version": "1.0.0"
  },
  "plugins": [
    {
      "name": "plugin-one",
      "version": "1.0.0",
      "description": "Does X",
      "source": {
        "source": "github",
        "repo": "username/plugin-one"
      }
    }
  ]
}
```

**Publish:**
```bash
git add .
git commit -m "Initial marketplace setup"
git remote add origin https://github.com/username/my-marketplace
git push -u origin main
```

**Users install:**
```bash
/plugin marketplace add username/my-marketplace
/plugin install plugin-name@my-marketplace
```

## Management Commands

**Add marketplace:**
```bash
/plugin marketplace add username/repo           # GitHub
/plugin marketplace add https://gitlab.com/...  # Git URL
/plugin marketplace add ./local-marketplace     # Local
```

**List marketplaces:**
```bash
/plugin marketplace list
```

**Update marketplace:**
```bash
/plugin marketplace update marketplace-name
```

**Remove marketplace:**
```bash
/plugin marketplace remove marketplace-name
```

## Best Practices

**Local Development:**
- Create .dev-marketplace automatically during scaffolding
- Use relative paths (`".."` for parent directory)
- Version as 0.x.x for development status
- Test with uninstall/reinstall cycle

**Public Distribution:**
- Use GitHub for easiest user experience
- Use semantic versioning (MAJOR.MINOR.PATCH)
- Include complete metadata (description, author, keywords, license)
- Pin to git refs for stable releases
- Write clear README with installation instructions
- Update marketplace.json when plugin versions change

**Team Marketplaces:**
- Use organization repositories for access control
- Configure in settings.json for automatic distribution
- Document internal plugins thoroughly
- Use monorepo with relative paths for easier management

**General:**
- Validate marketplace.json: `cat .claude-plugin/marketplace.json | jq .`
- Test locally before distribution
- Version the marketplace itself using `metadata.version`
- Keep plugins updated in marketplace.json
- Use keywords effectively for discovery

## Plugin Packaging and Distribution

When ready to share plugins, package them in standard archive formats for easy distribution.

### Supported Formats

**Git Repositories** (Recommended)
- Most common distribution method
- Enables version control and collaboration
- Marketplace references plugin via git URL with optional branch/tag
- Example: `https://github.com/user/plugin.git#v1.0.0`

**Archive Files**
- `.zip` or `.tar.gz` formats
- Useful for offline distribution or when git isn't available
- Must maintain proper plugin directory structure
- Include `.claude-plugin/plugin.json` at archive root

### Pre-Release Checklist

Before packaging or publishing:

1. **Validate structure**: Run `claude plugin validate /path/to/plugin`
2. **Update version**: Increment version in `plugin.json` following semantic versioning (MAJOR.MINOR.PATCH)
3. **Test locally**: Install from local marketplace and verify all components work
4. **Document changes**: Update README.md with new features or breaking changes
5. **Tag release**: For git repos, create version tag matching plugin.json version

### Distribution Channels

- **Public Marketplace**: Git repository referenced in marketplace.json
- **Team Marketplace**: Private git repo or network share
- **Direct Install**: Share archive file, users extract and reference local path

For comprehensive packaging workflows and automation, consult the [official Claude Code documentation](https://code.claude.com/docs/en/plugins-reference).

## Troubleshooting

See [troubleshooting.md](./troubleshooting.md) for marketplace-specific issues:
- Plugin not appearing
- Installation failures
- Path resolution problems
- Git access issues
