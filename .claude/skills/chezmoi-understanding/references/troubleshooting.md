# Chezmoi Troubleshooting Guide

## Common Issues and Solutions

### Installation Issues

#### Installation Fails with Permission Errors
```bash
# Problem: Permission denied during installation
curl -sfL https://chezmoi.io/install.sh | sh

# Solution: Install to user directory
curl -sfL https://chezmoi.io/install.sh | sh -s -- -b ~/.local/bin

# Or use package manager
brew install chezmoi  # macOS
sudo apt install chezmoi  # Ubuntu
```

#### Binary Not Found After Installation
```bash
# Problem: chezmoi command not found
chezmoi --version

# Solution: Add to PATH
echo 'export PATH="$PATH:$HOME/.local/bin"' >> ~/.bashrc
source ~/.bashrc

# Or install system-wide
sudo mv ~/.local/bin/chezmoi /usr/local/bin/chezmoi
```

### Initialization Issues

#### Repository Clone Fails
```bash
# Problem: Can't clone repository
chezmoi init https://github.com/user/dotfiles.git

# Solutions:
# Check repository URL
chezmoi init https://github.com/user/dotfiles

# Use SSH for private repos
chezmoi init git@github.com:user/dotfiles.git

# Check network connectivity
curl -I https://github.com

# Check authentication
git ls-remote https://github.com/user/dotfiles.git
```

#### Config File Generation Issues
```bash
# Problem: Config file not generated or prompts fail
chezmoi init

# Solution: Check config directory permissions
mkdir -p ~/.config/chezmoi
chmod 755 ~/.config/chezmoi

# Test template manually
chezmoi execute-template --init --promptString "email=test@example.com" < ~/.local/share/chezmoi/.chezmoi.toml.tmpl
```

### Template Issues

#### Template Syntax Errors
```bash
# Problem: Template contains syntax errors
chezmoi apply

# Solution: Test template syntax
chezmoi execute-template < template.tmpl

# Common syntax errors and fixes:
# Missing end blocks:
{{ if condition }}  # Add {{ end }}

# Unclosed functions:
{{ function arg    # Add closing }}

# Invalid variable access:
{{ .nonexistent }}  # Use default: {{ .nonexistent | default "value" }}
```

#### Template Variables Not Available
```bash
# Problem: Template variables show as empty
chezmoi execute-template '{{ .email }}'

# Solutions:
# Check data file location
cat ~/.local/share/chezmoi/.chezmoidata.yaml

# Verify config file format
chezmoi dump

# Test template with specific data
chezmoi execute-template --init --promptString "email=test@example.com" < template.tmpl
```

#### Template Permission Issues
```bash
# Problem: Can't write template files
chezmoi edit ~/.config/template.tmpl

# Solution: Check permissions
ls -la ~/.config/
chmod 755 ~/.config
chmod 644 ~/.config/template.tmpl
```

### Encryption Issues

#### Age Encryption Setup Problems
```bash
# Problem: Age encryption not working
chezmoi add --encrypt ~/.ssh/id_rsa

# Solutions:
# Check age installation
age --version

# Verify key file
cat ~/.config/chezmoi/key.txt

# Test encryption manually
echo "test" | age -r $(age-keygen -y ~/.config/chezmoi/key.txt) > test.age
age -d -i ~/.config/chezmoi/key.txt test.age
```

#### GPG Encryption Issues
```bash
# Problem: GPG encryption fails
chezmoi add --encrypt ~/.ssh/id_rsa

# Solutions:
# Check GPG installation
gpg --version

# List available keys
gpg --list-secret-keys

# Verify recipient in config
grep recipient ~/.config/chezmoi/chezmoi.toml

# Test GPG encryption
echo "test" | gpg --encrypt -r your-email@example.com > test.gpg
gpg --decrypt test.gpg
```

### Git Integration Issues

#### Auto-commit Fails
```bash
# Problem: Changes not automatically committed
chezmoi add ~/.bashrc

# Solutions:
# Check git configuration
chezmoi cd
git config user.name
git config user.email

# Configure auto-commit
echo '[git]
autoCommit = true
autoPush = true' >> ~/.config/chezmoi/chezmoi.toml

# Manual commit workflow
git add .
git commit -m "Add bashrc"
git push
exit
```

#### Merge Conflicts
```bash
# Problem: Merge conflicts during update
chezmoi update

# Solutions:
# View conflicts
chezmoi diff

# Use merge tool
chezmoi merge ~/.bashrc

# Accept target state
chezmoi apply --force

# Or update source state
chezmoi re-add ~/.bashrc
```

#### Remote Repository Issues
```bash
# Problem: Can't push to remote
chezmoi git push

# Solutions:
# Check remote URL
chezmoi cd
git remote -v

# Update remote URL
git remote set-url origin git@github.com:user/dotfiles.git

# Check authentication
ssh -T git@github.com

# Configure SSH key
ssh-keygen -t ed25519 -C "your-email@example.com"
cat ~/.ssh/id_ed25519.pub
# Add to GitHub SSH keys
```

### File Permission Issues

#### Permission Denied on Apply
```bash
# Problem: Permission denied when applying files
chezmoi apply

# Solutions:
# Check target directory permissions
ls -la ~/

# Fix permissions
chmod 755 ~/
chmod 755 ~/.config
chmod 700 ~/.ssh

# Check file attributes
chezmoi dump ~/.ssh/config

# Remove and re-add with correct attributes
chezmoi forget ~/.ssh/config
chezmoi add --private ~/.ssh/config
```

#### Executable Permissions Not Applied
```bash
# Problem: Scripts not executable after apply
chezmoi apply

# Solutions:
# Check source file name
ls -la ~/.local/share/chezmoi/executable_*

# Add executable attribute
chezmoi chattr +executable ~/bin/script

# Or re-add with executable flag
chezmoi forget ~/bin/script
chezmoi add --executable ~/bin/script
```

### Password Manager Integration Issues

#### 1Password Integration Fails
```bash
# Problem: 1Password functions not working
chezmoi execute-template '{{ (onepasswordRead "op://test") }}'

# Solutions:
# Check 1Password CLI installation
op --version

# Verify sign-in
eval $(op signin)

# Check account access
op item list

# Test manually
op read "op://Private/test"
```

#### Bitwarden Integration Issues
```bash
# Problem: Bitwarden functions return empty
chezmoi execute-template '{{ (bitwarden "item" "test") }}'

# Solutions:
# Check Bitwarden CLI installation
bw --version

# Verify login and unlock
bw login
export BW_SESSION=$(bw unlock --passwordenv BW_PASSWORD)

# Check session
bw status

# Test manually
bw get item "test"
```

### Performance Issues

#### Slow Apply Operations
```bash
# Problem: chezmoi apply is very slow
chezmoi apply

# Solutions:
# Check for large files
find ~/.local/share/chezmoi -type f -size +10M

# Exclude large files from management
echo "large-file" >> ~/.local/share/chezmoi/.chezmoiignore

# Use verbose mode to identify slow operations
chezmoi apply --verbose

# Check external resources
chezmoi diff --script-contents=false
```

#### Memory Usage Issues
```bash
# Problem: High memory usage during operations
chezmoi apply

# Solutions:
# Limit concurrent operations
# (Note: chezmoi doesn't have this setting, but you can)

# Process files individually
chezmoi apply ~/.bashrc
chezmoi apply ~/.vimrc

# Use exclude patterns
chezmoi apply --exclude=scripts
```

### External Resource Issues

#### Archive Downloads Fail
```bash
# Problem: External archives not downloading
chezmoi apply

# Solutions:
# Check network connectivity
curl -I https://github.com

# Verify external configuration
cat ~/.local/share/chezmoi/.chezmoiexternal.toml

# Test URL manually
curl -L https://github.com/ohmyzsh/ohmyzsh/archive/master.tar.gz

# Force refresh
chezmoi apply --refresh
```

#### External Resource Permissions
```bash
# Problem: Can't write external files
chezmoi apply

# Solutions:
# Check target directory permissions
ls -la ~/.config/

# Create directories manually
mkdir -p ~/.config/nvim
mkdir -p ~/.tmux/plugins

# Check disk space
df -h
```

## Debugging Commands

### System Health Check
```bash
# Check chezmoi installation and configuration
chezmoi doctor

# Check version
chezmoi --version

# Show configuration
chezmoi dump
```

### State Inspection
```bash
# Show all managed files
chezmoi managed

# Show unmanaged files
chezmoi unmanaged

# Show status
chezmoi status

# Show differences
chezmoi diff
```

### Template Debugging
```bash
# Show available template data
chezmoi data

# Test template execution
chezmoi execute-template 'Template: {{ .chezmoi.hostname }}'

# Test with specific data
chezmoi execute-template --init --promptString "email=test@example.com" < template.tmpl
```

### Git Debugging
```bash
# Check git status in source directory
chezmoi cd
git status
git log --oneline -10
git remote -v
exit

# Test git operations
chezmoi git status
chezmoi git log --oneline -5
```

## Configuration Validation

### Validate Configuration File
```bash
# Check TOML syntax
chezmoi dump

# Validate with specific config
chezmoi --config /path/to/config.toml dump

# Test configuration loading
chezmoi execute-template '{{ .chezmoi.configDir }}'
```

### Validate Data Files
```bash
# Check YAML syntax
python -c "import yaml; yaml.safe_load(open('~/.local/share/chezmoi/.chezmoidata.yaml'))"

# Check JSON syntax
python -c "import json; json.load(open('~/.local/share/chezmoi/.chezmoidata.json'))"

# Test data loading
chezmoi data
```

## Recovery Procedures

### Restore from Git History
```bash
# Navigate to source directory
chezmoi cd

# Show git history
git log --oneline

# Reset to previous commit
git reset --hard HEAD~1

# Apply specific commit
git checkout <commit-hash>
chezmoi apply
exit
```

### Recover from Corrupted State
```bash
# Backup current state
cp -r ~/.local/share/chezmoi ~/.local/share/chezmoi.backup

# Re-initialize from remote
chezmoi init --force https://github.com/user/dotfiles.git

# Or restore from backup
rm -rf ~/.local/share/chezmoi
mv ~/.local/share/chezmoi.backup ~/.local/share/chezmoi
```

### Reset Chezmoi Configuration
```bash
# Remove chezmoi configuration
rm -rf ~/.config/chezmoi

# Remove source directory (DANGEROUS)
rm -rf ~/.local/share/chezmoi

# Re-initialize
chezmoi init
```

## Performance Optimization

### Optimize Large Repositories
```bash
# Use shallow clones for initialization
chezmoi init --depth=1 https://github.com/user/dotfiles.git

# Exclude unnecessary files
echo "*.log" >> ~/.local/share/chezmoi/.chezmoiignore
echo "node_modules/" >> ~/.local/share/chezmoi/.chezmoiignore
echo ".cache/" >> ~/.local/share/chezmoi/.chezmoiignore

# Use sparse checkout for specific directories
chezmoi cd
git sparse-checkout init --cone
git sparse-checkout set dot_config/nvim dot_vimrc
exit
```

### Optimize Template Processing
```bash
# Cache expensive computations in templates
{{ $isLinux := eq .chezmoi.os "linux" }}

# Use include for external content
{{ include "external-template.txt" }}

# Minimize complex logic in templates
# Move logic to scripts when possible
```

## Common Error Messages

### "no such file or directory"
```bash
# Cause: Target directory doesn't exist
# Solution: Create directory or use create_ prefix
mkdir -p ~/.config/app
# Or rename to create_dot_config/app/
```

### "permission denied"
```bash
# Cause: Insufficient permissions
# Solution: Check and fix permissions
chmod 755 ~/.config
chmod 644 ~/.config/file
```

### "template: pattern: unexpected EOF"
```bash
# Cause: Incomplete template syntax
# Solution: Check template for missing {{ end }}
chezmoi execute-template < template.tmpl
```

### "cannot create encrypted file"
```bash
# Cause: Encryption not configured
# Solution: Set up encryption
age-keygen -o ~/.config/chezmoi/key.txt
# Add recipient to config
```

### "git remote not found"
```bash
# Cause: Remote repository not accessible
# Solution: Check URL and authentication
git remote -v
git ls-remote origin
```

## Getting Help

### Chezmoi Resources
```bash
# Built-in help
chezmoi help
chezmoi help <command>

# Documentation
man chezmoi
# Visit https://chezmoi.io
```

### Community Support
- GitHub Issues: https://github.com/twpayne/chezmoi/issues
- Discord: https://discord.gg/chezmoi
- Reddit: r/chezmoi

### Bug Reports
When reporting issues, include:
```bash
# System information
chezmoi doctor
chezmoi --version

# Error details
chezmoi apply --verbose 2>&1

# Configuration (remove sensitive data)
chezmoi dump | grep -v "password\|key\|token"
```

This troubleshooting guide covers the most common issues users encounter with Chezmoi, along with practical solutions and debugging techniques.