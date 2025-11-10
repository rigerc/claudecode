#!/bin/bash

# Automatic setup script for MarkdownTaskManager plugin
# This script runs silently via hooks and only creates files if they don't exist

set -e  # Exit on any error

# Get the directory where this script is located
SCRIPT_DIR="$CLAUDE_PLUGIN_ROOT/hooks/scripts"
ASSETS_DIR="$CLAUDE_PLUGIN_ROOT/hooks/assets"

PROJECT_ROOT="$CLAUDE_PROJECT_DIR"

# Check if PROJECT_ROOT is set and not empty
if [[ -z "$PROJECT_ROOT" ]]; then
    echo "No project root found. Exiting."
    exit 1
fi

# Function to copy file if it doesn't exist (silent version)
copy_if_not_exists_silent() {
    local src="$1"
    local dest="$2"

    if [[ -f "$dest" ]]; then
        return 0
    fi

    if [[ -f "$src" ]]; then
        cp "$src" "$dest"
        return 0
    else
        return 1
    fi
}

# Function to download file if it doesn't exist (silent version)
download_if_not_exists_silent() {
    local url="$1"
    local dest="$2"

    if [[ -f "$dest" ]]; then
        return 0
    fi

    # Try curl first, then wget as fallback
    if command -v curl >/dev/null 2>&1; then
        curl -fsSL "$url" -o "$dest" >/dev/null 2>&1 || return 1
    elif command -v wget >/dev/null 2>&1; then
        wget -q "$url" -O "$dest" >/dev/null 2>&1 || return 1
    else
        return 1
    fi

    return 0
}

# Function to handle CLAUDE.md - create or append to existing file (silent version)
setup_claude_md_silent() {
    local claude_example="$ASSETS_DIR/CLAUDE.MD.EXAMPLE"
    local claude_md="$PROJECT_ROOT/CLAUDE.md"

    if [[ ! -f "$claude_example" ]]; then
        return 1
    fi

    if [[ -f "$claude_md" ]]; then
        # Check if AI_WORKFLOW.md reference already exists
        if grep -q "AI_WORKFLOW.md" "$claude_md"; then
            return 0
        else
            echo "" >> "$claude_md"
            echo "---" >> "$claude_md"
            cat "$claude_example" >> "$claude_md"
            return 0
        fi
    else
        # Create new CLAUDE.md with the example content
        cp "$claude_example" "$claude_md"
        return 0
    fi
}

# Check if assets directory exists
if [[ ! -d "$ASSETS_DIR" ]]; then
    exit 1
fi

# Only run setup if we haven't already set up the basic files
if [[ -f "$PROJECT_ROOT/kanban.md" && -f "$PROJECT_ROOT/archive.md" && -f "$PROJECT_ROOT/AI_WORKFLOW.md" ]]; then
    exit 0  # Already set up, exit successfully
fi

# Copy asset files
copy_if_not_exists_silent "$ASSETS_DIR/kanban.md" "$PROJECT_ROOT/kanban.md"
copy_if_not_exists_silent "$ASSETS_DIR/archive.md" "$PROJECT_ROOT/archive.md"
copy_if_not_exists_silent "$ASSETS_DIR/AI_WORKFLOW.MD" "$PROJECT_ROOT/AI_WORKFLOW.md"

# Handle CLAUDE.md setup
setup_claude_md_silent

# Download task-manager.html
download_if_not_exists_silent "https://raw.githubusercontent.com/ioniks/MarkdownTaskManager/refs/heads/master/task-manager.html" "$PROJECT_ROOT/task-manager.html"

exit 0