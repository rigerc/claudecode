#!/bin/bash
# Get MCP server status for statusline display with caching and performance tracking
# Usage: ./get_mcp_status.sh [--format json|text|statusline] [--cache-dir /path] [--benchmark]

set -euo pipefail

# Configuration
FORMAT="text"
CACHE_DIR="${TMPDIR:-/tmp}/claude-mcp-cache"
CACHE_DURATION=30  # seconds
BENCHMARK=false
CLEANUP=false

# Create cache directory if it doesn't exist
mkdir -p "$CACHE_DIR"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --format)
            FORMAT="$2"
            shift 2
            ;;
        --cache-dir)
            CACHE_DIR="$2"
            shift 2
            ;;
        --benchmark)
            BENCHMARK=true
            shift
            ;;
        --cleanup)
            CLEANUP=true
            shift
            ;;
        *)
            shift
            ;;
    esac
done

# Cleanup cache files older than cache duration
cleanup_cache() {
    find "$CACHE_DIR" -name "mcp_status_*" -type f -mtime +$((${CACHE_DURATION}/86400+1)) -delete 2>/dev/null || true
}

# Get current timestamp
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

# Parse MCP server status
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
        echo "0|0||error"
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

# Get status with caching
get_cached_mcp_status() {
    local cache_file
    cache_file=$(get_cache_file)

    cleanup_cache

    if is_cache_valid "$cache_file" && [[ "$BENCHMARK" != "true" ]]; then
        cat "$cache_file"
    else
        local status
        status=$(get_mcp_status)
        echo "$status" | tee "$cache_file"
    fi
}

# Generate status text
get_status_text() {
    local online="${1:-0}"
    local total="${2:-0}"
    local servers="${3:-}"

    if [[ "$total" -eq 0 ]]; then
        echo "MCP: No servers"
    elif [[ "$online" -eq "$total" ]]; then
        echo "MCP: $online/$total ✓"
    elif [[ "$online" -gt 0 ]]; then
        echo "MCP: $online/$total ⚠"
    else
        echo "MCP: $online/$total ✗"
    fi
}

# Get color code based on status
get_status_color() {
    local online="$1"
    local total="$2"

    if [[ "$total" -eq 0 ]]; then
        echo "90"  # Bright black (gray)
    elif [[ "$online" -eq "$total" ]]; then
        echo "32"  # Green
    elif [[ "$online" -gt 0 ]]; then
        echo "33"  # Yellow
    else
        echo "31"  # Red
    fi
}

# Main execution
main() {
    if [[ "$CLEANUP" == "true" ]]; then
        cleanup_cache
        exit 0
    fi

    local status_info
    status_info=$(get_cached_mcp_status)

    IFS='|' read -r online total servers duration _ <<< "$status_info"

    case "$FORMAT" in
        json)
            local color_code
            color_code=$(get_status_color "$online" "$total")
            local status_text
            status_text=$(get_status_text "$online" "$total")

            cat <<EOF
{
  "online": $online,
  "total": $total,
  "servers": "$servers",
  "status_text": "$status_text",
  "color_code": "$color_code",
  "duration_ms": ${duration:-0},
  "cache_duration": $CACHE_DURATION,
  "timestamp": $(get_timestamp)
}
EOF
            ;;
        statusline)
            local color_code
            color_code=$(get_status_color "$online" "$total")
            local status_text
            status_text=$(get_status_text "$online" "$total")

            # Output with ANSI color codes
            printf "\x1b[%sm%s\x1b[0m" "$color_code" "$status_text"

            # Add benchmark info if requested
            if [[ "$BENCHMARK" == "true" && -n "${duration:-}" ]]; then
                printf " \x1b[90m(%dms)\x1b[0m" "$duration"
            fi
            ;;
        benchmark)
            echo "MCP Status Benchmark Results:"
            echo "============================"
            echo "Online servers: $online/$total"
            echo "Server list: $servers"
            echo "Command duration: ${duration:-N/A}ms"
            echo "Cache duration: ${CACHE_DURATION}s"
            echo "Cache file: $(get_cache_file)"
            echo "Cache valid: $(is_cache_valid "$(get_cache_file)" && echo "Yes" || echo "No")"
            ;;
        *)
            # Human-readable text format
            echo "MCP Server Status:"
            echo "================="
            echo "Online: $online/$total servers"
            if [[ -n "$servers" ]]; then
                echo "Servers: $servers"
            fi
            echo "Status: $(get_status_text "$online" "$total")"
            if [[ -n "${duration:-}" ]]; then
                echo "Response time: ${duration}ms"
            fi
            echo "Cache duration: ${CACHE_DURATION}s"
            ;;
    esac
}

main "$@"