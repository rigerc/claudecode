#!/usr/bin/env python3
"""
Marketplace Updater Hook Script for Claude Code

This script runs on Claude Code startup to check for marketplace updates.
It reads from ~/.claude/plugins/known_marketplaces.json and provides
update information to the user via SessionStart hook context.
"""

import json
import sys
import os
import subprocess
import time
from datetime import datetime, timedelta
from pathlib import Path
import urllib.request
import urllib.error
import urllib.parse

# Configuration
KNOWN_MARKETPLACES_FILE = Path.home() / ".claude" / "plugins" / "known_marketplaces.json"
CACHE_DIR = Path.home() / ".claude" / "cache" / "marketplace-updater"
DEFAULT_CHECK_INTERVAL_HOURS = 24

def log_error(message):
    """Log error to stderr"""
    print(f"[Marketplace Updater] Error: {message}", file=sys.stderr)

def log_info(message):
    """Log info to stderr for debugging"""
    print(f"[Marketplace Updater] {message}", file=sys.stderr)

def read_hook_input():
    """Read JSON input from stdin (Claude Code hook standard)"""
    try:
        input_data = json.load(sys.stdin)
        return input_data
    except json.JSONDecodeError as e:
        log_error(f"Invalid JSON input: {e}")
        return None

def read_known_marketplaces():
    """Read known marketplaces from Claude Code configuration"""
    if not KNOWN_MARKETPLACES_FILE.exists():
        log_error(f"Known marketplaces file not found: {KNOWN_MARKETPLACES_FILE}")
        return {}

    try:
        with open(KNOWN_MARKETPLACES_FILE, 'r') as f:
            data = json.load(f)
            return data.get('marketplaces', {})
    except (json.JSONDecodeError, IOError) as e:
        log_error(f"Failed to read known marketplaces: {e}")
        return {}

def get_cache_file(marketplace_name):
    """Get cache file path for a marketplace"""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    return CACHE_DIR / f"{marketplace_name}.json"

def should_check_marketplace(marketplace_name, check_interval_hours=DEFAULT_CHECK_INTERVAL_HOURS):
    """Check if we should check this marketplace based on cache timestamp"""
    cache_file = get_cache_file(marketplace_name)

    if not cache_file.exists():
        return True

    try:
        with open(cache_file, 'r') as f:
            cache_data = json.load(f)

        last_check = datetime.fromisoformat(cache_data.get('last_check', '1970-01-01'))
        return datetime.now() - last_check > timedelta(hours=check_interval_hours)
    except (json.JSONDecodeError, ValueError, IOError):
        return True  # If cache is corrupted, check again

def cache_marketplace_data(marketplace_name, data):
    """Cache marketplace data with timestamp"""
    cache_file = get_cache_file(marketplace_name)

    cache_data = {
        'last_check': datetime.now().isoformat(),
        'data': data
    }

    try:
        with open(cache_file, 'w') as f:
            json.dump(cache_data, f, indent=2)
    except IOError as e:
        log_error(f"Failed to cache data for {marketplace_name}: {e}")

def get_cached_marketplace_data(marketplace_name):
    """Get cached marketplace data"""
    cache_file = get_cache_file(marketplace_name)

    if not cache_file.exists():
        return None

    try:
        with open(cache_file, 'r') as f:
            cache_data = json.load(f)
            return cache_data.get('data')
    except (json.JSONDecodeError, IOError):
        return None

def get_github_repo_info(owner, repo):
    """Get repository information from GitHub API"""
    try:
        # GitHub API for repo information
        url = f"https://api.github.com/repos/{owner}/{repo}"

        # Create request with user agent
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Claude-Code-Marketplace-Updater/1.0')

        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                return json.loads(response.read().decode())
            else:
                log_error(f"GitHub API returned status {response.status}")
                return None

    except urllib.error.URLError as e:
        log_error(f"Failed to fetch GitHub repo info: {e}")
        return None
    except Exception as e:
        log_error(f"Unexpected error fetching GitHub repo info: {e}")
        return None

def get_github_latest_commit(owner, repo, branch="main"):
    """Get latest commit information from GitHub API"""
    try:
        # GitHub API for latest commit
        url = f"https://api.github.com/repos/{owner}/{repo}/commits/{branch}"

        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Claude-Code-Marketplace-Updater/1.0')

        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                return {
                    'sha': data['sha'],
                    'date': data['commit']['committer']['date'],
                    'message': data['commit']['message']
                }
            else:
                log_error(f"GitHub API returned status {response.status} for commits")
                return None

    except Exception as e:
        log_error(f"Failed to fetch latest commit: {e}")
        return None

def check_marketplace_update(marketplace_name, marketplace_info):
    """Check if a marketplace has updates"""
    source_info = marketplace_info.get('source', {})

    # Handle git-based sources (GitHub repositories)
    if 'repo' in source_info:
        repo_url = source_info['repo']
        # Parse GitHub URL: github.com/owner/repo
        if 'github.com' in repo_url:
            parts = repo_url.strip('/').split('/')
            if len(parts) >= 2:
                owner = parts[-2]
                repo = parts[-1].replace('.git', '')

                # Get latest commit info
                latest_commit = get_github_latest_commit(owner, repo)
                if latest_commit:
                    # Compare with last updated timestamp
                    last_updated = marketplace_info.get('lastUpdated', 0)
                    commit_date = datetime.fromisoformat(latest_commit['date'].replace('Z', '+00:00'))
                    commit_timestamp = int(commit_date.timestamp())

                    has_update = commit_timestamp > last_updated
                    return {
                        'has_update': has_update,
                        'latest_commit': latest_commit,
                        'last_updated': last_updated,
                        'commit_timestamp': commit_timestamp
                    }

    return {'has_update': False}

def format_update_context(updates):
    """Format updates as context for SessionStart hook"""
    if not updates:
        return None

    context_lines = ["## 🔄 Marketplace Updates"]
    context_lines.append("")

    update_count = sum(1 for u in updates if u.get('has_update'))

    if update_count == 0:
        context_lines.append("✅ All marketplaces are up to date")
    else:
        context_lines.append(f"⚠️ {update_count} marketplace{'s' if update_count > 1 else ''} have updates available:")
        context_lines.append("")

        for update in updates:
            marketplace_name = update['name']
            if update.get('has_update'):
                latest_commit = update['latest_commit']
                context_lines.append(f"• **{marketplace_name}**: New commit available")
                context_lines.append(f"  - Commit: `{latest_commit['sha'][:7]}`")
                context_lines.append(f"  - Message: {latest_commit['message'][:50]}...")
                context_lines.append("")
            else:
                context_lines.append(f"• **{marketplace_name}**: ✅ Up to date")

    return "\n".join(context_lines)

def main():
    """Main hook execution"""
    # Read hook input
    hook_input = read_hook_input()
    if not hook_input:
        sys.exit(1)

    hook_event = hook_input.get('hook_event_name')
    source = hook_input.get('source', '')

    log_info(f"Hook triggered: {hook_event} (source: {source})")

    # Only run on startup/resume events
    if hook_event != 'SessionStart':
        log_info(f"Skipping hook event: {hook_event}")
        sys.exit(0)

    # Read known marketplaces
    marketplaces = read_known_marketplaces()
    if not marketplaces:
        log_info("No marketplaces configured")
        sys.exit(0)

    log_info(f"Found {len(marketplaces)} marketplaces to check")

    updates = []

    # Check each marketplace for updates
    for marketplace_name, marketplace_info in marketplaces.items():
        log_info(f"Checking marketplace: {marketplace_name}")

        # Check if we should update based on cache
        if not should_check_marketplace(marketplace_name):
            # Use cached data
            cached_data = get_cached_marketplace_data(marketplace_name)
            if cached_data:
                updates.append({
                    'name': marketplace_name,
                    **cached_data
                })
                continue

        # Check for updates
        update_info = check_marketplace_update(marketplace_name, marketplace_info)

        # Cache the result
        cache_marketplace_data(marketplace_name, update_info)

        updates.append({
            'name': marketplace_name,
            **update_info
        })

        # Small delay to avoid rate limiting
        time.sleep(0.5)

    # Format and return context
    context = format_update_context(updates)

    if context:
        # Return JSON output for SessionStart hook
        output = {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": context
            }
        }
        print(json.dumps(output))
        log_info("Update context provided to user")
    else:
        log_info("No updates to report")

if __name__ == "__main__":
    main()