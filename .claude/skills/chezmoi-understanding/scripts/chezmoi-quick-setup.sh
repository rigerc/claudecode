#!/bin/bash
# Chezmoi Quick Setup Script
# Automated installation and initialization of Chezmoi dotfile management

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
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

# Function to detect operating system
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "darwin"
    elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        echo "windows"
    else
        echo "unknown"
    fi
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install chezmoi
install_chezmoi() {
    local os=$(detect_os)
    print_info "Detected OS: $os"

    if command_exists chezmoi; then
        print_success "Chezmoi is already installed: $(chezmoi --version)"
        return 0
    fi

    print_info "Installing Chezmoi..."

    case $os in
        "linux")
            if command_exists curl; then
                print_info "Installing via curl..."
                curl -sfL https://chezmoi.io/install.sh | sh
            elif command_exists wget; then
                print_info "Installing via wget..."
                wget -qO- https://chezmoi.io/install.sh | sh
            else
                print_error "Neither curl nor wget found. Please install one of them and try again."
                exit 1
            fi
            ;;
        "darwin")
            if command_exists brew; then
                print_info "Installing via Homebrew..."
                brew install chezmoi
            else
                print_info "Installing via curl..."
                curl -sfL https://chezmoi.io/install.sh | sh
            fi
            ;;
        "windows")
            print_error "Windows installation not supported by this script. Please visit https://chezmoi.io/get for Windows installation instructions."
            exit 1
            ;;
        *)
            print_error "Unsupported operating system: $os"
            exit 1
            ;;
    esac

    # Verify installation
    if command_exists chezmoi; then
        print_success "Chezmoi installed successfully: $(chezmoi --version)"
    else
        print_error "Chezmoi installation failed"
        exit 1
    fi
}

# Function to get GitHub username
get_github_username() {
    local username=""

    # Try to get from git config
    if command_exists git; then
        username=$(git config --global user.name 2>/dev/null || echo "")
    fi

    # Try to get from environment
    if [[ -z "$username" ]]; then
        username=${GITHUB_USERNAME:-}
    fi

    # Prompt user if still empty
    if [[ -z "$username" ]]; then
        echo -n "Enter your GitHub username: "
        read -r username
    fi

    while [[ -z "$username" ]]; do
        print_error "GitHub username is required"
        echo -n "Enter your GitHub username: "
        read -r username
    done

    echo "$username"
}

# Function to initialize chezmoi
initialize_chezmoi() {
    local username=$1
    local repo_url="https://github.com/${username}/dotfiles.git"

    print_info "Initializing Chezmoi with repository: $repo_url"

    # Check if repository exists
    if command_exists curl; then
        if curl -s -o /dev/null -w "%{http_code}" "$repo_url" | grep -q "200\|301\|302"; then
            print_info "Repository found. Initializing..."

            # Initialize and apply
            if chezmoi init --apply "$username"; then
                print_success "Chezmoi initialized and dotfiles applied successfully"
            else
                print_warning "Repository found but initialization failed. Trying basic initialization..."
                chezmoi init "$username"
                print_info "Please run 'chezmoi apply' to apply your dotfiles"
            fi
        else
            print_warning "Repository $repo_url not found or not accessible"

            # Try SSH
            local ssh_repo="git@github.com:${username}/dotfiles.git"
            if command_exists ssh; then
                print_info "Trying SSH repository: $ssh_repo"
                if ssh -o BatchMode=yes -o ConnectTimeout=5 git@github.com 2>/dev/null; then
                    print_info "SSH access available. Initializing with SSH..."
                    chezmoi init "$ssh_repo"
                    print_info "Please run 'chezmoi apply' to apply your dotfiles"
                else
                    print_info "SSH access not available. Initializing empty configuration..."
                    chezmoi init
                    print_info "Empty Chezmoi configuration created. You can add files later with 'chezmoi add'"
                fi
            else
                print_info "SSH not available. Initializing empty configuration..."
                chezmoi init
                print_info "Empty Chezmoi configuration created. You can add files later with 'chezmoi add'"
            fi
        fi
    else
        print_warning "curl not available, cannot check repository. Initializing empty configuration..."
        chezmoi init
        print_info "Empty Chezmoi configuration created. You can add files later with 'chezmoi add'"
    fi
}

# Function to setup basic configuration
setup_basic_config() {
    print_info "Setting up basic configuration..."

    # Create config directory if it doesn't exist
    mkdir -p ~/.config/chezmoi

    # Create basic config file if it doesn't exist
    local config_file="$HOME/.config/chezmoi/chezmoi.toml"
    if [[ ! -f "$config_file" ]]; then
        cat > "$config_file" << EOF
# Chezmoi configuration file
# Generated by chezmoi-quick-setup.sh

[data]
    # Add your personal data here
    # email = "your-email@example.com"
    # name = "Your Name"

[git]
    # Enable auto-commit and push
    autoCommit = false  # Set to true to enable
    autoPush = false    # Set to true to enable

[diff]
    # Use your preferred diff tool
    # command = "vimdiff"
    pager = "less -R"

[edit]
    # Apply changes immediately after editing
    apply = false
    # Watch for changes and auto-apply
    watch = false
EOF
        print_success "Basic configuration file created at $config_file"
        print_info "Edit this file to customize your Chezmoi configuration"
    else
        print_info "Configuration file already exists at $config_file"
    fi
}

# Function to provide next steps
show_next_steps() {
    cat << EOF

${GREEN}=== Chezmoi Setup Complete ===${NC}

${BLUE}Next Steps:${NC}
1. Add your existing dotfiles to Chezmoi:
   chezmoi add ~/.bashrc
   chezmoi add ~/.vimrc
   chezmoi add ~/.gitconfig

2. Edit managed files:
   chezmoi edit ~/.bashrc

3. Apply changes:
   chezmoi apply

4. Check status:
   chezmoi status

5. View differences:
   chezmoi diff

6. Push to remote repository:
   chezmoi cd
   git remote add origin https://github.com/YOUR_USERNAME/dotfiles.git
   git push -u origin main
   exit

${BLUE}Useful Commands:${NC}
- chezmoi help          Show help
- chezmoi doctor        Check system health
- chezmoi data          Show template variables
- chezmoi managed       List managed files
- chezmoi unmanaged     List unmanaged files

${BLUE}Documentation:${NC}
- https://chezmoi.io    Official documentation
- man chezmoi          Manual page

${YELLOW}Note:${NC} Edit ~/.config/chezmoi/chezmoi.toml to customize your configuration.

EOF
}

# Function to validate setup
validate_setup() {
    print_info "Validating Chezmoi setup..."

    # Check if chezmoi is installed
    if command_exists chezmoi; then
        print_success "✓ Chezmoi is installed: $(chezmoi --version)"
    else
        print_error "✗ Chezmoi is not installed"
        return 1
    fi

    # Check if source directory exists
    if [[ -d "$HOME/.local/share/chezmoi" ]]; then
        print_success "✓ Chezmoi source directory exists"
    else
        print_warning "✗ Chezmoi source directory not found"
    fi

    # Check if config directory exists
    if [[ -d "$HOME/.config/chezmoi" ]]; then
        print_success "✓ Chezmoi config directory exists"
    else
        print_warning "✗ Chezmoi config directory not found"
    fi

    # Run doctor command
    if chezmoi doctor >/dev/null 2>&1; then
        print_success "✓ Chezmoi doctor check passed"
    else
        print_warning "✗ Chezmoi doctor check found issues. Run 'chezmoi doctor' for details"
    fi
}

# Main function
main() {
    echo "${BLUE}=== Chezmoi Quick Setup Script ===${NC}"
    echo

    # Parse command line arguments
    local github_username=""
    local skip_install=false
    local apply_immediately=false

    while [[ $# -gt 0 ]]; do
        case $1 in
            -u|--username)
                github_username="$2"
                shift 2
                ;;
            -s|--skip-install)
                skip_install=true
                shift
                ;;
            -a|--apply)
                apply_immediately=true
                shift
                ;;
            -h|--help)
                cat << EOF
Usage: $0 [OPTIONS]

OPTIONS:
    -u, --username USERNAME     GitHub username (optional, will prompt if not provided)
    -s, --skip-install          Skip chezmoi installation
    -a, --apply                Apply dotfiles immediately after initialization
    -h, --help                 Show this help message

EXAMPLES:
    $0                         # Interactive setup
    $0 -u myusername          # Setup with specific GitHub username
    $0 -s -u myusername       # Skip installation, just initialize
    $0 -a -u myusername       # Apply dotfiles immediately

EOF
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                exit 1
                ;;
        esac
    done

    # Install chezmoi if needed
    if [[ "$skip_install" == false ]]; then
        install_chezmoi
    else
        if ! command_exists chezmoi; then
            print_error "Chezmoi is not installed but --skip-install was specified"
            exit 1
        fi
        print_info "Skipping chezmoi installation as requested"
    fi

    # Get GitHub username if not provided
    if [[ -z "$github_username" ]]; then
        github_username=$(get_github_username)
    fi

    # Initialize chezmoi
    initialize_chezmoi "$github_username"

    # Setup basic configuration
    setup_basic_config

    # Validate setup
    validate_setup

    # Show next steps
    show_next_steps
}

# Run main function
main "$@"