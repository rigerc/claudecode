#!/bin/bash
# Get system information for statusline display
# Usage: ./get_system_info.sh [--format json|text|statusline] [--components component1,component2,...]

set -euo pipefail

FORMAT="text"
COMPONENTS="time,user,host,load"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --format)
            FORMAT="$2"
            shift 2
            ;;
        --components)
            COMPONENTS="$2"
            shift 2
            ;;
        *)
            shift
            ;;
    esac
done

# Get current time
get_time() {
    date '+%H:%M:%S'
}

# Get current user
get_user() {
    whoami
}

# Get hostname
get_host() {
    hostname -s
}

# Get system load (1-min average)
get_load() {
    if [ -f /proc/loadavg ]; then
        cut -d' ' -f1 /proc/loadavg
    else
        uptime | awk -F'load average:' '{print $2}' | awk '{print $1}' | tr -d ','
    fi
}

# Get memory usage percentage
get_memory() {
    if command -v free > /dev/null 2>&1; then
        free | grep Mem | awk '{printf "%.0f%%", $3/$2 * 100.0}'
    else
        echo "N/A"
    fi
}

# Get CPU cores
get_cores() {
    if [ -f /proc/cpuinfo ]; then
        grep -c ^processor /proc/cpuinfo
    else
        sysctl -n hw.ncpu 2>/dev/null || echo "N/A"
    fi
}

# Get current directory (shortened)
get_pwd() {
    pwd | sed "s|^$HOME|~|"
}

# Build output based on format
case "$FORMAT" in
    json)
        cat <<EOF
{
  "time": "$(get_time)",
  "user": "$(get_user)",
  "host": "$(get_host)",
  "load": "$(get_load)",
  "memory": "$(get_memory)",
  "cores": "$(get_cores)",
  "pwd": "$(get_pwd)"
}
EOF
        ;;
    statusline)
        # Compact format for statusline
        OUTPUT=""
        IFS=',' read -ra COMP <<< "$COMPONENTS"
        for component in "${COMP[@]}"; do
            case "$component" in
                time)
                    OUTPUT="${OUTPUT}$(get_time) "
                    ;;
                user)
                    OUTPUT="${OUTPUT}$(get_user) "
                    ;;
                host)
                    OUTPUT="${OUTPUT}@$(get_host) "
                    ;;
                load)
                    OUTPUT="${OUTPUT}[$(get_load)] "
                    ;;
                memory)
                    OUTPUT="${OUTPUT}mem:$(get_memory) "
                    ;;
                pwd)
                    OUTPUT="${OUTPUT}$(get_pwd) "
                    ;;
            esac
        done
        echo "${OUTPUT% }"  # Remove trailing space
        ;;
    *)
        # Human-readable text format
        echo "Time: $(get_time)"
        echo "User: $(get_user)"
        echo "Host: $(get_host)"
        echo "Load: $(get_load)"
        echo "Memory: $(get_memory)"
        echo "Cores: $(get_cores)"
        echo "PWD: $(get_pwd)"
        ;;
esac
