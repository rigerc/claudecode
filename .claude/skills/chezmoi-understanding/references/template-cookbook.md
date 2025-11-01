# Chezmoi Template Cookbook

## Template Basics

Chezmoi uses Go's `text/template` syntax with Sprig function library. Template files end with `.tmpl` and are processed before being applied to the target location.

### Basic Syntax
```go
{{ variable }}                    # Output variable
{{ "literal string" }}            # Output literal
{{ function "arg1" "arg2" }}      # Call function
{{ if condition }}...{{ end }}    # Conditional block
{{ range items }}...{{ end }}     # Loop block
```

## System Variables

### Core System Information
```go
{{ .chezmoi.os }}                 # Operating system: linux, darwin, windows
{{ .chezmoi.arch }}               # Architecture: amd64, arm64, etc.
{{ .chezmoi.hostname }}           # Machine hostname
{{ .chezmoi.username }}           # Current username
{{ .chezmoi.homeDir }}            # Home directory path
{{ .chezmoi.sourceDir }}          # Chezmoi source directory
{{ .chezmoi.version }}            # Chezmoi version
```

### Kernel and System Details
```go
{{ .chezmoi.kernel.version }}     # Kernel version
{{ .chezmoi.osRelease.id }}       # OS release ID (ubuntu, fedora, etc.)
{{ .chezmoi.osRelease.versionId }} # OS version
{{ .chezmoi.osRelease.name }}     # OS name
```

### Hardware Information
```go
{{ .cpu.cores }}                  # Number of CPU cores
{{ .cpu.threads }}                # Number of CPU threads
{{ .memory.total }}               # Total memory in bytes
```

## Conditional Templates

### Operating System Specific Configuration
```go
# ~/.local/share/chezmoi/dot_bashrc.tmpl
{{ if eq .chezmoi.os "linux" }}
    # Linux-specific configuration
    export PATH="$PATH:/usr/local/bin"
    alias ls='ls --color=auto'
{{ else if eq .chezmoi.os "darwin" }}
    # macOS-specific configuration
    export PATH="$PATH:/usr/local/bin:/opt/homebrew/bin"
    alias ls='ls -G'
{{ else if eq .chezmoi.os "windows" }}
    # Windows-specific configuration
    export PATH="$PATH:/c/Program Files/Git/bin"
{{ end }}
```

### Hostname-Based Configuration
```go
# ~/.local/share/chezmoi/dot_gitconfig.tmpl
[user]
    email = {{ .email }}
    name = {{ if eq .chezmoi.hostname "work-laptop" }}{{ .name_work }}{{ else }}{{ .name_personal }}{{ end }}

[core]
{{ if eq .chezmoi.os "darwin" }}
    editor = /usr/local/bin/vim
{{ else if eq .chezmoi.os "linux" }}
    editor = /usr/bin/vim
{{ end }}
```

### Architecture-Specific Settings
```go
# ~/.local/share/chezmoi/dot_config/nvim/init.vim.tmpl
{{ if eq .chezmoi.arch "arm64" }}
    " ARM64-specific configuration
    let g:python3_host_prog = '/opt/homebrew/bin/python3'
{{ else if eq .chezmoi.arch "amd64" }}
    " x86_64-specific configuration
    let g:python3_host_prog = '/usr/bin/python3'
{{ end }}
```

## Variable Assignment and Usage

### Template Variables
```go
{{ $editor := "vim" }}
{{ if eq .chezmoi.os "darwin" }}
    {{ $editor = "/usr/local/bin/vim" }}
{{ else if eq .chezmoi.os "linux" }}
    {{ $editor = "/usr/bin/vim" }}
{{ end }}

export EDITOR="{{ $editor }}"
```

### Complex Conditional Logic
```go
{{ $isWork := false }}
{{ if or (eq .chezmoi.hostname "work-laptop") (eq .chezmoi.hostname "work-desktop") }}
    {{ $isWork = true }}
{{ end }}

{{ if $isWork }}
    # Work configuration
    export WORK_ENV="production"
    export COMPANY_EMAIL="{{ .work_email }}"
{{ else }}
    # Personal configuration
    export WORK_ENV="personal"
    export COMPANY_EMAIL="{{ .personal_email }}"
{{ end }}
```

## Password Manager Integration

### 1Password Integration
```go
# ~/.local/share/chezmoi/private_dot_ssh/config.tmpl
Host github.com
    User git
    IdentityFile ~/.ssh/id_rsa

Host work-server
    HostName {{ (onepasswordRead "op://Private/Work Server/hostname").value }}
    User {{ (onepasswordRead "op://Private/Work Server/username").value }}
    Port {{ (onepasswordRead "op://Private/Work Server/port").value | default "22" }}

Host *
    User {{ (onepasswordRead "op://Private/SSH/default_username").value }}
```

### Bitwarden Integration
```go
# ~/.local/share/chezmoi/dot_gitconfig.tmpl
[user]
    email = {{ (bitwarden "item" "GitHub").login.username }}

[github]
    token = {{ (bitwarden "item" "GitHub").login.password }}

[gitlab]
    token = {{ (bitwarden "item" "GitLab").login.password }}
```

### Pass Integration
```go
# ~/.local/share/chezmoi/dot_npmrc.tmpl
//registry.npmjs.org/:_authToken={{ pass "npm/authtoken" }}
//registry.github.com/:_authToken={{ pass "github/npm_token" }}
```

### Keychain Integration
```go
# ~/.local/share/chezmoi/dot_aws/credentials.tmpl
[default]
aws_access_key_id = {{ keyring "aws" "access_key_id" }}
aws_secret_access_key = {{ keyring "aws" "secret_access_key" }}

[work]
aws_access_key_id = {{ keyring "aws-work" "access_key_id" }}
aws_secret_access_key = {{ keyring "aws-work" "secret_access_key" }}
```

## Advanced Template Patterns

### Package Management Templates
```go
# ~/.local/share/chezmoi/run_once_install-packages.sh.tmpl
#!/bin/bash
set -e

{{ if eq .chezmoi.os "linux" }}
    {{ if eq .chezmoi.osRelease.id "ubuntu" }}
        sudo apt-get update
        sudo apt-get install -y {{ join .packages.ubuntu " " }}
    {{ else if eq .chezmoi.osRelease.id "fedora" }}
        sudo dnf install -y {{ join .packages.fedora " " }}
    {{ else if eq .chezmoi.osRelease.id "arch" }}
        sudo pacman -S --needed {{ join .packages.arch " " }}
    {{ end }}
{{ else if eq .chezmoi.os "darwin" }}
    brew install {{ join .packages.macos " " }}
{{ end }}

echo "Packages installed successfully"
```

### Development Environment Setup
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

# Language-specific configurations
{{ if .development.go }}
    set -gx GOPATH $HOME/go
    set -gx PATH $GOPATH/bin $PATH
{{ end }}

{{ if .development.node }}
    set -gx NVM_DIR $HOME/.nvm
    set -gx PATH $HOME/.npm-global/bin $PATH
{{ end }}

{{ if .development.python }}
    set -gx PATH $HOME/.local/bin $PATH
    set -gx PYENV_ROOT $HOME/.pyenv
    set -gx PATH $PYENV_ROOT/bin $PATH
{{ end }}
```

### Application Configuration Templates
```go
# ~/.local/share/chezmoi/dot_config/alacritty/alacritty.yml.tmpl
window:
  opacity: {{ if .dark_theme }}0.95{{ else }}0.85{{ end }}

font:
  normal:
    family: {{ .font.family | default "JetBrains Mono" }}
    size: {{ .font.size | default "12.0" }}

colors:
  {{ if .dark_theme }}
  primary:
    background: '0x282c34'
    foreground: '0xabb2bf'
  {{ else }}
  primary:
    background: '0xf8f8f2'
    foreground: '0x272822'
  {{ end }}

shell:
  program: {{ .shell.program | default "/bin/bash" }}
  args:
    - --login
```

## Data File Templates

### YAML Data File
```yaml
# ~/.local/share/chezmoi/.chezmoidata.yaml
email: user@example.com
github_username: johndoe
editor: vim
dark_theme: true

work_laptop: false
development:
  go: true
  node: true
  python: true

packages:
  ubuntu:
    - git
    - vim
    - tmux
    - curl
  fedora:
    - git
    - vim
    - tmux
    - curl
  macos:
    - git
    - vim
    - tmux
    - curl

font:
  family: JetBrains Mono
  size: 12.0

shell:
  program: /bin/bash
```

### JSON Data File
```json
{
  "email": "user@example.com",
  "github_username": "johndoe",
  "editor": "vim",
  "dark_theme": true,
  "work_laptop": false,
  "development": {
    "go": true,
    "node": true,
    "python": true
  },
  "packages": {
    "ubuntu": ["git", "vim", "tmux", "curl"],
    "fedora": ["git", "vim", "tmux", "curl"],
    "macos": ["git", "vim", "tmux", "curl"]
  },
  "font": {
    "family": "JetBrains Mono",
    "size": 12.0
  },
  "shell": {
    "program": "/bin/bash"
  }
}
```

## Interactive Templates

### Prompt Functions
```go
# ~/.local/share/chezmoi/.chezmoi.toml.tmpl
{{- $email := promptStringOnce . "email" "What is your email address?" -}}
{{- $name := promptStringOnce . "name" "What is your name?" -}}
{{- $work := promptBoolOnce . "work_setup" "Is this a work machine?" -}}

[data]
    email = {{ $email | quote }}
    name = {{ $name | quote }}
    work_setup = {{ $work }}

    {{- if $work }}
    company = {{ promptStringOnce . "company" "What is your company name?" | quote }}
    {{- end }}
```

### Choice Prompts
```go
# ~/.local/share/chezmoi/.chezmoi.toml.tmpl
{{- $choices := list "desktop" "laptop" "server" "termux" -}}
{{- $hosttype := promptChoiceOnce . "hosttype" "What type of host are you on?" $choices -}}
{{- $editor := promptChoiceOnce . "editor" "What editor do you prefer?" (list "vim" "emacs" "vscode") -}}

[data]
    hosttype = {{ $hosttype | quote }}
    editor = {{ $editor | quote }}

    {{- if eq $hosttype "server" }}
    server_mode = true
    {{- end }}
```

## Template Testing and Debugging

### Test Template Output
```bash
# Test basic template
chezmoi execute-template '{{ .chezmoi.hostname }}'

# Test complex template
chezmoi execute-template '{{ if eq .chezmoi.os "linux" }}Linux{{ else }}Not Linux{{ end }}'

# Test template with data
chezmoi execute-template '{{ .email }}'

# Test template from file
chezmoi cd
chezmoi execute-template < dot_bashrc.tmpl

# Test with simulated prompts
chezmoi execute-template --init --promptString "email=me@home.org" < .chezmoi.toml.tmpl
```

### Debug Template Variables
```go
# Debug template
{{ debug.Printf "OS: %s, Hostname: %s\n" .chezmoi.os .chezmoi.hostname }}
{{ debug.Printf "Data: %+v\n" . }}
```

## Shared Templates

### Create Shared Templates
```go
# ~/.local/share/chezmoi/.chezmoitemplates/colors.conf
background = {{ .bg }}
foreground = {{ .fg }}
cursor = {{ .cursor }}

{{ if .colors.primary }}
[colors.primary]
    background = {{ .colors.primary.background }}
    foreground = {{ .colors.primary.foreground }}
{{ end }}
```

### Use Shared Templates
```go
# ~/.local/share/chezmoi/dot_config/terminal/light.conf.tmpl
{{ template "colors.conf" dict "bg" "#ffffff" "fg" "#000000" "cursor" "#ff0000" "colors" (dict "primary" (dict "background" "#ffffff" "foreground" "#000000")) }}

# ~/.local/share/chezmoi/dot_config/terminal/dark.conf.tmpl
{{ template "colors.conf" dict "bg" "#000000" "fg" "#ffffff" "cursor" "#00ff00" "colors" (dict "primary" (dict "background" "#000000" "foreground" "#ffffff")) }}
```

## Custom Template Functions

### Template Delimiters
```go
#!/bin/bash
# chezmoi:template:left-delimiter="# [[" right-delimiter=]]

echo "Hostname: # [[ .chezmoi.hostname ]]"
echo "OS: # [[ .chezmoi.os ]]"
echo "Home: # [[ .chezmoi.homeDir ]]"
```

### Advanced Function Usage
```go
# String manipulation
{{ .chezmoi.hostname | upper }}
{{ .email | replace "@" " at " }}
{{ .chezmoi.homeDir | base }}

# Mathematical operations
{{ add 1 2 }}
{{ mul .cpu.cores 2 }}
{{ mod 5 2 }}

# List operations
{{ list "a" "b" "c" | join "," }}
{{ split "a,b,c" "," }}
{{ first (list "a" "b" "c") }}

# Conditional functions
{{ if and (eq .chezmoi.os "linux") (.development.go) }}
# Linux and Go development enabled
{{ end }}
```

## Error Handling

### Default Values
```go
{{ .editor | default "vim" }}
{{ .font.size | default "12.0" }}
{{ .shell.program | default "/bin/bash" }}
```

### Safe Template Access
```go
{{ if .packages }}
{{ if .packages.ubuntu }}
Packages for Ubuntu: {{ join .packages.ubuntu ", " }}
{{ end }}
{{ end }}
```

### Template Validation
```bash
# Validate template syntax
chezmoi execute-template < template.tmpl

# Test with actual data
chezmoi cd
chezmoi execute-template < dot_config.tmpl > /tmp/test_output
```

## Performance Considerations

### Efficient Templates
```go
# Good: Cache repeated computations
{{ $isLinux := eq .chezmoi.os "linux" }}
{{ if $isLinux }}
# Linux-specific code
{{ end }}
{{ if $isLinux }}
# More Linux code
{{ end }}

# Avoid: Repeated expensive operations
{{ if eq .chezmoi.os "linux" }}  # Computed multiple times
{{ if eq .chezmoi.os "linux" }}  # Computed again
```

### Template Organization
```go
# Split large templates into logical sections
{{ template "header" . }}
{{ template "body" . }}
{{ template "footer" . }}

# Use partial templates for reusable components
{{ template "ssh-config" . }}
{{ template "git-config" . }}
```