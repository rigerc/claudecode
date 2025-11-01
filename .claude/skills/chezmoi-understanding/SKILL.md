---
name: chezmoi-cli-guide
description: This skill provides comprehensive guidance for the Chezmoi dotfile management system. It should be used when users need help with Chezmoi CLI operations, template creation, configuration management, troubleshooting, or understanding Chezmoi's workflow and features. The skill covers setup, daily operations, advanced features like encryption and password manager integration, and complex template scenarios for managing dotfiles across multiple machines.
---

# Chezmoi CLI Guide

## Overview

This skill enables comprehensive understanding and effective usage of Chezmoi, a powerful dotfile management system for securely managing personal configuration files across multiple diverse machines with templating, encryption, and automation capabilities.

## Quick Start

Use the command reference and workflow guides to quickly accomplish common Chezmoi tasks, or consult the detailed template cookbook for advanced configuration scenarios.

## Core Workflows

### 1. Initial Setup and Bootstrap

For new machine setup or first-time Chezmoi users:

1. **Single-command bootstrap**: Use the one-shot installation for quick setup
2. **Repository initialization**: Set up source directory and remote configuration
3. **Initial file addition**: Add existing dotfiles to Chezmoi management
4. **First synchronization**: Push initial configuration to remote repository

Reference `references/command-reference.md` for detailed installation options and `references/troubleshooting.md` for common setup issues.

### 2. Daily Operations

For ongoing dotfile management:

1. **Status checking**: Use `chezmoi status` to understand current state
2. **Change review**: Run `chezmoi diff` before applying changes
3. **File modification**: Use `chezmoi edit` for managed file updates
4. **Synchronization**: Apply changes and push to remote with `chezmoi update`

Consult `references/command-reference.md` for detailed command usage patterns.

### 3. Template Creation and Management

For machine-specific configurations:

1. **Template design**: Create `.tmpl` files using Go template syntax
2. **Variable definition**: Set up data in `chezmoi.toml` or `.chezmoidata.yaml`
3. **Conditional logic**: Implement OS/host-specific configurations
4. **Testing and validation**: Verify template output before applying

Use `references/template-cookbook.md` for common patterns and `scripts/template-validator.py` for syntax validation.

### 4. Advanced Configuration

For complex setup scenarios:

1. **Encryption setup**: Configure age or GPG for sensitive files
2. **Password manager integration**: Set up 1Password, Bitwarden, or pass integration
3. **Script automation**: Create run_once, run_onchange scripts for system setup
4. **External resources**: Configure archives and external file sources

Reference `references/integration-patterns.md` for detailed setup instructions.

## File Type Management

### Configuration Files
- Use standard dotfiles (e.g., `dot_bashrc`) for static configurations
- Create templates (`.tmpl`) for dynamic content based on machine variables
- Apply encryption for sensitive configurations containing passwords or keys

### Scripts and Automation
- Use `run_once_` scripts for one-time setup operations (package installation)
- Use `run_onchange_` scripts for recurring operations when content changes
- Use `run_before_` and `run_after_` scripts for pre/post-apply operations

### Sensitive Data
- Apply `encrypted_` prefix for files requiring encryption (SSH keys, API tokens)
- Use `private_` prefix for files with restricted permissions (600)
- Integrate with password managers for dynamic secret retrieval

## Command Categories

### Initialization and Setup
- `chezmoi init` - Initialize new Chezmoi configuration
- `chezmoi init --apply` - Initialize and immediately apply changes
- `chezmoi init --one-shot` - Temporary environment setup

### File Management
- `chezmoi add` - Add files to Chezmoi management
- `chezmoi edit` - Edit managed files with automatic encryption handling
- `chezmoi forget` - Stop managing files while keeping them in place

### Status and Comparison
- `chezmoi status` - Show current state of managed files
- `chezmoi diff` - Display differences between actual and target states
- `chezmoi verify` - Check that system matches target state

### Template and Data
- `chezmoi data` - Display available template variables
- `chezmoi execute-template` - Test template output
- `chezmoi dump` - Show computed target state

### Synchronization
- `chezmoi update` - Pull and apply changes from remote
- `chezmoi cd` - Navigate to source directory for git operations

## Template Variables and Functions

### System Variables
- `.chezmoi.os` - Operating system (linux, darwin, windows)
- `.chezmoi.arch` - System architecture (amd64, arm64)
- `.chezmoi.hostname` - Machine hostname
- `.chezmoi.username` - Current username
- `.chezmoi.homeDir` - Home directory path

### Password Manager Functions
- `onepasswordRead` - Retrieve secrets from 1Password
- `bitwarden` - Access Bitwarden vault items
- `pass` - Use pass password manager
- `keyring` - Access system keychain

### Conditional Logic
Use Go template syntax for conditional configurations:
```go
{{ if eq .chezmoi.os "linux" }}
# Linux-specific configuration
{{ else if eq .chezmoi.os "darwin" }}
# macOS-specific configuration
{{ end }}
```

## Integration Patterns

### Git Workflow
- Configure automatic commit/push in `chezmoi.toml`
- Use branches for environment-specific configurations
- Implement proper merge conflict resolution

### Multi-Machine Management
- Use hostname-based conditional logic
- Implement shared templates with variable substitution
- Maintain separate data files for different machine types

### Package Management
- Create declarative package lists in YAML format
- Use run_once scripts for initial package installation
- Implement OS-specific package manager detection

## Common Usage Patterns

### Work vs Personal Machines
Set up conditional configurations based on hostname or custom variables:
```toml
[data]
    work_machine = {{ eq .chezmoi.hostname "work-laptop" }}
```

### Development Environment Setup
Use run_once scripts to install development tools and configure editors:
```bash
#!/bin/bash
# run_once_install-dev-tools.sh
{{ if eq .chezmoi.os "linux" }}
sudo apt install git vim tmux
{{ else if eq .chezmoi.os "darwin" }}
brew install git vim tmux
{{ end }}
```

### SSH and Security
Manage SSH keys and configurations with encryption:
```bash
chezmoi add --encrypt ~/.ssh/id_rsa
chezmoi add --encrypt ~/.ssh/config
```

## Resources

### scripts/
Executable utilities for common Chezmoi operations:

- `chezmoi-quick-setup.sh` - Automated installation and initialization script
- `template-validator.py` - Python script to validate Chezmoi template syntax
- `migration-helper.sh` - Script to migrate existing dotfiles to Chezmoi management

### references/
Comprehensive documentation loaded as needed:

- `command-reference.md` - Complete command reference with examples and usage patterns
- `template-cookbook.md` - Common template patterns, examples, and best practices
- `file-attributes.md` - Complete reference for file naming conventions and attributes
- `integration-patterns.md` - Detailed guides for password manager and service integrations
- `troubleshooting.md` - Common issues, error messages, and their solutions

### assets/
Template and configuration examples:

- `template-examples/` - Collection of common template files (.gitconfig.tmpl, .bashrc.tmpl)
- `config-examples/` - Sample configuration files (chezmoi.toml, chezmoi.yaml variants)
- `workflow-scripts/` - Example run_once, run_onchange, and automation scripts

## Troubleshooting

For common issues and error resolution:

1. **Template errors**: Use `chezmoi execute-template` to test templates
2. **Merge conflicts**: Use `chezmoi merge` with configured diff tools
3. **Permission issues**: Check file attributes and encryption settings
4. **Sync problems**: Verify git configuration and remote access

Consult `references/troubleshooting.md` for detailed error resolution guides.