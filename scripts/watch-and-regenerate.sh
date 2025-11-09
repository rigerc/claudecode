#!/bin/bash

# Watch .claude directory for changes and regenerate marketplace automatically

set -euo pipefail

echo "👀 Watching .claude directory for changes..."
echo "📝 Changes will automatically regenerate the marketplace"
echo "🛑 Press Ctrl+C to stop watching"
echo

# Check if inotifywait is available
if ! command -v inotifywait &> /dev/null; then
    echo "❌ inotifywait not found. Install with:"
    echo "   Ubuntu/Debian: sudo apt install inotify-tools"
    echo "   macOS: brew install inotify-tools"
    echo "   Or run manually: python3 scripts/generate-marketplace.py"
    exit 1
fi

# Initial generation
echo "🚀 Running initial generation..."
python3 scripts/generate-marketplace.py

# Watch for changes
while true; do
    # Wait for any change in .claude directory
    inotifywait -r -e modify,create,delete,move .claude/ \
        --exclude='__pycache__|\.git|\.DS_Store' \
        --quiet \
        --monitor \
        --recursive \
        --event modify,create,delete,move 2>/dev/null

    echo
    echo "📝 Change detected in .claude directory..."
    echo "🔄 Regenerating marketplace..."

    # Regenerate marketplace
    if python3 scripts/generate-marketplace.py; then
        echo "✅ Marketplace regenerated successfully!"
    else
        echo "❌ Error regenerating marketplace - check your changes"
    fi

    echo
    echo "👀 Continuing to watch for changes..."
done