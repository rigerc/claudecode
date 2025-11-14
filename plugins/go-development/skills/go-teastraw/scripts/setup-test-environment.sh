#!/bin/bash

# Setup Test Environment for Teastraw TUI Testing
# This script prepares the environment for running TUI tests with Teastraw

set -e

echo "Setting up Teastraw test environment..."

# Check if we're in a Go project
if [ ! -f "go.mod" ]; then
    echo "Error: No go.mod file found. Please run this script from the root of a Go project."
    exit 1
fi

# Install Teastraw dependency
echo "Installing Teastraw dependency..."
go get github.com/fiffeek/teastraw

# Create testdata directory if it doesn't exist
if [ ! -d "testdata" ]; then
    echo "Creating testdata directory..."
    mkdir -p testdata
fi

# Set up environment variables for consistent testing
echo "Setting up test environment variables..."

# Create a .env.test file for consistent testing
cat > .env.test << 'EOF'
# Teastraw Test Environment Variables
TEST_MODE=1
NO_COLOR=1
TERM=xterm-256color
COLUMNS=80
LINES=24
CI=true
EOF

# Create basic test directory structure
echo "Creating test directory structure..."
mkdir -p tests/tui
mkdir -p tests/integration

# Example test file template
cat > tests/tui/example_test.go << 'EOF'
package tui

import (
    "bytes"
    "os/exec"
    "testing"
    "time"

    "github.com/fiffeek/teastraw/exp"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
)

// getAppCmd returns the command for your TUI application
// Modify this to point to your actual application
func getAppCmd() *exec.Cmd {
    return exec.Command("go", "run", "./cmd/your-app")
}

func TestBasicExample(t *testing.T) {
    runner, err := exp.NewTestRunner(
        exp.WithInitialTermSize(80, 24),
        exp.WithCommand(getAppCmd()),
    )
    require.NoError(t, err)
    defer runner.Cleanup()

    // Wait for initial screen
    _, err = runner.WaitFor(func(screen []byte) bool {
        return len(screen) > 0 // Basic check that app started
    }, exp.WithDuration(5*time.Second))
    require.NoError(t, err)

    // Test basic functionality here...
    t.Log("Basic test completed successfully")
}
EOF

# Create a Makefile for common test operations
cat > Makefile.test << 'EOF'
# Teastraw TUI Testing Makefile

.PHONY: test-tui test-tui-verbose test-tui-update test-tui-clean test-tui-help

# Run all TUI tests
test-tui:
	@echo "Running TUI tests..."
	go test ./tests/tui/...

# Run TUI tests with verbose output
test-tui-verbose:
	@echo "Running TUI tests with verbose output..."
	go test -v ./tests/tui/...

# Update golden files for TUI tests
test-tui-update:
	@echo "Updating golden files for TUI tests..."
	go test ./tests/tui/... -update

# Clean test cache and artifacts
test-tui-clean:
	@echo "Cleaning TUI test cache..."
	go clean -testcache
	rm -f tests/tui/*_test.go

# Show help for TUI testing
test-tui-help:
	@echo "Teastraw TUI Testing Commands:"
	@echo "  test-tui        - Run all TUI tests"
	@echo "  test-tui-verbose- Run TUI tests with verbose output"
	@echo "  test-tui-update - Update golden files"
	@echo "  test-tui-clean  - Clean test cache and artifacts"
	@echo "  test-tui-help   - Show this help"

# Check if your application builds
check-build:
	@echo "Checking if application builds..."
	go build ./cmd/your-app
	@echo "Build successful!"

# Run application manually for debugging
run-app:
	@echo "Running application manually..."
	go run ./cmd/your-app
EOF

echo "Test environment setup complete!"
echo ""
echo "Next steps:"
echo "1. Modify tests/tui/example_test.go to point to your actual application"
echo "2. Create your TUI tests in the tests/tui/ directory"
echo "3. Use 'make -f Makefile.test test-tui' to run your tests"
echo "4. Use 'make -f Makefile.test test-tui-update' to update golden files"
echo ""
echo "Environment variables have been set in .env.test"
echo "Source this file before running tests: source .env.test"