# Fish Shell Plugin Development Guide

Complete reference for Fish shell plugin development, functions, completions, and best practices.

## Core Concepts

### Plugin Structure
```
~/.config/fish/
├── functions/       # autoloaded functions (.fish files)
├── completions/     # custom completions
├── conf.d/         # configuration snippets
└── config.fish     # main configuration
```

### Function Types
- **Simple functions**: Basic commands and utilities
- **Completion functions**: Tab completion logic
- **Event handlers**: Respond to shell events
- **Prompt functions**: Custom shell prompts

## Function Development

### Basic Function
```fish
function ll -d "List files in long format"
    ls -lh $argv
end
```

### Function with Arguments
```fish
function backup -a source destination -d "Backup files"
    if test -z "$source" -o -z "$destination"
        echo "Usage: backup <source> <destination>"
        return 1
    end

    cp -r "$source" "$destination"
    echo "Backup completed"
end
```

### Function with Options
```fish
function deploy -d "Deploy application"
    argparse 'e/env=' 'v/verbose' 'f/force' -- $argv
    or return 1

    if set -q _flag_verbose
        echo "Verbose mode enabled"
    end

    if set -q _flag_force
        echo "Force deployment"
    end

    echo "Deploying to $_flag_env"
end
```

## Completion Development

### Basic Completion
```fish
complete -c myapp -f
complete -c myapp -n "__fish_use_subcommand" -a build deploy test
```

### Dynamic Completions
```fish
complete -c myapp -n "__fish_seen_subcommand_from deploy" -a "(git branch --format='%(refname:short)')"
```

### File Completions
```fish
complete -c myapp -a "(__fish_complete_suffix .json .yaml .yml)"
```

## Event Handling

### Event Functions
```fish
function on_fish_prompt --on-event fish_prompt
    # Runs before each prompt
end

function on_variable_pwd --on-variable PWD
    # Runs when directory changes
end
```

### Custom Events
```fish
function notify_complete --on-event deploy_complete
    echo "Deployment finished"
end

# Trigger event
function deploy
    # deployment logic
    emit deploy_complete
end
```

## Plugin Management

### Using Fisher
```fish
# Install Fisher
curl -sL https://raw.githubusercontent.com/jorgebucaran/fisher/main/functions/fisher.fish | source

# Install plugins
fisher install jethrokuan/z  # Directory jumper
fisher install rafaelrinaldi/pure  # Prompt theme
```

### Manual Installation
```fish
# Copy files to appropriate directories
cp my_functions.fish ~/.config/fish/functions/
cp my_completions.fish ~/.config/fish/completions/
```

## Best Practices

### Error Handling
```fish
function safe_operation
    set -l result (command_that_might_fail)
    if test $status -ne 0
        echo "Operation failed" >&2
        return 1
    end
    echo "Success: $result"
end
```

### Performance
- Cache expensive operations
- Avoid heavy operations in prompt functions
- Use `functions -e` to erase unused functions

### Naming
- Use descriptive names
- Prefix with plugin name to avoid conflicts
- Use underscores for multi-word names

## Advanced Patterns

### State Management
```fish
set -g __myplugin_state "running"

function __myplugin_cleanup --on-process-exit %self
    set -e __myplugin_state
end
```

### Background Tasks
```fish
function background_worker
    long_running_task &
    set -l worker_pid $last_pid
    set -g __worker_pids $__worker_pids $worker_pid
end
```

### Configuration
```fish
function myplugin_configure
    set -U myplugin_timeout 30
    set -U myplugin_enabled true
end
```

## Testing

### Function Testing
```fish
function test_my_function
    set -l result (my_function test_input)
    if test "$result" != "expected_output"
        echo "Test failed"
        return 1
    end
    echo "Test passed"
end
```

### Completion Testing
```fish
# Test completions manually
complete -C"myapp "
```

## Debugging

### Debug Functions
```fish
functions -t my_function  # Trace function execution
functions my_function     # Show function definition
```

### Debug Completions
```fish
set -x FISH_DEBUG_COMPLETIONS 1
```

### Profile Performance
```fish
fish --profile-startup ~/profile
sort -nr ~/profile | head -20
```