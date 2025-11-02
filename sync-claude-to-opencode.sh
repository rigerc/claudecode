#!/bin/bash

# Script to sync .claude/ contents to .opencode/ directories
# Removes existing .opencode directories and copies fresh from .claude/

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if .claude directory exists
if [[ ! -d ".claude" ]]; then
    print_error ".claude directory not found!"
    exit 1
fi

# Create .opencode directory if it doesn't exist
if [[ ! -d ".opencode" ]]; then
    print_status "Creating .opencode directory..."
    mkdir -p .opencode
fi

# Remove existing directories
print_status "Removing existing .opencode directories..."
rm -rf .opencode/command .opencode/agent .opencode/skills

# Copy contents from .claude to .opencode
print_status "Copying commands from .claude/commands to .opencode/command..."
if [[ -d ".claude/commands" ]]; then
    cp -r .claude/commands .opencode/command
    print_status "Commands copied successfully"
else
    print_warning ".claude/commands directory not found, skipping..."
fi

print_status "Copying agents from .claude/agents to .opencode/agent..."
if [[ -d ".claude/agents" ]]; then
    cp -r .claude/agents .opencode/agent
    print_status "Agents copied successfully"
else
    print_warning ".claude/agents directory not found, skipping..."
fi

print_status "Copying skills from .claude/skills to .opencode/skills..."
if [[ -d ".claude/skills" ]]; then
    cp -r .claude/skills .opencode/skills
    print_status "Skills copied successfully"
else
    print_warning ".claude/skills directory not found, skipping..."
fi

# Verify the operation
print_status "Verifying the sync operation..."
echo "Contents of .opencode directory:"
ls -la .opencode/

echo ""
echo "Sync completed successfully!"