# Chezmoi File Attributes Reference

## File Naming Conventions

Chezmoi uses special prefixes and suffixes in the source directory to control file behavior when applied to the target directory. The source directory is typically `~/.local/share/chezmoi`.

## Basic File Types

### Regular Files
```bash
# Source file: dot_bashrc
# Target: ~/.bashrc
# Description: Regular file copied as-is

dot_zshrc
dot_vimrc
dot_config/nvim/init.vim
```

### Template Files
```bash
# Source file: dot_gitconfig.tmpl
# Target: ~/.gitconfig
# Description: File processed as Go template before copying

dot_gitconfig.tmpl
dot_bashrc.tmpl
dot_config/fish/config.fish.tmpl
```

### Executable Files
```bash
# Source file: executable_dot_local/bin/script
# Target: ~/.local/bin/script
# Description: File with executable permissions (755)

executable_dot_local/bin/script
executable_dot_bin/myapp
```

### Private Files
```bash
# Source file: private_dot_ssh/config
# Target: ~/.ssh/config
# Description: File with restricted permissions (600)

private_dot_ssh/config
private_dot_gnupg/gpg.conf
```

### Encrypted Files
```bash
# Source file: encrypted_private_dot_ssh/encrypted_private_id_rsa.age
# Target: ~/.ssh/id_rsa
# Description: File encrypted with age or GPG

encrypted_private_dot_ssh/encrypted_private_id_rsa.age
encrypted_dot_config/encrypted_secrets.json.age
```

## Directory Management

### Regular Directories
```bash
# Source: dot_config/nvim/
# Target: ~/.config/nvim/
# Description: Directory copied recursively

dot_config/nvim/init.vim
dot_config/nvim/plugins/
```

### Exact Directories
```bash
# Source: exact_dot_config/exact_nvim/
# Target: ~/.config/nvim/
# Description: Directory managed exactly (removes unmanaged files)

exact_dot_config/exact_nvim/init.vim
exact_dot_config/exact_nvim/plugins/
```

### Empty Files
```bash
# Source: empty_dot_keep
# Target: ~/.keep
# Description: Empty file preserved even if empty

empty_dot_local/share/app/keep
empty_dot_config/app/.keep
```

## Script Types

### Run Scripts
```bash
# Source: run_after_setup.sh
# Target: No target file (executed during apply)
# Description: Script executed every time chezmoi apply runs

run_after_setup.sh
run_before_backup.sh
run_update.sh
```

### Run Once Scripts
```bash
# Source: run_once_install-packages.sh
# Target: No target file (executed once)
# Description: Script executed only once, tracked by content hash

run_once_install-dev-tools.sh
run_once_setup-vim.sh
run_once_configure-git.sh
```

### Run On Change Scripts
```bash
# Source: run_onchange_install-vim-plugins.sh
# Target: No target file (executed when content changes)
# Description: Script re-executed when script content changes

run_onchange_update-config.sh
run_onchange-rebuild-database.sh
```

### Template Scripts
```bash
# Source: run_once_install-packages.sh.tmpl
# Target: No target file (template script)
# Description: Template script executed once

run_once_install-packages.sh.tmpl
run_onchange_configure-app.sh.tmpl
```

## Special File Types

### Create Files
```bash
# Source: create_dot_local/share/database.db
# Target: ~/.local/share/database.db
# Description: File created only if doesn't exist, never updated

create_dot_local/share/database.db
create_dot_config/app/settings.json
```

### Modify Files
```bash
# Source: modify_dot_ssh/config.tmpl
# Target: ~/.ssh/config
# Description: Script that transforms existing file content

modify_dot_ssh/config.tmpl
modify_dot_config/app/settings.tmpl
```

### Remove Files
```bash
# Source: remove_dot_oldconfig
# Target: ~/.oldconfig
# Description: Target file removed if it exists

remove_dot_config/old-app/config
remove_dot_local/share/old-data/
```

### Symlink Files
```bash
# Source: symlink_dot_vim.tmpl
# Content: {{ .chezmoi.homeDir }}/dotfiles/vim
# Target: ~/.vim -> ~/dotfiles/vim
# Description: Symbolic link to specified target

symlink_dot_config/nvim.tmpl
symlink_dot_local/bin/tool.tmpl
```

## Attribute Combinations

### Multiple Attributes
```bash
# Encrypted, private, template file
encrypted_private_dot_config/encrypted_private_secrets.tmpl.age

# Executable template script
executable_run_once_install-packages.sh.tmpl

# Private template config
private_dot_ssh/config.tmpl
```

### Directory Attributes
```bash
# Exact recursive directory with templates
exact_dot_config/exact_nvim/init.vim.tmpl
exact_dot_config/exact_nvim/plugins/

# Regular directory with mixed file types
dot_config/app/config.json.tmpl
dot_config/app/scripts/executable_run_setup.sh
dot_config/app/data/encrypted_private_secrets.age
```

## File Path Translation

### Source to Target Mapping
```bash
# Source: dot_bashrc
# Target: ~/.bashrc

# Source: dot_config/nvim/init.vim
# Target: ~/.config/nvim/init.vim

# Source: executable_dot_local/bin/script
# Target: ~/.local/bin/script

# Source: private_dot_ssh/id_rsa
# Target: ~/.ssh/id_rsa
```

### Path Patterns
```bash
# Dotfiles: dot_* → ~/.*
dot_bashrc → ~/.bashrc
dot_gitconfig → ~/.gitconfig

# Config directories: dot_config/* → ~/.config/*
dot_config/nvim/init.vim → ~/.config/nvim/init.vim
dot_config/fish/config.fish → ~/.config/fish/config.fish

# Local directories: dot_local/* → ~/.local/*
dot_local/bin/script → ~/.local/bin/script
dot_local/share/app → ~/.local/share/app
```

## Permission Management

### File Permissions
```bash
# Regular files: 644 (rw-r--r--)
dot_bashrc → ~/.bashrc (644)

# Executable files: 755 (rwxr-xr-x)
executable_dot_local/bin/script → ~/.local/bin/script (755)

# Private files: 600 (rw-------)
private_dot_ssh/config → ~/.ssh/config (600)

# Encrypted private files: 600
encrypted_private_dot_ssh/id_rsa.age → ~/.ssh/id_rsa (600)
```

### Directory Permissions
```bash
# Regular directories: 755 (rwxr-xr-x)
dot_config/ → ~/.config/ (755)

# Private directories: 700 (rwx------)
private_dot_ssh/ → ~/.ssh/ (700)
```

## Configuration Examples

### SSH Configuration
```bash
# SSH config (template, private)
private_dot_ssh/config.tmpl

# SSH private key (encrypted, private)
encrypted_private_dot_ssh/encrypted_private_id_rsa.age

# SSH public key (regular)
dot_ssh/id_rsa.pub

# SSH known hosts (regular)
dot_ssh/known_hosts
```

### Development Environment
```bash
# Git configuration (template)
dot_gitconfig.tmpl

# Vim configuration (template)
dot_vimrc.tmpl

# Vim plugins directory (exact)
exact_dot_config/exact_nvim/

# Development scripts (executable, template)
executable_dot_local/bin/setup-dev.sh.tmpl
executable_dot_local/bin/update-tools.sh.tmpl
```

### Application Setup
```bash
# Application config (template)
dot_config/app/config.json.tmpl

# Application data (create)
create_dot_local/share/app/database.db

# Application secrets (encrypted)
encrypted_dot_config/app/encrypted_secrets.age

# Setup script (run once)
run_once_install-app.sh.tmpl

# Update script (run on change)
run_onchange_update-app.sh.tmpl
```

## Advanced Patterns

### Conditional File Management
```bash
# Template that creates file only on certain systems
{{ if eq .chezmoi.os "linux" }}
# dot_linux-only-config would be included only on Linux
{{ end }}
```

### Shared Templates
```bash
# Create reusable template in .chezmoitemplates/
.chezmoitemplates/ssh-config
.chezmoitemplates/git-config

# Use in multiple files
{{ template "ssh-config" . }}
```

### External Files
```bash
# Reference external file in template
{{ include "external-config.txt" }}

# Read external file content
{{ .chezmoi.sourceDir }}/external-file.txt
```

## File Operations

### Adding Files with Attributes
```bash
# Add regular file
chezmoi add ~/.bashrc

# Add as template
chezmoi add --template ~/.gitconfig

# Add as executable
chezmoi add --executable ~/bin/script

# Add as private file
chezmoi add --private ~/.ssh/config

# Add encrypted file
chezmoi add --encrypt ~/.ssh/id_rsa

# Add exact directory
chezmoi add --exact --recursive ~/.config/nvim
```

### Changing Attributes
```bash
# Convert regular file to template
chezmoi chattr +template ~/.bashrc

# Remove template attribute
chezmoi chattr -template ~/.bashrc

# Add executable attribute
chezmoi chattr +executable ~/bin/script

# Remove executable attribute
chezmoi chattr -executable ~/bin/script
```

### File Status
```bash
# Show file status with attributes
chezmoi status --path-style=source-absolute

# Show target file paths
chezmoi status --path-style=absolute
```

## Best Practices

### File Organization
```bash
# Group related files
dot_config/app/
dot_config/app/config.json.tmpl
dot_config/app/scripts/run_setup.sh
dot_config/app/data/secrets.age

# Use descriptive names
dot_gitconfig_personal.tmpl
dot_gitconfig_work.tmpl
run_once_install-dev-tools.sh
```

### Security
```bash
# Encrypt sensitive files
encrypted_private_dot_ssh/id_rsa.age
encrypted_dot_config/api-keys.age

# Use private attribute for sensitive configs
private_dot_ssh/config
private_dot_gnupg/gpg.conf
```

### Template Management
```bash
# Use templates for platform-specific content
dot_bashrc.tmpl  # Contains OS-specific logic

# Use data files for variables
.chezmoidata.yaml  # Contains email, name, etc.

# Use shared templates for common patterns
.chezmoitemplates/ssh-config
.chezmoitemplates/git-config
```

## Troubleshooting

### Common Issues
```bash
# File not applying - check attribute syntax
chezmoi status

# Template errors - test template
chezmoi execute-template < template.tmpl

# Permission issues - check attributes
chezmoi dump target-file

# Encryption issues - check encryption setup
chezmoi doctor
```

### Debug File Types
```bash
# Show source file type
chezmoi source-path ~/.bashrc

# Show target path for source
chezmoi target-path dot_bashrc

# Dump target state
chezmoi dump ~/.bashrc
```