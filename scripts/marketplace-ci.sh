#!/bin/bash

# Marketplace CI Script
# Runs validation on all plugins in the marketplace

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counter for results
TOTAL_PLUGINS=0
PASSED_PLUGINS=0
FAILED_PLUGINS=0

# Logging functions
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "========================================"
echo "🏪 Claude Code Marketplace CI"
echo "========================================"
echo

# Validate marketplace.json first
log_info "Validating marketplace.json..."

if [[ ! -f "$PROJECT_ROOT/.claude-plugin/marketplace.json" ]]; then
    log_error "marketplace.json not found"
    exit 1
fi

# Check if marketplace.json is valid JSON
if ! python3 -m json.tool "$PROJECT_ROOT/.claude-plugin/marketplace.json" > /dev/null 2>&1; then
    log_error "marketplace.json is not valid JSON"
    exit 1
fi

log_success "marketplace.json is valid"

# Get list of plugins from marketplace.json
plugins=($(jq -r '.plugins[].name' "$PROJECT_ROOT/.claude-plugin/marketplace.json"))

echo "Found ${#plugins[@]} plugins to validate"
echo

# Validate each plugin
for plugin in "${plugins[@]}"; do
    ((TOTAL_PLUGINS++))
    echo "========================================"
    echo "🔍 Validating plugin: $plugin"
    echo "========================================"

    plugin_path="$PROJECT_ROOT/plugins/$plugin"

    if [[ ! -d "$plugin_path" ]]; then
        log_error "Plugin directory '$plugin_path' not found"
        ((FAILED_PLUGINS++))
        continue
    fi

    # Run validation script
    if "$SCRIPT_DIR/validate-plugin.sh" "$plugin_path"; then
        log_success "Plugin '$plugin' passed validation"
        ((PASSED_PLUGINS++))
    else
        log_error "Plugin '$plugin' failed validation"
        ((FAILED_PLUGINS++))
    fi

    echo
done

echo "========================================"
echo "📊 CI Results Summary"
echo "========================================"
echo -e "📦 Total plugins: $TOTAL_PLUGINS"
echo -e "${GREEN}✅ Passed: $PASSED_PLUGINS${NC}"
echo -e "${RED}❌ Failed: $FAILED_PLUGINS${NC}"
echo

# Exit with appropriate code
if [[ "$FAILED_PLUGINS" -gt 0 ]]; then
    log_error "CI failed: $FAILED_PLUGINS plugin(s) failed validation"
    exit 1
else
    log_success "CI passed: All $TOTAL_PLUGINS plugins are valid"
    exit 0
fi