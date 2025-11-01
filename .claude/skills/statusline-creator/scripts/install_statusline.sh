#!/bin/bash
# Install a statusline configuration to Claude Code settings
# Usage: ./install_statusline.sh <template-name-or-custom-string> [--backup]

set -euo pipefail

SETTINGS_FILE="$HOME/.claude/settings.json"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
TEMPLATES_DIR="$SKILL_DIR/assets/templates"

# Parse arguments
STATUSLINE=""
BACKUP=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --backup)
            BACKUP=true
            shift
            ;;
        *)
            STATUSLINE="$1"
            shift
            ;;
    esac
done

if [ -z "$STATUSLINE" ]; then
    echo "Usage: $0 <template-name-or-custom-string> [--backup]"
    echo ""
    echo "Available templates:"
    if [ -d "$TEMPLATES_DIR" ]; then
        for template in "$TEMPLATES_DIR"/*.json; do
            if [ -f "$template" ]; then
                basename "$template" .json
            fi
        done
    fi
    exit 1
fi

# Check if statusline is a template name
TEMPLATE_FILE="$TEMPLATES_DIR/${STATUSLINE}.json"
if [ -f "$TEMPLATE_FILE" ]; then
    echo "📋 Loading template: $STATUSLINE"
    STATUSLINE_CONFIG=$(cat "$TEMPLATE_FILE")
else
    echo "📝 Using custom statusline string"
    # Escape the statusline for JSON
    STATUSLINE_ESCAPED=$(echo "$STATUSLINE" | python3 -c 'import json, sys; print(json.dumps(sys.stdin.read().strip()))')
    STATUSLINE_CONFIG="{\"statusline\": {\"format\": $STATUSLINE_ESCAPED}}"
fi

# Backup existing settings if requested
if [ "$BACKUP" = true ] && [ -f "$SETTINGS_FILE" ]; then
    BACKUP_FILE="${SETTINGS_FILE}.backup.$(date +%Y%m%d_%H%M%S)"
    cp "$SETTINGS_FILE" "$BACKUP_FILE"
    echo "💾 Backed up existing settings to: $BACKUP_FILE"
fi

# Ensure settings directory exists
mkdir -p "$(dirname "$SETTINGS_FILE")"

# Merge with existing settings or create new file
if [ -f "$SETTINGS_FILE" ]; then
    echo "🔄 Merging with existing settings..."
    python3 -c "
import json
import sys

# Read existing settings
with open('$SETTINGS_FILE') as f:
    settings = json.load(f)

# Read new statusline config
new_config = json.loads('$STATUSLINE_CONFIG')

# Merge
settings.update(new_config)

# Write back
with open('$SETTINGS_FILE', 'w') as f:
    json.dump(settings, f, indent=2)
"
else
    echo "📄 Creating new settings file..."
    echo "$STATUSLINE_CONFIG" | python3 -m json.tool > "$SETTINGS_FILE"
fi

echo "✅ Statusline installed successfully!"
echo ""
echo "Your new statusline will appear in Claude Code."
echo "Restart Claude Code if the changes don't appear immediately."
