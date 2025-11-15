# Fish Shell Plugins: Complete Guide

Fish shell is a modern, user-friendly command-line shell that offers powerful plugin and extensibility features. This comprehensive guide covers everything you need to know about creating, managing, and using Fish plugins to enhance your shell experience.

## Table of Contents

- [Introduction to Fish Plugins](#introduction-to-fish-plugins)
- [Fish Plugin Architecture](#fish-plugin-architecture)
- [Installation and Setup](#installation-and-setup)
- [Creating Custom Functions](#creating-custom-functions)
- [Working with Completions](#working-with-completions)
- [Configuration Management](#configuration-management)
- [Event-Driven Programming](#event-driven-programming)
- [Plugin Managers](#plugin-managers)
- [Popular Fish Plugins](#popular-fish-plugins)
- [Advanced Plugin Development](#advanced-plugin-development)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Introduction to Fish Plugins

Fish plugins extend the shell's functionality through custom functions, completions, configuration snippets, and event handlers. Unlike other shells that require complex frameworks, Fish's plugin system is built directly into the shell architecture.

### What Makes Fish Plugins Special

- **Zero Configuration**: Fish autoloads functions from standardized directories
- **Event-Driven**: Respond to shell events with custom handlers
- **Intelligent Completions**: Built-in completion system that's easy to extend
- **Web-based Configuration**: Visual interface for managing colors and settings
- **Universal Variables**: Persistent variables across sessions

## Fish Plugin Architecture

### Directory Structure

Fish follows a well-defined directory structure for plugins and configurations:

```
~/.config/fish/
├── config.fish              # Main configuration file
├── conf.d/                  # Configuration snippets
│   ├── aliases.fish
│   ├── env_vars.fish
│   └── theme.fish
├── functions/               # autoloaded functions
│   ├── ll.fish
│   ├── git_status.fish
│   └── custom_prompt.fish
├── completions/             # custom completions
│   ├── docker.fish
│   └── kubectl.fish
└── functions/               # Event handlers and utilities
    ├── fish_prompt.fish
    └── fish_user_key_bindings.fish
```

### Autoloading Mechanism

Fish automatically loads functions from directories in `fish_function_path`:

```fish
# Check function path
echo $fish_function_path

# Add custom function directory
set -a fish_function_path ~/.config/fish/custom_functions
```

## Installation and Setup

### Basic Fish Installation

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install fish

# macOS (Homebrew)
brew install fish

# Set Fish as default shell
chsh -s $(which fish)
```

### Plugin Directory Setup

```fish
# Create plugin directories
mkdir -p ~/.config/fish/{functions,completions,conf.d}

# Initialize configuration
touch ~/.config/fish/config.fish
```

## Creating Custom Functions

### Basic Function Definition

```fish
# File: ~/.config/fish/functions/ll.fish
function ll -d "List files in long format"
    ls -lh $argv
end
```

### Function with Arguments and Options

```fish
# File: ~/.config/fish/functions/backup.fish
function backup -d "Backup files to remote location"
    # Arguments with validation
    set -l source_dir $argv[1]
    set -l remote_host $argv[2]

    if test -z "$source_dir"
        echo "Error: Source directory required"
        return 1
    end

    # Flags and options
    if set -q _flag_compress
        tar -czf "$source_dir.tar.gz" "$source_dir"
        set source_dir "$source_dir.tar.gz"
    end

    # Main logic
    rsync -av "$source_dir" "$remote_host:/backups/"

    if test $status -eq 0
        echo "Backup completed successfully"
    else
        echo "Backup failed"
        return 1
    end
end

# Enable help text
complete -c backup -s h -l help -d "Show help"
```

### Function Inheritance and Wrapping

```fish
# File: ~/.config/fish/functions/safe_rm.fish
function safe_rm -w rm -d "Safe removal with trash"
    # Inherit completions from rm command
    if test (count $argv) -eq 0
        echo "Usage: safe_rm <files...>"
        return 1
    end

    # Move to trash instead of permanent deletion
    for file in $argv
        if test -e "$file"
            mv "$file" ~/.trash/(date +%Y%m%d_%H%M%S)_"(basename $file)"
            echo "Moved to trash: $file"
        else
            echo "File not found: $file"
        end
    end
end
```

### Universal Variable Functions

```fish
# File: ~/.config/fish/functions/set_theme.fish
function set_theme -d "Set Fish theme"
    set -U fish_color_normal normal
    set -U fish_color_command blue
    set -U fish_color_keyword purple
    set -U fish_color_quote yellow
    set -U fish_color_redirection cyan
    set -U fish_color_error red --bold

    echo "Theme applied successfully"
end
```

## Working with Completions

### Custom Command Completion

```fish
# File: ~/.config/fish/completions/myapp.fish
complete -c myapp -f

# Subcommand completions
complete -c myapp -n "__fish_use_subcommand" -a build -d "Build project"
complete -c myapp -n "__fish_use_subcommand" -a deploy -d "Deploy project"
complete -c myapp -n "__fish_use_subcommand" -a test -d "Run tests"

# Option completions
complete -c myapp -n "__fish_seen_subcommand_from build" -s o -l output -d "Output directory"
complete -c myapp -n "__fish_seen_subcommand_from build" -l verbose -d "Verbose output"

# Dynamic completions
complete -c myapp -n "__fish_seen_subcommand_from deploy" -a "(__fish_print_hostnames)" -d "Remote host"
```

### File Pattern Completions

```fish
# File: ~/.config/fish/completions/convert.fish
complete -c convert -a "(__fish_complete_suffix .jpg .png .gif .pdf)" -d "Image files"
complete -c convert -a "(__fish_complete_suffix .mp4 .avi .mov)" -d "Video files"

# Conditional completions
complete -c convert -n "__fish_seen_subcommand_from -format" -a png jpg gif pdf -d "Output format"
```

### Git-style Completion Example

```fish
# File: ~/.config/fish/completions/mygit.fish
function __fish_mygit_needs_command
    set -l cmd (commandline -opc)
    test (count $cmd) -eq 1
end

function __fish_mygit_using_command
    set -l cmd (commandline -opc)
    test (count $cmd) -gt 1; and test $cmd[2] = $argv[1]
end

complete -c mygit -n "__fish_mygit_needs_command" -a add -d "Add files to staging"
complete -c mygit -n "__fish_mygit_needs_command" -a commit -d "Create commit"
complete -c mygit -n "__fish_mygit_needs_command" -a push -d "Push to remote"

# Complete git branches for push command
complete -c mygit -n "__fish_mygit_using_command push" -a "(git branch --format='%(refname:short)')" -d "Branch name"
```

## Configuration Management

### Environment Configuration

```fish
# File: ~/.config/fish/conf.d/environment.fish
# Set PATH
set -gx PATH /usr/local/bin $PATH /opt/local/bin

# Set default editor
set -gx EDITOR vim

# Set language
set -gx LANG en_US.UTF-8

# Development environment
set -gx NODE_ENV development
set -gx PYTHONPATH /usr/local/lib/python3.9/site-packages
```

### Aliases and Shortcuts

```fish
# File: ~/.config/fish/conf.d/aliases.fish
# Navigation aliases
alias .. 'cd ..'
alias ... 'cd ../..'
alias md 'mkdir -p'

# Git aliases
alias gs 'git status'
alias ga 'git add'
alias gc 'git commit'
alias gp 'git push'

# Utility aliases
alias la 'ls -la'
alias lt 'ls -lat'
alias df 'df -h'
```

### Theme Configuration

```fish
# File: ~/.config/fish/conf.d/theme.fish
# Color scheme
set -U fish_color_normal normal
set -U fish_color_command blue
set -U fish_color_keyword green
set -U fish_color_quote yellow
set -U fish_color_redirection cyan
set -U fish_color_error red --bold
set -U fish_color_param cyan
set -U fish_color_comment 949494
set -U fish_color_selection --background=cyan
set -U fish_color_search_match --background=purple

# Pager colors
set -U fish_pager_color_completion normal
set -U fish_pager_color_description B3A06D yellow
set -U fish_pager_color_prefix white --bold --underline
set -U fish_pager_color_progress brwhite --background=cyan
```

## Event-Driven Programming

### Event Handler Functions

```fish
# File: ~/.config/fish/functions/fish_prompt -d "Custom prompt"
function fish_prompt
    # Git branch status
    set -l git_branch (git branch --show-current 2>/dev/null)
    set -l git_status ""

    if test -n "$git_branch"
        if git diff --quiet HEAD 2>/dev/null
            set git_status (set_color green)"$git_branch"(set_color normal)
        else
            set git_status (set_color red)"$git_branch*"(set_color normal)
        end
    end

    # Prompt components
    set -l user_host (set_color blue)$USER@(hostname -s)(set_color normal)
    set -l cwd (set_color cyan)(prompt_pwd)(set_color normal)
    set -l suffix (set_color normal)' ❯ '

    echo -n "$user_host $cwd $git_status$suffix"
end
```

### Event Listeners

```fish
# File: ~/.config/fish/functions/on_variable_pwd.fish
function on_variable_pwd --on-variable PWD
    # Update terminal title
    echo -ne "\033]0;(basename $PWD)\007"

    # Load project-specific environment if .env.fish exists
    if test -f .env.fish
        source .env.fish
    end
end

# File: ~/.config/fish/functions/on_fish_prompt.fish
function on_fish_prompt --on-event fish_prompt
    # Display notification if background job completed
    for job in (jobs -p)
        if test $job -lt 0
            echo (set_color green)"✓ Background job completed"(set_color normal)
        end
    end
end
```

### Custom Events

```fish
# File: ~/.config/fish/functions/notify_deploy.fish
function notify_deploy --on-event deploy_complete
    set -l message "Deployment completed at "(date)
    echo (set_color green)"✓ $message"(set_color normal)

    # Send system notification (if available)
    if command -v notify-send >/dev/null
        notify-send "Fish Shell" "$message"
    end
end

# Trigger custom event
function deploy_app
    # Deployment logic here
    # ...

    # Fire custom event
    emit deploy_complete
end
```

## Plugin Managers

### Fisher Plugin Manager

```fish
# Install Fisher
curl -sL https://raw.githubusercontent.com/jorgebucaran/fisher/main/functions/fisher.fish | source && fisher install jorgebucaran/fisher

# Install plugins
fisher install jethrokuan/z           # Pure prompt
fisher install franciscolourenco/done  # Command completion notifications
fisher install jorgebucaran/autopair.fish  # Auto-close brackets

# List installed plugins
fisher list

# Update plugins
fisher update

# Remove plugin
fisher remove jethrokuan/z

# Manage configuration
fisher edit jethrokuan/z
```

### Tide Plugin Manager

```fish
# Install Tide
fisher install IlanCosman/tide@v6

# Configure Tide
tide configure

# Configure individual items
tide configure prompt_character
tide configure git_status
tide configure node

# Reset to defaults
tide reload
```

### Fundle Plugin Manager

```fish
# Install Fundle
curl --silent https://git.io/fundle-install | source

# Fundle configuration in config.fish
# fundle plugin 'edc/bass'
# fundle plugin 'matchai/spacefish'

# Install plugins
fundle install

# Update all plugins
fundle update

# Clean up unused plugins
fundle clean
```

## Popular Fish Plugins

### Productivity Plugins

#### Z - Directory Jumper
```fish
# Install
fisher install jethrokuan/z

# Usage
z ~/projects/webapp
z documents
```

#### Done - Completion Notifications
```fish
# Install
fisher install franciscolourenco/done

# Configuration
set -U __done_min_cmd_duration 5000
set -U __done_exclude 'git (status|push|pull)'
```

#### AutoPair - Auto-close Brackets
```fish
# Install
fisher install jorgebucaran/autopair.fish

# Usage - automatically closes: (), [], {}, '', ""
```

### Theme Plugins

#### Pure Prompt
```fish
# Install
fisher install rafaelrinaldi/pure

# Configuration
set -U pure_symbol_prompt "❯"
set -U pure_color_muted (set_color 666)
```

#### Spacefish Prompt
```fish
# Install
fundle plugin 'matchai/spacefish'

# Configuration
set -g SPACEFISH_CHAR_COLOR_SUCCESS green
set -g SPACEFISH_DIR_COLOR blue
set -g SPACEFISH_GIT_COLOR_BRANCH yellow
```

### Development Plugins

#### Bass - Bash Integration
```fish
# Install
fisher install edc/bass

# Use bash scripts/functions in Fish
bass source ~/.nvm/nvm.sh
```

#### Docker Completions
```fish
# Install
fisher install brgmnn/fish-docker-completions

# Provides completions for docker commands
docker run <TAB>
docker build <TAB>
```

#### Kubernetes Completions
```fish
# Install
fisher install evanlucas/fish-kubectl-completions

# Kubernetes command completions
kubectl get pods <TAB>
kubectl apply -f <TAB>
```

## Advanced Plugin Development

### Plugin with External Commands

```fish
# File: ~/.config/fish/functions/ai_helper.fish
function ai_helper -d "AI-powered command assistant"
    set -l query (string join " " $argv)

    if test -z "$query"
        echo "Usage: ai_helper <command description>"
        return 1
    end

    # Call external AI service
    set -l api_key $OPENAI_API_KEY
    set -l response (curl -s -X POST \
        -H "Authorization: Bearer $api_key" \
        -H "Content-Type: application/json" \
        -d "{\"prompt\": \"Convert to shell command: $query\", \"max_tokens\": 100}" \
        https://api.openai.com/v1/completions)

    set -l command (echo $response | jq -r '.choices[0].text')

    if test -n "$command"
        echo "Suggested command: $command"
        read -l -P "Execute? [y/N] " confirm

        if test "$confirm" = "y" -o "$confirm" = "Y"
            eval $command
        end
    else
        echo "No command generated"
        return 1
    end
end
```

### Plugin with Configuration System

```fish
# File: ~/.config/fish/functions/project_manager.fish
# Configuration file
set -g __PROJECT_CONFIG_FILE ~/.config/fish/projects.json

function project_manager -d "Manage project environments"
    set -l action $argv[1]
    set -l project_name $argv[2]

    switch $action
        case add
            __project_add $project_name
        case list
            __project_list
        case activate
            __project_activate $project_name
        case '*'
            echo "Usage: project_manager [add|list|activate] <project>"
    end
end

function __project_add -a project_name
    set -l project_dir (pwd)
    set -l config (cat $__PROJECT_CONFIG_FILE 2>/dev/null; or echo '{}')

    # Update JSON configuration
    set -l new_config (echo $config | jq ". + {\"$project_name\": \"$project_dir\"}")
    echo $new_config > $__PROJECT_CONFIG_FILE

    echo "Added project: $project_name -> $project_dir"
end

function __project_activate -a project_name
    set -l config (cat $__PROJECT_CONFIG_FILE 2>/dev/null)
    set -l project_dir (echo $config | jq -r ".\"$project_name\" // empty")

    if test -n "$project_dir" -a -d "$project_dir"
        cd "$project_dir"

        # Load project-specific environment
        if test -f "$project_dir/.env.fish"
            source "$project_dir/.env.fish"
        end

        # Set project-specific variables
        set -gx PROJECT_NAME $project_name
        set -gx PROJECT_ROOT $project_dir

        echo "Activated project: $project_name"
    else
        echo "Project not found: $project_name"
        return 1
    end
end
```

### Plugin with Background Tasks

```fish
# File: ~/.config/fish/functions/file_watcher.fish
function file_watcher -d "Watch files and run commands on changes"
    set -l directory $argv[1]
    set -l command $argv[2..]

    if test -z "$directory" -o -z "$command"
        echo "Usage: file_watcher <directory> <command>"
        return 1
    end

    # Start background watcher
    inotifywait -m -r -e modify,create,delete "$directory" | while read event
        set -l file_path (echo $event | cut -d' ' -f3)
        echo "Change detected: $file_path"

        # Run the command in background
        eval $command &

        # Fire custom event
        emit file_changed $file_path
    end &

    set -l watcher_pid $last_pid
    echo "File watcher started (PID: $watcher_pid)"

    # Store PID for cleanup
    set -g __file_watcher_pids $__file_watcher_pids $watcher_pid
end

function on_file_changed --on-event file_changed
    set -l changed_file $argv[1]
    set -l timestamp (date +%H:%M:%S)

    echo "[$timestamp] File modified: $changed_file"
end

function stop_file_watchers -d "Stop all running file watchers"
    for pid in $__file_watcher_pids
        kill $pid 2>/dev/null
        echo "Stopped watcher (PID: $pid)"
    end

    set -e __file_watcher_pids
end
```

## Best Practices

### Plugin Organization

1. **Use Standard Directory Structure**
   ```
   ~/.config/fish/
   ├── functions/       # Your custom functions
   ├── completions/     # Custom completions
   └── conf.d/         # Configuration snippets
   ```

2. **Naming Conventions**
   - Function files: `function_name.fish`
   - Use descriptive, lowercase names with underscores
   - Prefix your functions to avoid conflicts: `myplugin_function_name`

3. **Documentation**
   ```fish
   function my_tool -d "Brief description of what the function does"
       # Add inline comments for complex logic
       # Include usage examples in help text
   end
   ```

### Error Handling

```fish
function robust_function -a required_arg
    # Validate required arguments
    if test -z "$required_arg"
        echo "Error: required_arg is required" >&2
        return 1
    end

    # Use try/catch with command status
    if not command_that_might_fail
        echo "Command failed" >&2
        return 1
    end

    # Cleanup on exit
    function cleanup --on-process-exit %self
        rm -f /tmp/temp_file
    end
end
```

### Performance Optimization

```fish
# Cache expensive operations
function __get_git_branch
    set -l cache_key (pwd)
    set -l cached_value $__git_branch_cache[$cache_key]

    if test -n "$cached_value"
        echo $cached_value
        return
    end

    set -l branch (git branch --show-current 2>/dev/null)
    set -g __git_branch_cache[$cache_key] $branch
    echo $branch
end
```

### Universal Variables

```fish
# Use universal variables for persistent settings
set -U myplugin_enabled true
set -U myplugin_timeout 30

# Avoid polluting global scope
set -l local_var "local to this function"

# Use __private variables for internal state
set -g __myplugin_internal_state "running"
```

## Troubleshooting

### Common Issues

#### Function Not Found

```fish
# Check function path
echo $fish_function_path

# Manually load function
source ~/.config/fish/functions/my_function.fish

# Debug function loading
functions -t my_function
```

#### Completion Not Working

```fish
# Check if completion file exists
ls ~/.config/fish/completions/

# Test completion manually
complete -C"mycommand "

# Debug completion system
set -x FISH_DEBUG_COMPLETIONS 1
```

#### Performance Issues

```fish
# Profile Fish startup
fish --profile-startup ~/fish_profile

# Analyze profiling output
sort -nr ~/fish_profile | head -20
```

### Debugging Tools

```fish
# Function inspection
functions my_function           # Show function definition
functions -n                   # List all functions
functions --details my_function # Show where function was loaded

# Variable inspection
set -n | grep myvar            # Find variables matching pattern
set -S myvar                   # Show variable scope and details

# Event debugging
functions --handlers           # List event handlers

# Trace execution
set -x FISH_DEBUG 1           # Enable debug output
```

### Plugin Conflicts

```fish
# Check for function conflicts
functions | grep -E "(duplicate|override)"

# Identify plugin conflicts
fish_config theme show        # Visual configuration check

# Reset to clean state
fish --no-config              # Start without loading configs
```

---

This guide provides a comprehensive foundation for developing and managing Fish shell plugins. Fish's simple yet powerful plugin system makes it easy to extend your shell with custom functionality, smart completions, and intelligent automation.

For more information, visit the [official Fish documentation](https://fishshell.com/docs/current/) and explore the growing ecosystem of community plugins.