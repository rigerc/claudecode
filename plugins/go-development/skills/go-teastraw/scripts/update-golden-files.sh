#!/bin/bash

# Update Golden Files Script for Teastraw TUI Testing
# This script updates golden files for all TUI tests

set -e

echo "Updating golden files for TUI tests..."

# Check if we're in a Go project
if [ ! -f "go.mod" ]; then
    echo "Error: No go.mod file found. Please run this script from the root of a Go project."
    exit 1
fi

# Create testdata directory if it doesn't exist
mkdir -p testdata

# Backup existing golden files
if [ -d "testdata" ] && [ "$(ls -A testdata 2>/dev/null)" ]; then
    echo "Backing up existing golden files..."
    backup_dir="testdata/backup_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$backup_dir"
    cp testdata/*.golden "$backup_dir/" 2>/dev/null || true
    echo "Backup created: $backup_dir"
fi

# Run tests with -update flag to update golden files
echo "Running tests to update golden files..."
if [ -d "tests/tui" ]; then
    echo "Updating golden files in tests/tui/..."
    go test ./tests/tui/... -update -v
fi

if [ -d "tests/integration" ]; then
    echo "Updating golden files in tests/integration/..."
    go test ./tests/integration/... -update -v
fi

# Check for test files in root directory
find . -maxdepth 1 -name "*_test.go" -type f | while read test_file; do
    echo "Updating golden files for $(basename "$test_file")..."
    go test -run "$(basename "$test_file" _test.go)" -update -v
done

# List updated golden files
echo ""
echo "Updated golden files:"
if [ -d "testdata" ]; then
    find testdata -name "*.golden" -type f -exec ls -la {} \; | while read line; do
        echo "  $line"
    done
fi

echo ""
echo "Golden file update complete!"
echo ""
echo "To review changes:"
echo "  1. Check the backup directory (if created): $backup_dir"
echo "  2. Use 'git diff' to see changes"
echo "  3. Run tests normally to verify: go test ./tests/tui/..."
echo ""
echo "If you need to restore from backup:"
echo "  cp $backup_dir/*.golden testdata/"

# Optional: Open editor for reviewing changes
if command -v code >/dev/null 2>&1; then
    read -p "Open golden files in VS Code for review? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if [ -d "testdata" ]; then
            code testdata/*.golden
        fi
    fi
fi