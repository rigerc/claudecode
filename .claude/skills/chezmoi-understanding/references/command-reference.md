# Chezmoi Command Reference

## Installation Commands

### Install Chezmoi
```bash
# Install using curl (recommended)
curl -sfL https://chezmoi.io/install.sh | sh

# Install using wget
wget -qO- https://chezmoi.io/install.sh | sh

# Custom installation path
PREFIX=/opt/chezmoi DESTDIR=install-root make install
```

### Verify Installation
```bash
chezmoi --version
chezmoi doctor
```

## Core Commands

### Initialization
```bash
# Initialize new Chezmoi setup
chezmoi init

# Initialize from remote repository
chezmoi init https://github.com/username/dotfiles.git
chezmoi init git@github.com:username/dotfiles.git
chezmoi init username  # Short form for GitHub

# Initialize and immediately apply changes
chezmoi init --apply username
chezmoi init --apply --verbose https://github.com/username/dotfiles.git

# One-shot mode (for temporary environments)
chezmoi init --one-shot username
```

### File Management
```bash
# Add files to Chezmoi management
chezmoi add ~/.bashrc                    # Add as regular file
chezmoi add --template ~/.gitconfig      # Add as template
chezmoi add --encrypt ~/.ssh/id_rsa     # Add encrypted file
chezmoi add --recursive ~/.vim           # Add directory
chezmoi add --exact --recursive ~/.oh-my-zsh  # Exact directory management

# Edit managed files
chezmoi edit ~/.bashrc                   # Edit source state
chezmoi edit --apply ~/.bashrc          # Edit and apply immediately
chezmoi edit --watch ~/.bashrc          # Edit with live reload

# Stop managing files
chezmoi forget ~/.bashrc                # Keep file, remove from management
chezmoi remove ~/.oldconfig             # Remove from source and target
chezmoi unmanage ~/.bashrc              # Alias for forget
```

### Status and Comparison
```bash
# Show status of managed files
chezmoi status
chezmoi status --path-style=absolute    # Show absolute paths
chezmoi status --path-style=source-absolute  # Show source paths

# Show differences
chezmoi diff                            # Show all differences
chezmoi diff ~/.bashrc                  # Diff specific file
chezmoi diff --reverse                  # Reverse diff (actual vs target)
chezmoi diff --pager=less               # Use custom pager
chezmoi diff --script-contents=false    # Hide script contents
```

### Apply Changes
```bash
# Apply target state
chezmoi apply                           # Apply all changes
chezmoi apply --dry-run --verbose       # Preview changes
chezmoi apply --exclude=scripts         # Apply excluding scripts
chezmoi apply --include=files           # Apply only files
chezmoi apply ~/.bashrc                 # Apply specific file
```

### Synchronization
```bash
# Update from remote and apply
chezmoi update                          # Pull and apply changes
chezmoi update --exclude=scripts        # Update without running scripts

# Navigate to source directory
chezmoi cd                              # Open shell in source directory
chezmoi source-path                     # Get source directory path
chezmoi source-path ~/.bashrc           # Get source path for specific file
chezmoi target-path dot_bashrc          # Get target path for source file
```

## Template and Data Commands

### Template Operations
```bash
# Display available template data
chezmoi data

# Test template execution
chezmoi execute-template '{{ .chezmoi.hostname }}'
chezmoi execute-template '{{ .chezmoi.os }}/{{ .chezmoi.arch }}'

# Test template from file
chezmoi cd
chezmoi execute-template < dot_bashrc.tmpl

# Execute template with simulated prompts
chezmoi execute-template --init --promptString "email=me@home.org" < .chezmoi.toml.tmpl
```

### State Management
```bash
# Dump target state
chezmoi dump ~/.bashrc                  # Dump specific file
chezmoi dump                            # Dump all target state
chezmoi dump --format=yaml              # YAML format output

# Show managed/unmanaged files
chezmoi managed                         # List managed files
chezmoi unmanaged                       # List unmanaged files in home directory
chezmoi unmanaged ~/.config/chezmoi ~/.ssh  # Check specific directories
```

## Git Integration Commands

### Git Operations
```bash
# Git commands within Chezmoi
chezmoi git add dot_bashrc
chezmoi git commit -- -m "Update bashrc"
chezmoi git push
chezmoi git pull -- --autostash --rebase

# Manual git workflow
chezmoi cd
git status
git add .
git commit -m "Update configuration"
git push
exit
```

### Configuration for Auto-commit
```toml
# ~/.config/chezmoi/chezmoi.toml
[git]
    autoCommit = true
    autoPush = true
    commitMessageTemplate = "{{ promptString \"Commit message\" }}"
```

## Advanced Commands

### Encryption
```bash
# Age encryption setup
age-keygen -o ~/.config/chezmoi/key.txt

# GPG encryption setup
# Configure recipient in chezmoi.toml
```

### External Resources
```bash
# Create archive of dotfiles
chezmoi archive --output=dotfiles.tar.gz
chezmoi archive --output=dotfiles.zip --format=zip

# Import external archives
curl -s -L -o ${TMPDIR}/oh-my-zsh-master.tar.gz https://github.com/ohmyzsh/ohmyzsh/archive/master.tar.gz
mkdir -p $(chezmoi source-path)/dot_oh-my-zsh
chezmoi import --strip-components 1 --destination ~/.oh-my-zsh ${TMPDIR}/oh-my-zsh-master.tar.gz
```

### Merge and Resolution
```bash
# Resolve conflicts
chezmoi merge ~/.bashrc                # Open merge tool
chezmoi apply --force                  # Accept target state
chezmoi re-add ~/.bashrc               # Update source with local changes
```

### Verification and Cleanup
```bash
# Verify system state
chezmoi verify                         # Check if system matches target

# System health check
chezmoi doctor                         # Check for common problems

# Cleanup operations
chezmoi purge                          # Remove all managed files and chezmoi
chezmoi destroy                        # Purge + remove source directory
```

## Configuration File Formats

### TOML Configuration
```toml
# ~/.config/chezmoi/chezmoi.toml
sourceDir = "~/.dotfiles"

[git]
    autoCommit = true
    autoPush = true

[data]
    email = "user@example.com"
    name = "John Doe"

encryption = "age"
[age]
    identity = "~/.config/chezmoi/key.txt"
    recipient = "age1ql3z7hjy54pw3hyww5ayyfg7zqgvc7w3j2elw8zmrj2kg5sfn9aqmcac8p"

[diff]
    command = "vimdiff"
    pager = "less -R"

[edit]
    apply = true
    watch = true
```

### YAML Configuration
```yaml
# ~/.config/chezmoi/chezmoi.yaml
sourceDir: ~/.dotfiles

git:
  autoCommit: true
  autoPush: true

data:
  email: user@example.com
  name: John Doe

encryption: age
age:
  identity: ~/.config/chezmoi/key.txt
  recipient: age1ql3z7hjy54pw3hyww5ayyfg7zqgvc7w3j2elw8zmrj2kg5sfn9aqmcac8p
```

## File Attributes Reference

### Basic Attributes
- `dot_` - Regular dotfile (e.g., `dot_bashrc` → `~/.bashrc`)
- `.tmpl` - Template file (processed with Go templates)
- `executable_` - Make file executable
- `private_` - Remove group/world permissions (600)
- `encrypted_` - Encrypt file (with age or GPG)
- `empty_` - Preserve empty files
- `create_` - Create only if doesn't exist
- `modify_` - Transform existing file
- `remove_` - Remove target file
- `symlink_` - Create symbolic link

### Script Attributes
- `run_` - Execute script on every apply
- `run_once_` - Execute only once (tracked by content hash)
- `run_onchange_` - Execute when script content changes
- `run_before_` - Execute before any file updates
- `run_after_` - Execute after all files are applied

### Directory Attributes
- `exact_` - Exact directory (removes unmanaged files)
- Combined with `recursive_` for directory management

## Common Flag Options

### Global Flags
- `--config` - Specify config file location
- `--source` - Specify source directory
- `--destination` - Specify destination directory
- `--verbose` - Verbose output
- `--dry-run` - Show what would be done without doing it

### Add Command Flags
- `--template` - Add file as template
- `--encrypt` - Add encrypted file
- `--recursive` - Add directory recursively
- `--exact` - Add directory as exact (remove unmanaged files)
- `--autotemplate` - Auto-detect template variables
- `--prompt` - Prompt before each file

### Init Command Flags
- `--apply` - Apply changes after initialization
- `--one-shot` - Temporary environment mode
- `--branch` - Checkout specific branch
- `--depth` - Clone with specified depth
- `--purge` - Remove source and config after applying

### Diff Command Flags
- `--reverse` - Show reverse diff
- `--pager` - Use specified pager
- `--script-contents` - Show/hide script contents

## Environment Variables

```bash
# Configuration
CHEZMOI_CONFIG_DIR          # Config directory location
CHEZMOI_SOURCE_DIR          # Source directory location
CHEZMOI_DESTINATION_DIR     # Destination directory location

# Git integration
CHEZMOI_GITHUB_USERNAME     # GitHub username for short repo names
CHEZMOI_GITLAB_USERNAME     # GitLab username
CHEZMOI_CODEBERG_USERNAME   # Codeberg username

# Behavior
CHEZMOI_VERBOSE             # Enable verbose output
CHEZMOI_DEBUG               # Enable debug output
```