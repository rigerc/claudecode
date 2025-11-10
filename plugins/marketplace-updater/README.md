# Plugin Repository Updater

Automatically checks if repositories in `~/.claude/plugins/` are up to date and informs you when updates are available.

## Features

- **Automatic Repository Discovery**: Scans for git repositories in `~/.claude/plugins/` and `~/.claude/plugins/marketplaces/`
- **Smart Update Detection**: Compares local commits with remote GitHub repositories
- **Intelligent Caching**: Avoids excessive API requests with configurable check intervals
- **User-Friendly Notifications**: Provides clear update information in session context
- **Non-Intrusive**: Runs silently in background, only notifies when updates are available
- **Error Handling**: Gracefully handles network issues, missing remotes, and API errors

## How It Works

This plugin uses Claude Code's [SessionStart hooks](https://docs.claude.com/en/docs/claude-code/hooks) to automatically check plugin repositories when:

- Claude Code starts a new session
- A session is resumed
- The session is cleared or compacted

The plugin automatically discovers git repositories in your plugins directory and checks each one for updates by comparing the local commit with the latest commit on GitHub.

## Installation

The plugin should be automatically available when placed in the `plugins/` directory of your Claude Code installation.

## Configuration

### Check Interval

By default, the plugin checks for updates every 24 hours per repository. This interval can be adjusted by modifying the `DEFAULT_CHECK_INTERVAL_HOURS` constant in the script.

### Repositories Monitored

The plugin automatically monitors all git repositories found in:
- `~/.claude/plugins/`
- `~/.claude/plugins/marketplaces/`

Only repositories with GitHub remotes are checked for updates.

## Cache Management

The plugin caches repository data in `~/.claude/cache/plugin-updater/` to avoid excessive API calls. Cache files are automatically refreshed based on the configured check interval.

## Supported Repository Types

- **GitHub Repositories**: Automatically checks for new commits via GitHub API
- **Git Repositories**: Scans for `.git` directories to identify repositories
- **Non-Git Repositories**: Skipped (no version control to check)
- **Non-GitHub Remotes**: Skipped with error message

## User Experience

When updates are available, you'll see a notification in your Claude Code session context:

```
## 🔄 Plugin Repository Updates

⚠️ 1 plugin repository has updates available:

• **rigerc-claude**: Updates available
  - Current: `411a3ae`
  - Latest: `8c5052e`
  - Message: 🤖 Auto-update marketplace v1.0.29 (11 plugins)...

• **astrorepo**: ❌ Could not fetch latest commit
```

When no updates are available, the plugin runs silently without interrupting your workflow.

## Troubleshooting

### No Repositories Found
- Ensure you have git repositories in `~/.claude/plugins/` or `~/.claude/plugins/marketplaces/`
- Verify repositories have `.git` directories
- Check that repositories have GitHub remotes configured

### Errors in Hook Execution
- Ensure the script has execute permissions (`chmod +x`)
- Check that Python 3 and git are available
- Review error messages in Claude Code debug output (`claude --debug`)

### GitHub API Issues
The plugin includes delays between requests to avoid rate limiting. If you encounter API issues, the plugin will log error messages but continue functioning with other repositories.

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
└── README.md
```

### Hook Configuration

The plugin uses a SessionStart hook defined in `hooks/hooks.json`:

```json
{
  "description": "Automatically checks plugin repositories for updates at session start",
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
2. **Repository Discovery**: Scans plugins directories for git repositories
3. **Remote URL Parsing**: Extracts GitHub owner/repo from git remote URLs
4. **Update Checking**: Uses GitHub API to compare local vs remote commits
5. **Caching**: Stores results to avoid excessive API calls
6. **User Notification**: Returns formatted context for SessionStart hook

### Key Functions

- `find_plugin_repos()`: Discovers git repositories in plugins directories
- `check_repo_update()`: Compares local commit with GitHub API data
- `parse_github_url()`: Extracts owner/repo from various GitHub URL formats
- `format_update_context()`: Creates user-friendly update notifications

## Security Considerations

- Validates all git repository paths before processing
- Uses secure HTTPS connections for GitHub API calls
- Implements timeouts for all git and network operations
- Handles subprocess execution safely with proper error handling
- Implements rate limiting to avoid API abuse

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions welcome! Please ensure all code follows the existing patterns and includes appropriate error handling.