# Marketplace Updater Plugin

Automatically checks for marketplace updates on Claude Code startup and provides notifications when updates are available.

## Features

- **Automatic Updates**: Checks for marketplace updates when Claude Code starts
- **Smart Caching**: Avoids excessive network requests with configurable check intervals
- **User-Friendly Notifications**: Provides clear, concise update information in session context
- **Non-Intrusive**: Runs silently in background, only notifies when updates are available
- **Secure**: Validates marketplace URLs and handles authentication properly

## How It Works

This plugin uses Claude Code's [SessionStart hooks](https://docs.claude.com/en/docs/claude-code/hooks) to automatically check for marketplace updates when:

- Claude Code starts a new session
- A session is resumed
- The session is cleared or compacted

The plugin reads from `~/.claude/plugins/known_marketplaces.json` to get the list of installed marketplaces and checks each one for updates using the GitHub API.

## Installation

The plugin should be automatically available when placed in the `plugins/` directory of your Claude Code installation.

## Configuration

### Check Interval

By default, the plugin checks for updates every 24 hours per marketplace. This interval can be adjusted by modifying the `DEFAULT_CHECK_INTERVAL_HOURS` constant in the script.

### Marketplaces Monitored

The plugin monitors all marketplaces listed in `~/.claude/plugins/known_marketplaces.json`. This file is automatically managed by Claude Code when you add or remove marketplaces.

## Cache Management

The plugin caches marketplace data in `~/.claude/cache/marketplace-updater/` to avoid excessive API calls. Cache files are automatically refreshed based on the configured check interval.

## Supported Marketplace Types

- **GitHub Repositories**: Automatically checks for new commits
- **Git-based Sources**: Uses GitHub API for version comparison
- **Local Marketplaces**: Skipped (no remote to check)

## User Experience

When updates are available, you'll see a notification in your Claude Code session context:

```
## 🔄 Marketplace Updates

⚠️ 1 marketplace has updates available:

• **rigerc-claude**: New commit available
  - Commit: `a1b2c3d`
  - Message: Fix marketplace updater configuration...

```

When no updates are available, the plugin runs silently without interrupting your workflow.

## Troubleshooting

### No Updates Shown
- Check that `~/.claude/plugins/known_marketplaces.json` exists and contains marketplaces
- Verify network connectivity
- Check the cache interval setting

### Errors in Hook Execution
- Ensure the script has execute permissions (`chmod +x`)
- Check that Python 3 is available
- Review error messages in Claude Code debug output (`claude --debug`)

### GitHub API Rate Limits
The plugin includes delays between requests to avoid rate limiting. If you encounter rate limit issues, the plugin will log error messages but continue functioning.

## Development

### File Structure

```
plugins/marketplace-updater/
├── .claude-plugin/
│   └── plugin.json              # Plugin metadata
├── hooks/
│   ├── hooks.json              # Hook configuration
│   └── scripts/
│       └── update-marketplaces.py  # Main update script
├── README.md
└── config/
    └── default-marketplaces.json
```

### Hook Configuration

The plugin uses a SessionStart hook defined in `hooks/hooks.json`:

```json
{
  "description": "Automatically checks and updates marketplace metadata at session start",
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume|clear|compact",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/scripts/update-marketplaces.py",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

### Script Details

The main script (`update-marketplaces.py`) implements:

1. **Hook Input Processing**: Reads JSON input from Claude Code
2. **Marketplace Discovery**: Reads known marketplaces from configuration
3. **Update Checking**: Uses GitHub API to compare versions
4. **Caching**: Stores results to avoid excessive API calls
5. **User Notification**: Returns formatted context for SessionStart hook

## Security Considerations

- Validates all marketplace URLs before fetching
- Uses secure HTTPS connections only
- Handles authentication for private repositories
- Sanitizes file paths to prevent directory traversal
- Implements rate limiting to avoid API abuse

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions welcome! Please ensure all code follows the existing patterns and includes appropriate error handling.