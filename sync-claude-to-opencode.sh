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

# Function to clean frontmatter, keeping only 'description'
clean_frontmatter() {
    local file="$1"
    
    # Check if file has frontmatter (starts with ---)
    if [[ "$(head -n1 "$file")" != "---" ]]; then
        return 0  # No frontmatter, skip
    fi
    
    # Create temporary file
    local temp_file=$(mktemp)
    
    # Process the file:
    # 1. Find the end of frontmatter (second ---)
    # 2. Extract only the description line from frontmatter
    # 3. Encapsulate description in double quotes
    # 4. Keep the rest of the file content
    awk '
    BEGIN { in_frontmatter = 0; frontmatter_ended = 0; description_found = 0 }
    NR == 1 && $0 == "---" { in_frontmatter = 1; next }
    in_frontmatter && $0 == "---" { 
        in_frontmatter = 0; 
        frontmatter_ended = 1;
        if (description_found) {
            print "---";
            print "description: \"" description "\"";
            print "---";
        }
        next 
    }
    in_frontmatter && /^description:/ { 
        description = $0; 
        sub(/^description:\s*/, "", description);
        # Remove existing quotes if present
        gsub(/^"|"$/, "", description);
        description_found = 1;
        next 
    }
    in_frontmatter { next }  # Skip other frontmatter
    { print }  # Print rest of content
    ' "$file" > "$temp_file"
    
    # Replace original file with cleaned version
    mv "$temp_file" "$file"
}

# Clean frontmatter from copied files
print_status "Cleaning frontmatter from copied files..."

# Clean command files
if [[ -d ".opencode/command" ]]; then
    find .opencode/command -name "*.md" -type f | while read -r file; do
        print_status "Cleaning frontmatter from: $file"
        clean_frontmatter "$file"
    done
fi

# Clean agent files
if [[ -d ".opencode/agent" ]]; then
    find .opencode/agent -name "*.md" -type f | while read -r file; do
        print_status "Cleaning frontmatter from: $file"
        clean_frontmatter "$file"
    done
fi

# Clean skill files (if they contain markdown files)
if [[ -d ".opencode/skills" ]]; then
    find .opencode/skills -name "*.md" -type f | while read -r file; do
        print_status "Cleaning frontmatter from: $file"
        clean_frontmatter "$file"
    done
fi

# Verify the operation
print_status "Verifying the sync operation..."
echo "Contents of .opencode directory:"
ls -la .opencode/

echo ""
echo "Sync completed successfully!"