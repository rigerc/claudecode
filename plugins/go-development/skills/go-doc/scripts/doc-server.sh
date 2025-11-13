#!/bin/bash

# Go Doc HTTP Server Management Script
# This script manages the go doc HTTP documentation server

set -e

# Default configuration
DEFAULT_PORT=6060
DEFAULT_HOST="localhost"
PID_FILE="/tmp/go-doc-server.pid"
LOG_FILE="/tmp/go-doc-server.log"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored output
print_status() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Show help
show_help() {
    cat << EOF
Go Doc HTTP Server Management Script

USAGE:
    $0 [COMMAND] [OPTIONS]

COMMANDS:
    start [PORT]         Start the documentation server
    stop                 Stop the documentation server
    restart [PORT]      Restart the documentation server
    status              Show server status
    logs                Show server logs
    open [PACKAGE]      Start server and open in browser

OPTIONS:
    PORT                Port number (default: 6060)
    PACKAGE             Package to document (default: current directory)

EXAMPLES:
    $0 start                    # Start server on default port 6060
    $0 start 8080              # Start server on port 8080
    $0 start 8080 net/http     # Document net/http package on port 8080
    $0 stop                     # Stop running server
    $0 status                   # Check server status
    $0 open                     # Start server and open browser
    $0 open fmt                 # Start server for fmt package and open browser

ENVIRONMENT VARIABLES:
    GO_DOC_PORT        Default port for server
    GO_DOC_HOST        Default host for server
    GO_DOC_BROWSER     Browser command (default: auto-detect)

EOF
}

# Check if server is running
is_server_running() {
    if [ -f "$PID_FILE" ]; then
        local pid=$(cat "$PID_FILE")
        if ps -p "$pid" > /dev/null 2>&1; then
            return 0
        else
            # PID file exists but process is dead
            rm -f "$PID_FILE"
            return 1
        fi
    fi
    return 1
}

# Get server URL
get_server_url() {
    local port=${1:-${GO_DOC_PORT:-$DEFAULT_PORT}}
    local host=${GO_DOC_HOST:-$DEFAULT_HOST}
    echo "http://$host:$port"
}

# Start server
start_server() {
    local port=${1:-${GO_DOC_PORT:-$DEFAULT_PORT}}
    local package=${2:-""}

    if is_server_running; then
        print_status $YELLOW "Server is already running on $(get_server_url $port)"
        return 1
    fi

    local url=$(get_server_url $port)
    print_status $BLUE "Starting Go doc server on $url"

    # Build the command
    local cmd="go doc -http=$url"

    # Add package if specified
    if [ -n "$package" ]; then
        # Change to package directory
        local pkg_dir=$(go list -f '{{.Dir}}' "$package" 2>/dev/null || echo "")
        if [ -n "$pkg_dir" ] && [ -d "$pkg_dir" ]; then
            cd "$pkg_dir"
            print_status $BLUE "Documenting package: $package"
        else
            print_status $RED "Package '$package' not found"
            return 1
        fi
    fi

    # Start server in background
    nohup $cmd > "$LOG_FILE" 2>&1 &
    local pid=$!

    # Save PID
    echo "$pid" > "$PID_FILE"

    # Wait a moment for server to start
    sleep 2

    if is_server_running; then
        print_status $GREEN "Server started successfully on $url"
        print_status $BLUE "Package directory: $(pwd)"
        print_status $BLUE "Logs: $LOG_FILE"
    else
        print_status $RED "Failed to start server"
        if [ -f "$LOG_FILE" ]; then
            print_status $RED "Error logs:"
            cat "$LOG_FILE"
        fi
        return 1
    fi
}

# Stop server
stop_server() {
    if ! is_server_running; then
        print_status $YELLOW "Server is not running"
        return 1
    fi

    local pid=$(cat "$PID_FILE")
    print_status $BLUE "Stopping Go doc server (PID: $pid)"

    kill "$pid" 2>/dev/null || true

    # Wait for process to stop
    local count=0
    while ps -p "$pid" > /dev/null 2>&1 && [ $count -lt 10 ]; do
        sleep 1
        count=$((count + 1))
    done

    # Force kill if still running
    if ps -p "$pid" > /dev/null 2>&1; then
        print_status $YELLOW "Force killing server process"
        kill -9 "$pid" 2>/dev/null || true
    fi

    rm -f "$PID_FILE"
    print_status $GREEN "Server stopped"
}

# Restart server
restart_server() {
    local port=${1:-${GO_DOC_PORT:-$DEFAULT_PORT}}
    local package=${2:-""}

    print_status $BLUE "Restarting Go doc server"
    stop_server
    sleep 1
    start_server "$port" "$package"
}

# Show server status
show_status() {
    if is_server_running; then
        local pid=$(cat "$PID_FILE")
        local port=$(ps -p "$pid" -o args= | grep -o '\:[0-9]\+' | head -1 | cut -c2-)
        local url=$(get_server_url "$port")
        print_status $GREEN "Server is running on $url (PID: $pid)"

        # Show package info
        if [ -f "$LOG_FILE" ]; then
            local cwd=$(grep "go doc" "$LOG_FILE" | head -1 | sed 's/.*go doc -http=\([^ ]*\).*/\1/')
            print_status $BLUE "Working directory: $(pwd)"
        fi
    else
        print_status $RED "Server is not running"
    fi
}

# Show logs
show_logs() {
    if [ -f "$LOG_FILE" ]; then
        print_status $BLUE "Server logs ($LOG_FILE):"
        cat "$LOG_FILE"
    else
        print_status $YELLOW "No log file found"
    fi
}

# Detect browser command
detect_browser() {
    if [ -n "$GO_DOC_BROWSER" ]; then
        echo "$GO_DOC_BROWSER"
        return
    fi

    # Try common browsers
    if command -v xdg-open > /dev/null; then
        echo "xdg-open"
    elif command -v open > /dev/null; then
        echo "open"
    elif command -v firefox > /dev/null; then
        echo "firefox"
    elif command -v google-chrome > /dev/null; then
        echo "google-chrome"
    elif command -v chromium > /dev/null; then
        echo "chromium"
    else
        echo ""
    fi
}

# Start server and open browser
start_and_open() {
    local port=${1:-${GO_DOC_PORT:-$DEFAULT_PORT}}
    local package=${2:-""}

    start_server "$port" "$package"

    if is_server_running; then
        local url=$(get_server_url "$port")
        local browser=$(detect_browser)

        if [ -n "$browser" ]; then
            print_status $BLUE "Opening $url in browser"
            $browser "$url" 2>/dev/null &
        else
            print_status $YELLOW "Could not detect browser. Please open manually: $url"
        fi
    else
        print_status $RED "Failed to start server"
        return 1
    fi
}

# Parse command line arguments
case "${1:-}" in
    "start")
        start_server "$2" "$3"
        ;;
    "stop")
        stop_server
        ;;
    "restart")
        restart_server "$2" "$3"
        ;;
    "status")
        show_status
        ;;
    "logs")
        show_logs
        ;;
    "open")
        start_and_open "$2" "$3"
        ;;
    "help"|"--help"|"-h")
        show_help
        ;;
    "")
        show_help
        ;;
    *)
        print_status $RED "Unknown command: $1"
        show_help
        exit 1
        ;;
esac