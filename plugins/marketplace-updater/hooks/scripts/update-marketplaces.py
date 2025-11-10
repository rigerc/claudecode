#!/usr/bin/env python3
"""
Plugin Repository Updater Hook Script for Claude Code

This script runs on Claude Code startup to check if repositories in
~/.claude/plugins/ are up to date, and informs the user if not.
It scans for git repositories and checks for updates via GitHub API.
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
PLUGINS_DIR = Path.home() / ".claude" / "plugins"
CACHE_DIR = Path.home() / ".claude" / "cache" / "plugin-updater"
DEFAULT_CHECK_INTERVAL_HOURS = 24


def log_error(message):
    """Log error to stderr"""
    print(f"[Plugin Updater] Error: {message}", file=sys.stderr)


def log_info(message):
    """Log info to stderr for debugging"""
    print(f"[Plugin Updater] {message}", file=sys.stderr)


def read_hook_input():
    """Read JSON input from stdin (Claude Code hook standard)"""
    try:
        input_data = json.load(sys.stdin)
        return input_data
    except json.JSONDecodeError as e:
        log_error(f"Invalid JSON input: {e}")
        return None


def get_cache_file(repo_name):
    """Get cache file path for a repository"""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    return CACHE_DIR / f"{repo_name}.json"


def should_check_repo(repo_name, check_interval_hours=DEFAULT_CHECK_INTERVAL_HOURS):
    """Check if we should check this repository based on cache timestamp"""
    cache_file = get_cache_file(repo_name)

    if not cache_file.exists():
        return True

    try:
        with open(cache_file, "r") as f:
            cache_data = json.load(f)

        last_check = datetime.fromisoformat(cache_data.get("last_check", "1970-01-01"))
        return datetime.now() - last_check > timedelta(hours=check_interval_hours)
    except (json.JSONDecodeError, ValueError, IOError):
        return True  # If cache is corrupted, check again


def cache_repo_data(repo_name, data):
    """Cache repository data with timestamp"""
    cache_file = get_cache_file(repo_name)

    cache_data = {"last_check": datetime.now().isoformat(), "data": data}

    try:
        with open(cache_file, "w") as f:
            json.dump(cache_data, f, indent=2)
    except IOError as e:
        log_error(f"Failed to cache data for {repo_name}: {e}")


def get_cached_repo_data(repo_name):
    """Get cached repository data"""
    cache_file = get_cache_file(repo_name)

    if not cache_file.exists():
        return None

    try:
        with open(cache_file, "r") as f:
            cache_data = json.load(f)
            return cache_data.get("data")
    except (json.JSONDecodeError, IOError):
        return None


def is_git_repo(path):
    """Check if a directory is a git repository"""
    git_dir = path / ".git"
    return git_dir.exists() or git_dir.is_dir()


def get_git_remote_url(repo_path):
    """Get the remote URL for a git repository"""
    try:
        result = subprocess.run(
            ["git", "config", "--get", "remote.origin.url"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return None
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
        return None


def get_git_current_commit(repo_path):
    """Get the current commit hash for a git repository"""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return None
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
        return None


def parse_github_url(url):
    """Parse GitHub URL to extract owner and repo"""
    if not url:
        return None, None

    # Handle various GitHub URL formats:
    # https://github.com/owner/repo.git
    # git@github.com:owner/repo.git
    # https://github.com/owner/repo

    if "github.com" not in url:
        return None, None

    # Remove protocol and git@ prefix
    url = url.replace("https://", "").replace("http://", "").replace("git@", "")

    # Remove .git suffix
    url = url.replace(".git", "")

    # Split by / and take last two parts
    parts = url.split("/")
    if len(parts) >= 2:
        owner = parts[-2]
        repo = parts[-1]
        return owner, repo

    return None, None


def get_github_latest_commit(owner, repo, branch="main"):
    """Get latest commit information from GitHub API"""
    try:
        # GitHub API for latest commit
        url = f"https://api.github.com/repos/{owner}/{repo}/commits/{branch}"

        req = urllib.request.Request(url)
        req.add_header("User-Agent", "Claude-Code-Plugin-Updater/1.0")

        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                return {
                    "sha": data["sha"],
                    "date": data["commit"]["committer"]["date"],
                    "message": data["commit"]["message"],
                }
            else:
                log_error(
                    f"GitHub API returned status {response.status} for {owner}/{repo}"
                )
                return None

    except urllib.error.URLError as e:
        log_error(f"Failed to fetch latest commit for {owner}/{repo}: {e}")
        return None
    except Exception as e:
        log_error(f"Unexpected error fetching latest commit for {owner}/{repo}: {e}")
        return None


def check_repo_update(repo_path, repo_name):
    """Check if a repository has updates"""
    # Get remote URL
    remote_url = get_git_remote_url(repo_path)
    if not remote_url:
        return {"has_update": False, "error": "No remote URL found"}

    # Parse GitHub URL
    owner, repo = parse_github_url(remote_url)
    if not owner or not repo:
        return {"has_update": False, "error": "Not a GitHub repository"}

    # Get current commit
    current_commit = get_git_current_commit(repo_path)
    if not current_commit:
        return {"has_update": False, "error": "Could not get current commit"}

    # Get latest commit from GitHub
    latest_commit = get_github_latest_commit(owner, repo)
    if not latest_commit:
        return {"has_update": False, "error": "Could not fetch latest commit"}

    # Compare commits (compare full hashes, but display short versions)
    has_update = current_commit != latest_commit["sha"]

    return {
        "has_update": has_update,
        "current_commit": current_commit[:7],
        "latest_commit": latest_commit,
        "remote_url": remote_url,
        "owner": owner,
        "repo": repo,
    }


def find_plugin_repos():
    """Find all git repositories in the plugins directory"""
    repos = []

    # Check both plugins directory and marketplaces subdirectory
    search_dirs = [PLUGINS_DIR, PLUGINS_DIR / "marketplaces"]

    for search_dir in search_dirs:
        if not search_dir.exists():
            log_info(f"Directory not found: {search_dir}")
            continue

        for item in search_dir.iterdir():
            if item.is_dir() and is_git_repo(item):
                repos.append((item.name, item))

    return repos


def format_update_context(updates):
    """Format updates as context for SessionStart hook"""
    if not updates:
        return None

    context_lines = ["## 🔄 Plugin Repository Updates"]
    context_lines.append("")

    update_count = sum(1 for u in updates if u.get("has_update"))
    error_count = sum(1 for u in updates if u.get("error"))

    if update_count == 0 and error_count == 0:
        context_lines.append("✅ All plugin repositories are up to date")
    else:
        if update_count > 0:
            context_lines.append(
                f"⚠️ {update_count} plugin repositor{'y has' if update_count == 1 else 'ies have'} updates available:"
            )
            context_lines.append("")

        for update in updates:
            repo_name = update["name"]
            if update.get("has_update"):
                latest_commit = update["latest_commit"]
                context_lines.append(f"• **{repo_name}**: Updates available")
                context_lines.append(f"  - Current: `{update['current_commit']}`")
                context_lines.append(f"  - Latest: `{latest_commit['sha'][:7]}`")
                context_lines.append(f"  - Message: {latest_commit['message'][:50]}...")
                context_lines.append("")
            elif update.get("error"):
                context_lines.append(f"• **{repo_name}**: ❌ {update['error']}")
            else:
                context_lines.append(f"• **{repo_name}**: ✅ Up to date")

    return "\n".join(context_lines)


def main():
    """Main hook execution"""
    # Read hook input
    hook_input = read_hook_input()
    if not hook_input:
        sys.exit(1)

    hook_event = hook_input.get("hook_event_name")
    source = hook_input.get("source", "")

    log_info(f"Hook triggered: {hook_event} (source: {source})")

    # Only run on startup/resume events
    if hook_event != "SessionStart":
        log_info(f"Skipping hook event: {hook_event}")
        sys.exit(0)

    # Find plugin repositories
    repos = find_plugin_repos()
    if not repos:
        log_info("No plugin repositories found")
        sys.exit(0)

    log_info(f"Found {len(repos)} plugin repositories to check")

    updates = []

    # Check each repository for updates
    for repo_name, repo_path in repos:
        log_info(f"Checking repository: {repo_name}")

        # Check for updates (no caching)
        update_info = check_repo_update(repo_path, repo_name)

        updates.append({"name": repo_name, **update_info})

        # Small delay to avoid rate limiting
        time.sleep(0.5)

    # Format and return context
    context = format_update_context(updates)

    if context:
        # Return JSON output for SessionStart hook
        output = {"systemMessage": context}
        print(json.dumps(output))
        log_info("Update context provided to user")
    else:
        log_info("No updates to report")


if __name__ == "__main__":
    main()
