#!/bin/bash
# Chezmoi Migration Helper
# Script to help migrate existing dotfiles to Chezmoi management

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
BACKUP_DIR="$HOME/.chezmoi-migration-backup-$(date +%Y%m%d_%H%M%S)"
COMMON_DOTFILES=(
    ".bashrc"
    ".bash_profile"
    ".zshrc"
    ".vimrc"
    ".gitconfig"
    ".tmux.conf"
    ".config/nvim/init.vim"
    ".config/fish/config.fish"
    ".ssh/config"
    ".inputrc"
    ".profile"
    ".xprofile"
    ".Xresources"
    ".gtkrc-2.0"
)

# Functions
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_question() {
    echo -e "${BLUE}[QUESTION]${NC} $1"
}

# Function to check if chezmoi is installed
check_chezmoi() {
    if ! command -v chezmoi &> /dev/null; then
        print_error "Chezmoi is not installed. Please install it first:"
        echo "curl -sfL https://chezmoi.io/install.sh | sh"
        exit 1
    fi
    print_success "Chezmoi found: $(chezmoi --version)"
}

# Function to check if chezmoi is initialized
check_chezmoi_init() {
    if [[ ! -d "$HOME/.local/share/chezmoi" ]]; then
        print_warning "Chezmoi is not initialized"
        print_question "Would you like to initialize chezmoi now? (y/N): "
        read -r response
        if [[ "$response" =~ ^[Yy]$ ]]; then
            print_info "Initializing chezmoi..."
            chezmoi init
            print_success "Chezmoi initialized"
        else
            print_error "Chezmoi must be initialized before migrating dotfiles"
            exit 1
        fi
    else
        print_success "Chezmoi is already initialized"
    fi
}

# Function to create backup
create_backup() {
    print_info "Creating backup directory: $BACKUP_DIR"
    mkdir -p "$BACKUP_DIR"
}

# Function to backup a file
backup_file() {
    local file="$1"
    local backup_path="$BACKUP_DIR/$(dirname "$file")"

    if [[ -f "$HOME/$file" ]]; then
        mkdir -p "$backup_path"
        cp "$HOME/$file" "$backup_path/"
        print_info "Backed up: $file"
    fi
}

# Function to restore from backup
restore_backup() {
    print_info "Restoring files from backup..."

    if [[ -d "$BACKUP_DIR" ]]; then
        # Use rsync to preserve permissions and timestamps
        rsync -av "$BACKUP_DIR/" "$HOME/"
        print_success "Files restored from backup"

        # Ask if user wants to remove backup
        print_question "Remove backup directory? (y/N): "
        read -r response
        if [[ "$response" =~ ^[Yy]$ ]]; then
            rm -rf "$BACKUP_DIR"
            print_info "Backup directory removed"
        fi
    else
        print_warning "Backup directory not found"
    fi
}

# Function to add file to chezmoi
add_to_chezmoi() {
    local file="$1"
    local options="$2"

    if [[ -f "$HOME/$file" ]]; then
        print_info "Adding $file to chezmoi..."
        chezmoi add $options "$HOME/$file"
        print_success "Added: $file"
    else
        print_warning "File not found: $file"
    fi
}

# Function to detect file type and suggest attributes
suggest_attributes() {
    local file="$1"
    local attrs=""

    # Check if file is executable
    if [[ -x "$HOME/$file" ]]; then
        attrs="$attrs --executable"
    fi

    # Check if file contains sensitive information
    if [[ "$file" == *"ssh"* ]] || [[ "$file" == *"key"* ]] || [[ "$file" == *"password"* ]]; then
        print_question "File '$file' may contain sensitive information. Encrypt it? (y/N): "
        read -r response
        if [[ "$response" =~ ^[Yy]$ ]]; then
            attrs="$attrs --encrypt"
        fi
    fi

    # Check if file should be a template (contains placeholders or variables)
    if grep -q "{{" "$HOME/$file" 2>/dev/null || grep -q "EMAIL" "$HOME/$file" 2>/dev/null || grep -q "USER" "$HOME/$file" 2>/dev/null; then
        print_question "File '$file' appears to contain template variables. Treat as template? (y/N): "
        read -r response
        if [[ "$response" =~ ^[Yy]$ ]]; then
            attrs="$attrs --template"
        fi
    fi

    echo "$attrs"
}

# Function to migrate common dotfiles
migrate_common_dotfiles() {
    print_info "Migrating common dotfiles..."

    for file in "${COMMON_DOTFILES[@]}"; do
        if [[ -f "$HOME/$file" ]]; then
            backup_file "$file"
            attrs=$(suggest_attributes "$file")
            add_to_chezmoi "$file" "$attrs"
        fi
    done
}

# Function to find and migrate all dotfiles
find_all_dotfiles() {
    print_info "Finding all dotfiles in home directory..."

    # Find all dotfiles excluding common directories to skip
    local exclude_dirs=(
        ".cache"
        ".local/share/Trash"
        ".local/share/chezmoi"
        ".config/Code/User/workspaceStorage"
        ".config/google-chrome"
        ".config/mozilla"
        ".config/discord"
        "node_modules"
        ".git"
        ".svn"
        ".hg"
    )

    # Build exclude pattern for find
    local exclude_args=()
    for dir in "${exclude_dirs[@]}"; do
        exclude_args+=(-path "$HOME/$dir" -prune -o)
    done

    # Find all dotfiles
    local dotfiles=()
    while IFS= read -r -d '' file; do
        dotfiles+=("$file")
    done < <(find "$HOME" -maxdepth 3 -name ".*" -type f "${exclude_args[@]}" -print0 2>/dev/null | sort -z)

    echo "${dotfiles[@]}"
}

# Function to migrate all dotfiles interactively
migrate_all_dotfiles() {
    local dotfiles=($(find_all_dotfiles))

    if [[ ${#dotfiles[@]} -eq 0 ]]; then
        print_warning "No dotfiles found"
        return
    fi

    print_info "Found ${#dotfiles[@]} dotfiles"

    for file in "${dotfiles[@]}"; do
        local relative_path="${file#$HOME/}"

        # Skip if already managed by chezmoi
        if chezmoi managed | grep -q "^$HOME/$relative_path$"; then
            print_info "Already managed: $relative_path"
            continue
        fi

        # Skip files in backup directory
        if [[ "$relative_path" == .chezmoi-migration-backup* ]]; then
            continue
        fi

        print_question "Add '$relative_path' to chezmoi? (y/N/a/q): "
        read -r response

        case "$response" in
            [Yy]*)
                backup_file "$relative_path"
                attrs=$(suggest_attributes "$relative_path")
                add_to_chezmoi "$relative_path" "$attrs"
                ;;
            [Aa]*)
                print_info "Adding all remaining files..."
                backup_file "$relative_path"
                attrs=$(suggest_attributes "$relative_path")
                add_to_chezmoi "$relative_path" "$attrs"

                # Add remaining files without asking
                for remaining_file in "${dotfiles[@]}"; do
                    local remaining_relative="${remaining_file#$HOME/}"

                    # Skip if already processed or managed
                    if [[ "$remaining_relative" == "$relative_path" ]] || chezmoi managed | grep -q "^$HOME/$remaining_relative$"; then
                        continue
                    fi

                    if [[ "$remaining_relative" != .chezmoi-migration-backup* ]]; then
                        backup_file "$remaining_relative"
                        remaining_attrs=$(suggest_attributes "$remaining_relative")
                        add_to_chezmoi "$remaining_relative" "$remaining_attrs"
                    fi
                done
                break
                ;;
            [Qq]*)
                print_info "Quitting migration"
                break
                ;;
            *)
                print_info "Skipping: $relative_path"
                ;;
        esac
    done
}

# Function to create basic template data
create_template_data() {
    local data_file="$HOME/.local/share/chezmoi/.chezmoidata.yaml"

    if [[ -f "$data_file" ]]; then
        print_info "Data file already exists: $data_file"
        return
    fi

    print_info "Creating basic template data file..."

    # Get user information
    echo "Please provide some information for template variables:"

    echo -n "Email address: "
    read -r email

    echo -n "Full name: "
    read -r name

    echo -n "GitHub username: "
    read -r github_username

    # Create data file
    cat > "$data_file" << EOF
# Chezmoi template data
# This file contains variables used in templates

email: "$email"
name: "$name"
github_username: "$github_username"

# Add your custom variables here
# work_email: "work@example.com"
# editor: "vim"
# dark_theme: true
EOF

    print_success "Template data file created: $data_file"
}

# Function to suggest next steps
show_next_steps() {
    cat << EOF

${GREEN}=== Migration Complete ===${NC}

${BLUE}Next Steps:${NC}
1. Review the changes:
   chezmoi diff

2. Apply the changes:
   chezmoi apply

3. Check status:
   chezmoi status

4. Edit files if needed:
   chezmoi edit ~/.bashrc

5. Initialize git repository (if not already done):
   chezmoi cd
   git init
   git remote add origin https://github.com/YOUR_USERNAME/dotfiles.git
   git add .
   git commit -m "Initial commit"
   git push -u origin main
   exit

${BLUE}Template Variables:${NC}
- Edit template data: ~/.local/share/chezmoi/.chezmoidata.yaml
- Test templates: chezmoi execute-template '{{ .email }}'

${BLUE}Backup:${NC}
- Backup location: $BACKUP_DIR
- Restore if needed: Run this script with --restore

${BLUE}Useful Commands:${NC}
- chezmoi managed       List managed files
- chezmoi unmanaged     List unmanaged files
- chezmoi doctor        Check system health

EOF
}

# Function to show menu
show_menu() {
    echo
    echo "Chezmoi Migration Helper"
    echo "========================"
    echo "1. Migrate common dotfiles (.bashrc, .vimrc, etc.)"
    echo "2. Migrate all dotfiles interactively"
    echo "3. Create template data file"
    echo "4. Restore from backup"
    echo "5. Exit"
    echo
    echo -n "Choose an option: "
}

# Main function
main() {
    # Parse command line arguments
    case "${1:-}" in
        --restore)
            restore_backup
            exit 0
            ;;
        --help|-h)
            cat << EOF
Chezmoi Migration Helper

USAGE:
    $0                  # Interactive menu
    $0 --restore        # Restore from backup
    $0 --help           # Show this help

This script helps migrate existing dotfiles to Chezmoi management.
EOF
            exit 0
            ;;
    esac

    # Check prerequisites
    check_chezmoi
    check_chezmoi_init

    # Create backup
    create_backup

    # Show menu
    while true; do
        show_menu
        read -r choice

        case $choice in
            1)
                migrate_common_dotfiles
                ;;
            2)
                migrate_all_dotfiles
                ;;
            3)
                create_template_data
                ;;
            4)
                restore_backup
                ;;
            5)
                print_info "Exiting"
                break
                ;;
            *)
                print_error "Invalid option: $choice"
                ;;
        esac
    done

    # Show next steps
    show_next_steps
}

# Trap to handle interruption
trap 'print_warning "Migration interrupted. Backup files are preserved in $BACKUP_DIR"; exit 1' INT

# Run main function
main "$@"