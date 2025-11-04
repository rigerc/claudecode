#!/bin/bash

# Sync script to copy .claude/commands and .claude/agents to .opencode directories
# with proper frontmatter processing

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
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if yq is available
check_dependencies() {
    if ! command -v yq &> /dev/null; then
        print_warning "yq not found. Installing yq..."
        # Install yq if not available
        if command -v wget &> /dev/null; then
            wget https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64 -O /tmp/yq
        elif command -v curl &> /dev/null; then
            curl -L https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64 -o /tmp/yq
        else
            print_error "Neither wget nor curl available. Please install yq manually."
            exit 1
        fi
        chmod +x /tmp/yq
        sudo mv /tmp/yq /usr/local/bin/yq
    fi
}

# Process frontmatter: quote all values and escape properly
process_frontmatter() {
    local input_file="$1"
    local output_file="$2"

    # Temporarily disable strict mode for this function
    local old_opts=$(set +o)
    set +e

    # Extract frontmatter (between --- markers)
    local frontmatter_start=$(grep -n "^---$" "$input_file" | head -1 | cut -d: -f1)
    local frontmatter_end=$(grep -n "^---$" "$input_file" | tail -1 | cut -d: -f1)

    if [[ -z "$frontmatter_start" || -z "$frontmatter_end" ]]; then
        print_warning "No frontmatter found in $input_file, copying as-is"
        cp "$input_file" "$output_file"
        return
    fi

    # Extract frontmatter and content
    local frontmatter=$(sed -n "${frontmatter_start},${frontmatter_end}p" "$input_file")
    local content=$(sed -n "$((frontmatter_end + 1)),\$p" "$input_file")

    # Process frontmatter with simple bash-based approach
    local frontmatter_body=$(echo "$frontmatter" | sed '1d;$d')
    local processed_frontmatter_body=""

    # Process each line in frontmatter to quote string values
    local in_array=false
    local array_indent=""

    while IFS= read -r line; do
        if [[ -n "$line" ]]; then
            # Check if this is an array line
            if [[ "$line" =~ ^[[:space:]]*- ]]; then
                in_array=true
                array_indent=$(echo "$line" | sed 's/^\([[:space:]]*\).*/\1/')
                # Process array item
                local item_content=$(echo "$line" | sed 's/^[[:space:]]*- *//')
                if [[ "$item_content" =~ ^[0-9]+$ ]] || [[ "$item_content" == "true" ]] || [[ "$item_content" == "false" ]]; then
                    processed_frontmatter_body+="${line}"$'\n'
                else
                    local escaped_item=$(echo "$item_content" | sed 's/"/\\"/g')
                    processed_frontmatter_body+="${array_indent}- \"${escaped_item}\""$'\n'
                fi
            else
                in_array=false
                # Process regular key-value pair
                if [[ "$line" == *":"* ]]; then
                    local key=$(echo "$line" | cut -d: -f1 | xargs)
                    local value_part=$(echo "$line" | cut -d: -f2- | sed 's/^ *//')

                    # Check if value is already quoted or is a special type
                    if [[ "$value_part" == \"*\" ]] || [[ "$value_part" == "["* ]] || [[ "$value_part" == "true" ]] || [[ "$value_part" == "false" ]] || [[ "$value_part" =~ ^[0-9]+$ ]]; then
                        processed_frontmatter_body+="${line}"$'\n'
                    else
                        # Quote the string value and escape quotes
                        local escaped_value=$(echo "$value_part" | sed 's/"/\\"/g')
                        processed_frontmatter_body+="${key}: \"${escaped_value}\""$'\n'
                    fi
                else
                    processed_frontmatter_body+="${line}"$'\n'
                fi
            fi
        else
            processed_frontmatter_body+=$'\n'
        fi
    done <<< "$frontmatter_body"

    local processed_frontmatter="$processed_frontmatter_body"

    # Reconstruct the file with processed frontmatter
    cat > "$output_file" << EOF
---
$processed_frontmatter
---
$content
EOF

    # Restore original options
    eval "$old_opts"
    return 0
}

# Sync directory
sync_directory() {
    local source_dir="$1"
    local target_dir="$2"

    print_status "Syncing $source_dir to $target_dir..."

    # Remove target directory if it exists
    if [[ -d "$target_dir" ]]; then
        print_status "Removing existing $target_dir"
        rm -rf "$target_dir"
    fi

    # Create target directory
    mkdir -p "$target_dir"

    # Process each markdown file
    local file_count=0
    while IFS= read -r -d '' file; do
        local filename=$(basename "$file")
        local target_file="$target_dir/$filename"

        print_status "Processing $filename"
        if ! process_frontmatter "$file" "$target_file"; then
            print_error "Failed to process $filename, copying as-is"
            cp "$file" "$target_file"
        fi
        ((file_count++))
    done < <(find "$source_dir" -name "*.md" -print0)

    print_status "Processed $file_count files from $source_dir"
}

# Main function
main() {
    print_status "Starting sync from .claude to .opencode..."

    # Check dependencies
    check_dependencies

    # Get script directory
    local script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    local project_root="$script_dir"

    # Define paths
    local claude_commands="$project_root/.claude/commands"
    local claude_agents="$project_root/.claude/agents"
    local opencode_commands="$project_root/.opencode/command"
    local opencode_agents="$project_root/.opencode/agent"

    # Check if source directories exist
    if [[ ! -d "$claude_commands" ]]; then
        print_error "Source directory $claude_commands not found"
        exit 1
    fi

    if [[ ! -d "$claude_agents" ]]; then
        print_error "Source directory $claude_agents not found"
        exit 1
    fi

    # Sync directories
    sync_directory "$claude_commands" "$opencode_commands"
    sync_directory "$claude_agents" "$opencode_agents"

    print_status "Sync completed successfully!"

    # Show summary
    echo
    print_status "Sync Summary:"
    echo "  Commands: $(find "$opencode_commands" -name "*.md" | wc -l) files"
    echo "  Agents: $(find "$opencode_agents" -name "*.md" | wc -l) files"
    echo
}

# Run main function
main "$@"