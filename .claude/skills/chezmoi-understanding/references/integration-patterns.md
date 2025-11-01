# Chezmoi Integration Patterns

## Password Manager Integration

### 1Password Integration

#### Setup
```bash
# Install 1Password CLI
brew install 1password-cli  # macOS
sudo apt install 1password-cli  # Ubuntu

# Sign in to 1Password
op account add
eval $(op signin)
```

#### Configuration
```toml
# ~/.config/chezmoi/chezmoi.toml
[onepassword]
    # Optional: specify account
    account = "myaccount.1password.com"
```

#### Template Usage
```go
# Basic secret retrieval
{{ (onepasswordRead "op://Private/SSH/private_key") }}

# Field-specific retrieval
{{ (onepasswordRead "op://Private/GitHub/login").value }}

# Document retrieval
{{ (onepasswordDocument "uuid") }}

# Item with vault specification
{{ (onepasswordRead "op://Vault Name/Item Name/field") }}
```

#### Examples
```go
# ~/.local/share/chezmoi/dot_gitconfig.tmpl
[user]
    email = {{ (onepasswordRead "op://Private/Email/personal").value }}
    name = {{ (onepasswordRead "op://Private/Name/full").value }}

[github]
    token = {{ (onepasswordRead "op://Private/GitHub/token").value }}
```

```go
# ~/.local/share/chezmoi/private_dot_ssh/config.tmpl
Host github.com
    User git
    IdentityFile ~/.ssh/id_rsa
    IdentityAgent ~/.config/1password/agent.sock

Host work-server
    HostName {{ (onepasswordRead "op://Work/SSH Server/hostname").value }}
    User {{ (onepasswordRead "op://Work/SSH Server/username").value }}
    Port {{ (onepasswordRead "op://Work/SSH Server/port").value | default "22" }}
```

### Bitwarden Integration

#### Setup
```bash
# Install Bitwarden CLI
brew install bitwarden-cli  # macOS
sudo apt install bitwarden-cli  # Ubuntu

# Login to Bitwarden
bw login
export BW_SESSION=$(bw unlock --passwordenv BW_PASSWORD)
```

#### Configuration
```toml
# ~/.config/chezmoi/chezmoi.toml
[bitwarden]
    # Optional: specify server URL
    server = "https://bitwarden.example.com"
```

#### Template Usage
```go
# Get item field
{{ (bitwarden "item" "GitHub").login.username }}
{{ (bitwarden "item" "GitHub").login.password }}

# Get attachment
{{ (bitwardenAttachmentByRef "id_rsa" "item" "SSH Keys") }}

# Get secure note
{{ (bitwarden "item" "API Keys").notes }}
```

#### Examples
```go
# ~/.local/share/chezmoi/dot_npmrc.tmpl
//registry.npmjs.org/:_authToken={{ (bitwarden "item" "NPM").login.password }}
//registry.github.com/:_authToken={{ (bitwarden "item" "GitHub Packages").login.password }}
```

```go
# ~/.local/share/chezmoi/dot_aws/credentials.tmpl
[default]
aws_access_key_id = {{ (bitwarden "item" "AWS").login.username }}
aws_secret_access_key = {{ (bitwarden "item" "AWS").login.password }}

[work]
aws_access_key_id = {{ (bitwarden "item" "AWS Work").login.username }}
aws_secret_access_key = {{ (bitwarden "item" "AWS Work").login.password }}
```

### Pass Integration

#### Setup
```bash
# Install pass
brew install pass  # macOS
sudo apt install pass  # Ubuntu

# Initialize pass store
pass init "your-email@example.com"
```

#### Template Usage
```go
# Get password
{{ pass "email/password" }}

# Get password with specific store
{{ pass "work/api-key" "/path/to/work-store" }}
```

#### Examples
```go
# ~/.local/share/chezmoi/dot_mbsyncrc.tmpl
IMAPAccount personal
Host imap.gmail.com
User {{ pass "email/personal/username" }}
PassCmd "pass email/personal/password"
```

### Keychain Integration

#### Template Usage
```go
# macOS Keychain
{{ keychain "account" "service" }}

# Windows Credential Manager
{{ keychain "username" "server" }}

# Linux Secret Service
{{ keyring "service" "username" }}
```

#### Examples
```go
# ~/.local/share/chezmoi/dot_gitconfig.tmpl
[user]
    email = {{ keyring "git" "email" }}
    name = {{ keyring "git" "name" }}

[github]
    token = {{ keyring "github" "token" }}
```

## Encryption Setup

### Age Encryption

#### Setup
```bash
# Install age
brew install age  # macOS
sudo apt install age  # Ubuntu

# Generate key
age-keygen -o ~/.config/chezmoi/key.txt

# Get public key
age-keygen -y ~/.config/chezmoi/key.txt
```

#### Configuration
```toml
# ~/.config/chezmoi/chezmoi.toml
encryption = "age"

[age]
    identity = "~/.config/chezmoi/key.txt"
    recipient = "age1ql3z7hjy54pw3hyww5ayyfg7zqgvc7w3j2elw8zmrj2kg5sfn9aqmcac8p"
```

#### Usage
```bash
# Add encrypted file
chezmoi add --encrypt ~/.ssh/id_rsa

# Edit encrypted file
chezmoi edit ~/.ssh/id_rsa

# View encrypted file
chezmoi cat ~/.ssh/id_rsa
```

### GPG Encryption

#### Setup
```bash
# Install GPG
brew install gnupg  # macOS
sudo apt install gnupg  # Ubuntu

# Generate key
gpg --full-generate-key

# List keys
gpg --list-secret-keys --keyid-format LONG
```

#### Configuration
```toml
# ~/.config/chezmoi/chezmoi.toml
encryption = "gpg"

[gpg]
    recipient = "user@example.com"
    # Or use key ID
    # recipient = "ABC1234567890ABC"
```

#### Usage
```bash
# Configure GPG agent
echo "default-cache-ttl 3600" >> ~/.gnupg/gpg-agent.conf
gpgconf --launch gpg-agent

# Add encrypted file
chezmoi add --encrypt ~/.ssh/id_rsa
```

## Git Integration

### Automatic Commit and Push

#### Configuration
```toml
# ~/.config/chezmoi/chezmoi.toml
[git]
    autoCommit = true
    autoPush = true
    commitMessageTemplate = "Update dotfiles: {{ .chezmoi.hostname }}"

    # Or use commit message template file
    commitMessageTemplateFile = ".commit_message.tmpl"
```

#### Custom Commit Messages
```go
# ~/.local/share/chezmoi/.commit_message.tmpl
{{ if .chezmoi.stdin.isTTY }}
{{ promptString "Commit message" "Enter commit message: " }}
{{ else }}
{{ .chezmoi.stdin.contents }}
{{ end }}
```

### Branch Strategy

#### Environment-Specific Branches
```bash
# Work branch
chezmoi cd
git checkout -b work
chezmoi edit ~/.gitconfig
# Edit work-specific configuration
git add .
git commit -m "Add work git config"
git push origin work
exit

# Personal branch
chezmoi cd
git checkout personal
chezmoi edit ~/.gitconfig
# Edit personal configuration
git add .
git commit -m "Update personal git config"
git push origin personal
exit
```

#### Merge Workflow
```bash
# Update from main branch
chezmoi cd
git checkout main
git pull origin main
git checkout work
git merge main
chezmoi apply
exit
```

### Repository Management

#### Multiple Repositories
```toml
# ~/.config/chezmoi/chezmoi.toml
[sourceDir]
    personal = "~/.dotfiles-personal"
    work = "~/.dotfiles-work"

# Use with chezmoi --source
chezmoi --source ~/.dotfiles-personal status
chezmoi --source ~/.dotfiles-work status
```

#### Submodule Integration
```bash
# Add submodule for shared configs
chezmoi cd
git submodule add https://github.com/user/shared-configs.git shared
git add .
git commit -m "Add shared configs submodule"
git push
exit
```

## Package Management Integration

### Declarative Package Installation

#### YAML Package Definition
```yaml
# ~/.local/share/chezmoi/packages.yaml
packages:
  darwin:
    brews:
    - git
    - vim
    - tmux
    - curl
    casks:
    - visual-studio-code
    - google-chrome

  ubuntu:
    apt:
    - git
    - vim
    - tmux
    - curl
    snap:
    - code --classic

  fedora:
    dnf:
    - git
    - vim
    - tmux
    - curl
```

#### Installation Script
```bash
# ~/.local/share/chezmoi/run_once_install-packages.sh.tmpl
#!/bin/bash
set -e

{{ if eq .chezmoi.os "linux" }}
    {{ if eq .chezmoi.osRelease.id "ubuntu" }}
        sudo apt-get update
        {{ range .packages.ubuntu.apt }}
        sudo apt-get install -y {{ . }}
        {{ end }}

        {{ range .packages.ubuntu.snap }}
        sudo snap install {{ . }}
        {{ end }}

    {{ else if eq .chezmoi.osRelease.id "fedora" }}
        sudo dnf update
        {{ range .packages.fedora.dnf }}
        sudo dnf install -y {{ . }}
        {{ end }}

    {{ end }}
{{ else if eq .chezmoi.os "darwin" }}
    # Update Homebrew
    brew update

    # Install brews
    {{ range .packages.darwin.brews }}
    brew install {{ . }}
    {{ end }}

    # Install casks
    {{ range .packages.darwin.casks }}
    brew install --cask {{ . }}
    {{ end }}
{{ end }}

echo "Packages installed successfully"
```

### Language Version Managers

#### Node.js (nvm)
```bash
# ~/.local/share/chezmoi/run_once_install-node.sh.tmpl
#!/bin/bash
set -e

{{ if eq .chezmoi.os "darwin" }}
    brew install nvm
    export NVM_DIR="$HOME/.nvm"
    [ -s "/opt/homebrew/opt/nvm/nvm.sh" ] && \. "/opt/homebrew/opt/nvm/nvm.sh"
{{ else if eq .chezmoi.os "linux" }}
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
{{ end }}

{{ range .node_versions }}
nvm install {{ . }}
{{ end }}

{{ range .npm_packages }}
npm install -g {{ . }}
{{ end }}
```

#### Python (pyenv)
```bash
# ~/.local/share/chezmoi/run_once_install-python.sh.tmpl
#!/bin bash
set -e

{{ if eq .chezmoi.os "darwin" }}
    brew install pyenv
{{ else if eq .chezmoi.os "linux" }}
    sudo apt-get install -y make build-essential libssl-dev zlib1g-dev \
        libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
        libncurses5-dev libncursesw5-dev xz-utils tk-dev
    curl https://pyenv.run | bash
{{ end }}

export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"

{{ range .python_versions }}
pyenv install {{ . }}
{{ end }}

{{ if .default_python }}
pyenv global {{ .default_python }}
{{ end }}
```

## External Resource Integration

### Archive Integration

#### Configuration
```toml
# ~/.local/share/chezmoi/.chezmoiexternal.toml
[".vim/pack/plugins/start/vim-plug"]
    type = "file"
    url = "https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim"
    refreshPeriod = "168h"

[".oh-my-zsh"]
    type = "archive"
    url = "https://github.com/ohmyzsh/ohmyzsh/archive/master.tar.gz"
    stripComponents = 1
    refreshPeriod = "168h"

[".tmux/plugins/tpm"]
    type = "archive"
    url = "https://github.com/tmux-plugins/tpm/archive/master.tar.gz"
    stripComponents = 1
    refreshPeriod = "168h"
```

#### Usage
```bash
# Apply external resources
chezmoi apply

# Force refresh of external resources
chezmoi apply --refresh
```

### GitHub Integration

#### GitHub CLI Integration
```go
# ~/.local/share/chezmoi/dot_gitconfig.tmpl
[github]
    user = {{ .github_username }}
    token = {{ (bitwarden "item" "GitHub").login.password }}

[credential "https://github.com"]
    helper = !gh auth git-credential
```

#### GitHub Repository Management
```bash
# Clone repository as external resource
echo '["dotfiles"]
type = "git-repo"
url = "https://github.com/user/dotfiles.git"
refreshPeriod = "1h"' > ~/.local/share/chezmoi/.chezmoiexternal.toml

# Use repository content
chezmoi apply
```

## Cloud Service Integration

### AWS Integration

#### Configuration
```go
# ~/.local/share/chezmoi/dot_aws/credentials.tmpl
[default]
aws_access_key_id = {{ keyring "aws" "access_key_id" }}
aws_secret_access_key = {{ keyring "aws" "secret_access_key" }}

[work]
aws_access_key_id = {{ keyring "aws-work" "access_key_id" }}
aws_secret_access_key = {{ keyring "aws-work" "secret_access_key" }}

[dev]
aws_access_key_id = {{ keyring "aws-dev" "access_key_id" }}
aws_secret_access_key = {{ keyring "aws-dev" "secret_access_key" }}
```

#### AWS CLI Configuration
```go
# ~/.local/share/chezmoi/dot_aws/config.tmpl
[default]
region = {{ .aws_region | default "us-east-1" }}

[profile work]
region = {{ .aws_work_region | default "us-west-2" }}

[profile dev]
region = {{ .aws_dev_region | default "eu-west-1" }}
```

### Docker Integration

#### Docker Configuration
```go
# ~/.local/share/chezmoi/dot_docker/config.json.tmpl
{
  "auths": {
    "https://index.docker.io/v1/": {
      "auth": {{ (bitwarden "item" "Docker Hub").login.password }}
    },
    "https://ghcr.io": {
      "auth": {{ (bitwarden "item" "GitHub Container Registry").login.password }}
    }
  },
  "credsStore": {{ if eq .chezmoi.os "darwin" }}"osxkeychain"{{ else if eq .chezmoi.os "linux" }}"secretservice"{{ end }}
}
```

#### Docker Compose Integration
```yaml
# ~/.local/share/chezmoi/docker-compose.yml.tmpl
version: '3.8'

services:
  app:
    image: {{ .docker_image | default "nginx:latest" }}
    ports:
      - "{{ .app_port | default "8080" }}:80"
    environment:
      - ENV={{ .environment | default "development" }}
```

## IDE and Editor Integration

### VS Code Integration

#### Settings Sync
```json
// ~/.local/share/chezmoi/dot_config/Code/User/settings.json.tmpl
{
    "git.enableSmartCommit": true,
    "git.autofetch": true,
    "editor.fontSize": {{ .vscode.font_size | default 14 }},
    "editor.fontFamily": "{{ .vscode.font_family | default \"'JetBrains Mono', monospace\" }}",
    "workbench.colorTheme": "{{ .vscode.theme | default \"Default Dark+\" }}",
    "terminal.integrated.shell.linux": {{ .vscode.shell.linux | quote }},
    "terminal.integrated.shell.osx": {{ .vscode.shell.macos | quote }}
}
```

#### Extensions Management
```bash
# ~/.local/share/chezmoi/run_once_install-vscode-extensions.sh.tmpl
#!/bin/bash
set -e

{{ range .vscode.extensions }}
code --install-extension {{ . }}
{{ end }}

echo "VS Code extensions installed"
```

### Vim/Neovim Integration

#### Plugin Management
```lua
# ~/.local/share/chezmoi/dot_config/nvim/lua/plugins.lua.tmpl
return {
    -- Core plugins
    {{ range .vim.plugins.core }}
    { "{{ . }}" },
    {{ end }}

    -- Language-specific plugins
    {{ if .development.go }}
    { "fatih/vim-go" },
    {{ end }}

    {{ if .development.python }}
    { "davidhalter/jedi-vim" },
    {{ end }}

    -- Theme
    {{ if .dark_theme }}
    { "morhetz/gruvbox" },
    {{ else }}
    { "altercation/vim-colors-solarized" },
    {{ end }}
}
```

## Shell Integration

### Zsh Integration

#### Oh My Zsh Setup
```bash
# ~/.local/share/chezmoi/run_once_install-oh-my-zsh.sh
#!/bin/bash
set -e

if [ ! -d "$HOME/.oh-my-zsh" ]; then
    sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
fi

echo "Oh My Zsh installed"
```

#### Zsh Configuration
```go
# ~/.local/share/chezmoi/dot_zshrc.tmpl
export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME="{{ .zsh.theme | default "robbyrussell" }}"

plugins = ({{ join .zsh.plugins " " }})

source $ZSH/oh-my-zsh.sh

# Custom aliases
{{ range .aliases }}
alias {{ .name }}="{{ .command }}"
{{ end }}

# Environment variables
{{ range .env_vars }}
export {{ .name }}="{{ .value }}"
{{ end }}
```

### Fish Shell Integration

#### Fish Configuration
```go
# ~/.local/share/chezmoi/dot_config/fish/config.fish.tmpl
# Fish shell configuration

{{ if eq .chezmoi.os "darwin" }}
    # macOS-specific paths
    set -gx PATH /opt/homebrew/bin /usr/local/bin $PATH
    set -gx HOMEBREW_PREFIX /opt/homebrew
{{ else if eq .chezmoi.os "linux" }}
    # Linux-specific paths
    set -gx PATH /usr/local/bin $PATH
{{ end }}

# Environment variables
{{ range .env_vars }}
set -gx {{ .name }} {{ .value }}
{{ end }}

# Abbreviations
{{ range .abbreviations }}
abbr {{ .name }} {{ .command }}
{{ end }}

# Functions
{{ if .fish.functions }}
{{ range .fish.functions }}
function {{ .name }}
    {{ .body }}
end

{{ end }}
{{ end }}
```

## Automation and Scripting

### System Service Integration

#### Systemd Services
```ini
# ~/.local/share/chezmoi/dot_config/systemd/user/backup.service.tmpl
[Unit]
Description=Personal backup service
After=network.target

[Service]
Type=oneshot
ExecStart=/home/{{ .chezmoi.username }}/.local/bin/backup-script
User={{ .chezmoi.username }}
```

```ini
# ~/.local/share/chezmoi/dot_config/systemd/user/backup.timer.tmpl
[Unit]
Description=Run backup service daily
Requires=backup.service

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
```

#### Cron Jobs
```bash
# ~/.local/share/chezmoi/run_once_setup-crontab.sh.tmpl
#!/bin/bash
set -e

# Create crontab entry
(crontab -l 2>/dev/null; echo "0 2 * * * /home/{{ .chezmoi.username }}/.local/bin/daily-backup") | crontab -

echo "Crontab updated"
```

### Backup Integration

#### Backup Script Template
```bash
# ~/.local/share/chezmoi/executable_dot_local/bin/backup.sh.tmpl
#!/bin/bash
set -e

BACKUP_DIR="{{ .backup.directory | default "$HOME/backup" }}"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Backup specific directories
{{ range .backup.directories }}
echo "Backing up {{ . }}..."
tar czf "$BACKUP_DIR/{{ . | base }}_$DATE.tar.gz" "{{ . }}"
{{ end }}

# Upload to cloud storage if configured
{{ if .backup.s3.bucket }}
aws s3 cp "$BACKUP_DIR" "s3://{{ .backup.s3.bucket }}/" --recursive
{{ end }}

echo "Backup completed: $BACKUP_DIR"
```

This integration guide provides comprehensive patterns for connecting Chezmoi with various external services, password managers, encryption tools, and development workflows. Each integration includes setup instructions, configuration examples, and practical usage templates.