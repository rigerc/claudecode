#!/bin/bash
# Claude Code statusline with emojis, MCP server monitoring, git info, caching, and performance tracking
# This script displays: 📁 directory 🌿 git │ 🤖 MCP server status 🕒 time

set -euo pipefail

# Configuration
CACHE_DIR="${TMPDIR:-/tmp}/claude-mcp-cache"
CACHE_DURATION=30  # seconds

# Ensure cache directory exists
mkdir -p "$CACHE_DIR"

# Get current directory name with emoji
get_directory() {
    local dir_name
    dir_name=$(basename "$PWD")
    echo "📁 $dir_name"
}

# Get current time with emoji
get_time() {
    local current_time
    current_time=$(date +%H:%M)
    echo "🕒 $current_time"
}

# Get git information with emojis and colors
get_git_info() {
    # Check if we're in a git repository
    if ! git rev-parse --git-dir >/dev/null 2>&1; then
        return 0
    fi

    # Get branch name
    local branch
    branch=$(git branch --show-current 2>/dev/null || echo "HEAD")

    # Get repository status (dirty/clean)
    local status_indicator=""
    local status_emoji=""
    local dirty=false
    if ! git diff --quiet >/dev/null 2>&1 || ! git diff --cached --quiet >/dev/null 2>&1 || [ -n "$(git ls-files --others --exclude-standard 2>/dev/null)" ]; then
        dirty=true
        status_indicator="*"
        status_emoji="🔥"
    else
        status_emoji="✅"
    fi

    # Get ahead/behind info (only if there's a remote)
    local ahead_behind=""
    local ahead_emoji=""
    if git rev-parse --verify @{upstream} >/dev/null 2>&1; then
        local ahead behind
        ahead=$(git rev-list --count @{upstream}..HEAD 2>/dev/null || echo "0")
        behind=$(git rev-list --count HEAD..@{upstream} 2>/dev/null || echo "0")

        if [[ "$ahead" -gt 0 ]]; then
            ahead_behind="↑$ahead"
            ahead_emoji="⬆️"
        fi
        if [[ "$behind" -gt 0 ]]; then
            ahead_behind="${ahead_behind}↓$behind"
            ahead_emoji="${ahead_emoji}⬇️"
        fi
    fi

    # Format output with colors and emojis
    local git_info=""
    local emoji_display="🌿"

    if [[ "$dirty" == true ]]; then
        # Dirty - red with fire emoji
        git_info="\x1b[31m${branch}${status_indicator}\x1b[0m"
        emoji_display="🌿🔥"
    else
        # Clean - green with check emoji
        git_info="\x1b[32m${branch}\x1b[0m"
        emoji_display="🌿✅"
    fi

    # Add ahead/behind info in cyan with arrows
    if [[ -n "$ahead_behind" ]]; then
        git_info="${git_info} \x1b[36m${ahead_behind}\x1b[0m"
        emoji_display="${emoji_display} ${ahead_emoji}"
    fi

    echo -e "${emoji_display} ${git_info}"
}

# Get timestamp for cache
get_timestamp() {
    date +%s
}

# Get cache file path
get_cache_file() {
    echo "$CACHE_DIR/mcp_status_$(whoami)"
}

# Check if cache is valid
is_cache_valid() {
    local cache_file="$1"
    local current_time
    current_time=$(get_timestamp)

    if [[ -f "$cache_file" ]]; then
        local cache_time
        cache_time=$(stat -c %Y "$cache_file" 2>/dev/null || stat -f %m "$cache_file" 2>/dev/null || echo 0)
        local age=$((current_time - cache_time))
        [[ $age -lt $CACHE_DURATION ]]
    else
        false
    fi
}

# Parse MCP server status from command output
parse_mcp_status() {
    local output="$1"
    local online=0
    local total=0
    local servers=""

    while IFS= read -r line; do
        if [[ $line =~ ^[a-zA-Z0-9_-]+:.*Connected$ ]]; then
            ((online++))
            ((total++))
            local server_name
            server_name=$(echo "$line" | cut -d: -f1)
            servers="${servers}${server_name},"
        elif [[ $line =~ ^[a-zA-Z0-9_-]+: ]]; then
            ((total++))
            local server_name
            server_name=$(echo "$line" | cut -d: -f1)
            servers="${servers}${server_name},"
        fi
    done <<< "$output"

    servers="${servers%,}"  # Remove trailing comma

    # Ensure all variables have values
    online=${online:-0}
    total=${total:-0}
    servers=${servers:-""}

    echo "$online|$total|$servers"
}

# Get MCP server status with timing
get_mcp_status() {
    local start_time
    start_time=$(date +%s%N 2>/dev/null || date +%s)

    local mcp_output
    if ! mcp_output=$(claude mcp list 2>/dev/null); then
        echo "0|0||error|0"
        return 1
    fi

    local end_time
    end_time=$(date +%s%N 2>/dev/null || date +%s)
    local duration
    if [[ $start_time =~ ^[0-9]{10,}$ ]]; then
        duration=$(( (end_time - start_time) / 1000000 ))  # Convert to milliseconds
    else
        duration=$((end_time - start_time))
    fi

    local parsed
    parsed=$(parse_mcp_status "$mcp_output")
    echo "${parsed}|${duration}"
}

# Get MCP server status with caching and emojis
get_mcp_status_cached() {
    local cache_file
    cache_file=$(get_cache_file)

    # Clean up old cache files
    find "$CACHE_DIR" -name "mcp_status_*" -type f -mtime +$((${CACHE_DURATION}/86400+1)) -delete 2>/dev/null || true

    if is_cache_valid "$cache_file"; then
        # Use cached data
        local cached_data
        cached_data=$(cat "$cache_file")
    else
        # Get fresh data and cache it
        local fresh_data
        fresh_data=$(get_mcp_status)
        echo "$fresh_data" > "$cache_file"
        cached_data="$fresh_data"
    fi

    IFS='|' read -r online total servers duration _ <<< "$cached_data"

    # Build emoji-based status
    local emoji="🤖"
    local status_text=""
    local color_code=""

    if [[ "$total" -eq 0 ]]; then
        emoji="🚫"
        status_text="No servers"
        color_code="90"  # Bright black (gray)
    elif [[ "$online" -eq "$total" ]]; then
        emoji="🚀"
        status_text="$online/$total"
        color_code="32"  # Green
    elif [[ "$online" -gt 0 ]]; then
        emoji="⚠️"
        status_text="$online/$total"
        color_code="33"  # Yellow
    else
        emoji="💥"
        status_text="$online/$total"
        color_code="31"  # Red
    fi

    # Output with emojis and colors
    printf "\x1b[%sm%s %s\x1b[0m" "$color_code" "$emoji" "$status_text"
}

# Main statusline builder
build_statusline() {
    local directory
    directory=$(get_directory)

    local git_info
    git_info=$(get_git_info)

    local mcp_status
    mcp_status=$(get_mcp_status_cached)

    local time
    time=$(get_time)

    # Build the complete statusline with emojis
    if [[ -n "$git_info" ]]; then
        printf "%s │ %s │ %s │ %s" "$directory" "$git_info" "$mcp_status" "$time"
    else
        printf "%s │ %s │ %s" "$directory" "$mcp_status" "$time"
    fi
}

# Main execution
build_statusline