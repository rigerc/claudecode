# Fish Shell: Comprehensive Guide

Fish (Friendly Interactive Shell) is a modern, user-friendly command line shell focused on usability and interactive use. This guide covers everything you need to know to get started with Fish and make the most of its powerful features.

## Table of Contents

- [Installation](#installation)
- [Getting Started](#getting-started)
- [Core Features](#core-features)
- [Syntax and Language](#syntax-and-language)
- [Configuration](#configuration)
- [Functions and Scripts](#functions-and-scripts)
- [Interactive Features](#interactive-features)
- [Customization](#customization)
- [Advanced Topics](#advanced-topics)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Installation

### On macOS

```bash
# Using Homebrew (recommended)
brew install fish

# Using MacPorts
sudo port install fish
```

### On Ubuntu/Debian

```bash
# Add official PPA (recommended)
sudo apt-add-repository ppa:fish-shell/release-4
sudo apt update
sudo apt install fish

# Development builds
sudo add-apt-repository ppa:fish-shell/nightly-master
sudo apt-get update
sudo apt-get install fish
```

### On Other Linux Distributions

```bash
# From source
git clone https://github.com/fish-shell/fish-shell
cd fish-shell
mkdir build && cd build
cmake ..
make
sudo make install

# Using package managers
# Fedora/CentOS: sudo dnf install fish
# Arch Linux: sudo pacman -S fish
# openSUSE: sudo zypper install fish
```

### Set Fish as Default Shell

```bash
# Change default login shell
chsh -s /usr/local/bin/fish  # macOS
chsh -s /usr/bin/fish         # Linux

# Or use the utility path
which fish | xargs chsh -s
```

## Getting Started

### Starting Fish

```bash
# Start a new Fish session
fish

# Exit Fish
exit

# Run commands directly
fish -c 'echo Hello from Fish!'

# Run a Fish script
fish script.fish
```

### Basic Commands

```bash
# Echo output
echo hello world
# Output: hello world

# List files with colors
ls

# Change to home directory
cd

# Get help
help set
man set
```

## Core Features

### 1. Smart Tab Completion

Fish provides intelligent, context-aware completions out of the box:

```bash
# Command completion
git [tab]  # Shows git subcommands

# File completion
cat /etc/[tab]  # Shows files in /etc/

# Option completion
ls --[tab]  # Shows ls options with descriptions
```

### 2. Syntax Highlighting

Fish highlights commands as you type:
- Green: Valid commands
- Red: Invalid commands
- Blue: Valid paths
- Magenta: Strings

### 3. Autosuggestions

Fish suggests commands as you type based on history:

```bash
# If you previously ran 'git status'
git st[autosuggestion: atus]  # Press right arrow to accept
```

### 4. Web-Based Configuration

```bash
# Open web configuration interface
fish_config

# Browse themes and prompts
fish_config theme show
fish_config prompt show
```

## Syntax and Language

### Variables

```bash
# Set variables
set smurf_color blue
set pants_color red

# Use variables
echo Smurfs are usually $smurf_color
echo Papa smurf wears $pants_color pants

# Local variables (function scope)
set -l local_var value

# Global variables
set -g global_var value

# Universal variables (persist across sessions)
set -U universal_var value

# Export to environment
set -x PATH $PATH /new/path

# Erase variables
set -e smurf_color
```

### Command Substitution

```bash
# Using parentheses
echo (date)
echo (pwd)

# Splitting on newlines (default)
printf '%s\n' (pkg-config --libs gio-2.0)
# Output: -lgio-2.0 -lgobject-2.0 -lglib-2.0

# Splitting on spaces
printf '%s\n' (pkg-config --libs gio-2.0 | string split -n " ")
# Output:
# -lgio-2.0
# -lgobject-2.0
# -lglib-2.0

# Split with null delimiter (handles spaces in filenames)
for i in (find . -print0 | string split0)
    echo "Found: $i"
end
```

### Lists and Arrays

```bash
# Create lists
set fruits apple banana orange

# Access elements
echo $fruits[1]  # apple
echo $fruits[-1] # orange (last element)

# List slicing
echo $fruits[2..3]  # banana orange

# List operations
set -l foo x y z
echo 1$foo  # 1x 1y 1z

# Combine lists
set -l a x y z
set -l b 1 2 3
echo $a$b  # x1 y1 z1 x2 y2 z2 x3 y3 z3

# Empty lists
set -l empty_list
echo $empty_listword  # Output is empty
echo "$empty_listword"  # Output is literally "word"
```

### Control Flow

#### If Statements

```bash
# Basic if/else
if grep fish /etc/shells
    echo Found fish
else if grep bash /etc/shells
    echo Found bash
else
    echo Got nothing
end

# Test conditions
if test "$fish" = "flounder"
    echo FLOUNDER
end

# Numerical comparisons
if test "$number" -gt 5
    echo $number is greater than five
else
    echo $number is five or less
end

# File tests
if test -e /etc/hosts
    echo We most likely have a hosts file
end

# Command existence
if command -sq fish; and grep fish /etc/shells
    echo fish is installed and configured
end
```

#### Loops

```bash
# For loops
for i in (seq 1 5)
    echo "Count: $i"
end

# While loops
set count 0
while test $count -lt 5
    echo "Count: $count"
    set count (math $count + 1)
end

# Loop over files
for file in *.txt
    echo "Processing: $file"
end
```

#### Functions

```bash
# Basic function definition
function say_hello
    echo Hello $argv
end

# Function with parameters
function greet
    set -l name $argv[1]
    set -l greeting $argv[2]
    echo "$greeting, $name!"
end

# Function with local variables
function calc_area
    set -l width $argv[1]
    set -l height $argv[2]
    math $width \* $height
end

# Usage examples
say_hello                    # Hello
say_hello everybody!        # Hello everybody!
greet "Alice" "Welcome"      # Welcome, Alice!
calc_area 5 4               # 20

# List all functions
functions

# Remove a function
functions -e say_hello
```

### Wildcards and Globbing

```bash
# Basic wildcards
ls *.jpg           # All .jpg files
ls l*.p*          # Files starting with 'l' and ending with 'p' + anything

# Recursive wildcards
ls /var/**.log    # All .log files in /var and subdirectories

# Brace expansion
echo input.{c,h,txt}  # input.c input.h input.txt

# Move files with multiple extensions
mv *.{c,h} src/

# Backup files
cp file{,.bak}       # Copies file to file.bak

# Complex expansion
set -l dogs hot cool cute "good "
echo {$dogs}dog      # hotdog cooldog cutedog good dog
```

### String Manipulation

```bash
# Basic string operations
string length "hello world"        # 11
string upper "hello"               # HELLO
string lower "HELLO"               # hello
string repeat "ha" 3               # hahaha

# Splitting and joining
set -l items "apple,banana,cherry"
string split "," $items            # apple banana cherry

string join "," apple banana cherry  # apple,banana,cherry

# Matching patterns
string match -r "fish" "shellfish"  # fish
string match -a "a" "banana"       # a a a

# Substrings
string sub -s 1 -l 3 "hello"       # hel
string sub -s -2 "hello"           # lo

# Replacement
string replace "old" "new" "old text"  # new text
```

### Math Operations

```bash
# Basic arithmetic
math 1+1                    # 2
math 5 * 2                 # 10
math 10 / 6                # 1.6666666667

# Different syntaxes
math "5 * 2"               # 10
math 5 "*" 2               # 10

# Precision control
math -s 3 10 / 6           # 1.667

# Complex expressions
math "sqrt(16) + 2^3"      # 12
```

## Configuration

### Configuration Files

```bash
# Main configuration file
~/.config/fish/config.fish

# Functions directory
~/.config/fish/functions/

# Completions directory
~/.config/fish/completions/

# Colors configuration
fish_config theme save
```

### Basic Configuration

```bash
# ~/.config/fish/config.fish

# Set PATH
set -gx PATH $HOME/.local/bin $PATH

# Interactive-only configuration
if status is-interactive
    # Set a nice theme
    fish_config theme choose coolbeans

    # Set custom greeting
    set -g fish_greeting "Welcome to Fish Shell!"

    # Custom aliases
    alias ll 'ls -la'
    alias la 'ls -a'
    alias .. 'cd ..'
end

# Login shell configuration
if status is-login
    # Run commands only for login shells
    echo "Login shell started at (date)"
end
```

### Environment Variables

```bash
# Set persistent environment variables
set -gx EDITOR vim
set -gx BROWSER firefox
set -gx LANG en_US.UTF-8

# Set PATH properly
set -gx PATH $HOME/bin $HOME/.local/bin /usr/local/bin $PATH

# Remove from PATH
set -e PATH[1]  # Remove first element

# Add to beginning of PATH
set -g PATH /custom/path $PATH
```

### Universal Variables

Universal variables persist across Fish sessions and are stored on disk:

```bash
# Set universal variable
set -U fish_key_bindings vi

# Set theme preference
set -U fish_color_command blue

# Check if universal variable exists
if set -q fish_key_bindings
    echo "Key bindings are set"
end
```

## Functions and Scripts

### Creating Functions

#### Method 1: Temporary Function

```bash
# Define function in current session
function mkcd
    mkdir -p $argv[1]
    cd $argv[1]
end
```

#### Method 2: Permanent Function

```bash
# Create file: ~/.config/fish/functions/mkcd.fish
function mkcd -d "Create directory and cd into it"
    mkdir -p $argv[1]
    cd $argv[1]
end

# Save function
funcsave mkcd
```

### Function Features

```bash
# Function with documentation
function md -d "Make directory and enter it"
    mkdir -p $argv[1]
    cd $argv[1]
end

# Function with argument validation
function backup_file -d "Backup a file with timestamp"
    if test (count $argv) -eq 0
        echo "Usage: backup_file <filename>"
        return 1
    end

    set -l file $argv[1]
    set -l backup (path change-extension (date +%Y%m%d_%H%M%S).$file:ext $file)
    cp $file $backup
    echo "Backed up $file to $backup"
end

# Function with event handlers
function notify_on_job_complete --on-job-exit %self
    echo "Job completed!"
    # Send notification (requires notify-send)
    command -v notify-send >/dev/null; and notify-send "Job Complete" "Background job finished"
end
```

### Fish Scripts

#### Shebang Lines

```fish
#!/usr/bin/env fish
# or
#!/usr/local/bin/fish

echo "Hello from Fish script $version"
```

#### Example Scripts

```fish
#!/usr/bin/env fish
# backup.fish - Backup important files

set -l backup_dir $HOME/backups/(date +%Y%m%d)
set -l files_to_backup $HOME/Documents $HOME/.config/fish

echo "Starting backup to $backup_dir..."

for dir in $files_to_backup
    if test -d $dir
        echo "Backing up $dir..."
        rsync -av $dir/ $backup_dir/(basename $dir)/
    else
        echo "Warning: $dir does not exist"
    end
end

echo "Backup completed!"
```

```fish
#!/usr/bin/env fish
# dev_helper.fish - Development helper functions

function git_cleanup -d "Clean up git branches"
    git fetch --prune
    git branch -d (git branch --merged | grep -v "^\*" | grep -v "main\|master")
    echo "Cleaned up merged branches"
end

function docker_clean -d "Clean up Docker containers and images"
    docker container prune -f
    docker image prune -f
    echo "Docker cleanup completed"
end

function project_setup -d "Set up a new project directory"
    set -l project_name $argv[1]
    test -z "$project_name"; and echo "Usage: project_setup <name>"; and return 1

    mkdir -p $project_name/{src,docs,tests}
    cd $project_name
    git init
    echo "# $project_name" > README.md
    echo "Project $project_name created"
end
```

## Interactive Features

### Key Bindings

```bash
# View current bindings
bind

# Add custom binding
bind ctrl-c cancel-commandline

# Bind to custom function
bind ctrl-r 'commandline -f history-search-backward'

# Vi-style bindings
set -g fish_key_bindings vi

# Emacs-style bindings (default)
set -g fish_key_bindings emacs
```

### History

```bash
# Search history
history                    # Show all history
history search "git"       # Search for git commands

# Clear history
history clear

# History navigation
history backward           # Up arrow
history forward            # Down arrow

# Interactive search (ctrl-r)
```

### Command Line Editing

```bash
# Move cursor
ctrl-a     # Beginning of line
ctrl-e     # End of line
ctrl-f     # Forward one character
ctrl-b     # Backward one character

# Delete
ctrl-u     # Delete to beginning
ctrl-k     # Delete to end
ctrl-w     # Delete previous word

# Yank (paste)
ctrl-y     # Yank deleted text

# Accept/Reject suggestions
right arrow    # Accept autosuggestion
alt-right      # Accept next word
ctrl-c         # Cancel autosuggestion
```

### Job Control

```bash
# Background jobs
sleep 10 &                    # Start in background
jobs                          # List jobs
fg %1                         # Bring job 1 to foreground
bg %1                         # Resume job 1 in background
kill %1                       # Kill job 1

# Job completion notification
function notify_on_complete --on-job-exit %1
    echo "Job %1 completed!"
end
```

## Customization

### Prompt Customization

```bash
# Create custom prompt
function fish_prompt
    # Exit status
    set -l last_status $status

    # Current directory (shortened)
    set -l cwd (prompt_pwd)

    # Git status
    set -l git_status (git rev-parse --git-dir >/dev/null 2>&1; and echo "⚡"; or echo "")

    # Prompt symbols
    set_color normal
    echo -n "[$cwd]$git_status "

    # Show prompt character based on status
    if test $last_status -eq 0
        set_color green
        echo -n "❯ "
    else
        set_color red
        echo -n "❌ "
    end

    set_color normal
end

funcsave fish_prompt
```

### Using fish_config

```bash
# Open web interface
fish_config

# Available themes
fish_config theme show

# Choose and save theme
fish_config theme choose coolbeans
fish_config theme save

# Available prompts
fish_config prompt show

# Choose and save prompt
fish_config prompt choose disco
fish_config prompt save
```

### Colors and Syntax Highlighting

```bash
# Color variables
set -g fish_color_command blue
set -g fish_color_keyword green
set -g fish_color_quote yellow
set -g fish_color_redirection cyan
set -g fish_color_end green
set -g fish_color_error red
set -g fish_color_param cyan
set -g fish_color_comment brown
set -g fish_color_selection --background=brblack
set -g fish_color_search_match --background=purple

# Save color scheme
fish_config theme save
```

### Custom Completions

```bash
# Create completion for custom command
# File: ~/.config/fish/completions/mytool.fish

complete -c mytool -f
complete -c mytool -s h -l help -d "Show help"
complete -c mytool -s v -l version -d "Show version"
complete -c mytool -s f -l file -r -d "Input file"
complete -c mytool -s o -l output -r -d "Output file"

# Conditional completions
complete -c mytool -n "__fish_use_subcommand" -a build -d "Build project"
complete -c mytool -n "__fish_use_subcommand" -a test -d "Run tests"
complete -c mytool -n "__fish_seen_subcommand_from build" -l release -d "Release build"
```

## Advanced Topics

### Event Handlers

```bash
# Function to run on variable change
function track_path_change --on-variable PWD
    echo "Changed directory to: $PWD"
end

# Function to run on command execution
function log_commands --on-event fish_preexec
    echo "Running: $history[1]" >> ~/.fish_command_log
end

# Function to run on prompt display
function update_git_status --on-event fish_prompt
    # Update git status in prompt
end
```

### Universal Variables for Configuration

```bash
# Persistent configuration across machines
set -U EDITOR vim
set -U BROWSER firefox
set -U fish_key_bindings vi
set -U fish_greeting ""

# Theme preferences
set -U fish_color_command blue
set -U fish_color_error red

# Custom aliases (stored as functions)
function ll -d "List all files with details"
    ls -la $argv
end
funcsave ll
```

### Path Manipulation

```bash
# Path operations with the path command
path basename /usr/local/bin/fish        # fish
path dirname /usr/local/bin/fish         # /usr/local/bin
path extension ./script.py               # .py
path change-extension .txt ./file.py     # ./file.txt

# Normalize and clean paths
path normalize ././foo//bar/../baz       # foo/baz

# Sort and unique paths
set -l clean_path (path sort $PATH | path unique)
```

### Performance Profiling

```bash
# Profile startup time
fish --profile-startup /tmp/start.prof -ic exit

# Analyze profile
sort -nk2 /tmp/start.prof

# Profile specific function
function --on-event fish_prompt
    # Your prompt code here
end

# Enable debug categories
fish -d debugger,ast
```

### Testing and Debugging

```bash
# Debug functions
functions --details fish_prompt

# Trace execution
fish --debug-level 2

# Check syntax
fish -n script.fish

# Test command existence
if command -v fish >/dev/null
    echo "Fish is available"
end
```

## Best Practices

### Script Organization

```bash
# Use descriptive function names
function create_backup_with_timestamp
    # ...
end

# Add documentation to functions
function deploy_project -d "Deploy project to staging environment"
    # ...
end

# Use local variables in functions
function calculate_area
    set -l width $argv[1]
    set -l height $argv[2]
    math $width \* $height
end
```

### Error Handling

```bash
# Check command success
if command cp source.txt destination.txt
    echo "Copy successful"
else
    echo "Copy failed"
    return 1
end

# Validate arguments
function process_file
    set -l file $argv[1]

    if test -z "$file"
        echo "Error: No file specified" >&2
        return 1
    end

    if not test -f "$file"
        echo "Error: File '$file' does not exist" >&2
        return 1
    end

    # Process file
end
```

### Performance Tips

```bash
# Use built-in commands instead of external ones
string length "hello"      # Faster than echo -n "hello" | wc -c
math 1+1                    # Faster than expr 1 + 1

# Avoid unnecessary command substitutions
set -l files *.txt         # Better than ls *.txt

# Use lists for multiple operations
set -l extensions .txt .md .rst
for ext in $extensions
    echo "Processing *$ext"
end
```

### Configuration Management

```bash
# Separate concerns in config.fish
if status is-interactive
    # Interactive-only settings
    set -g fish_greeting ""
    alias ll 'ls -la'
end

if status is-login
    # Login-only settings
    set -gx PATH $HOME/bin $PATH
end

# Use universal variables for persistent settings
set -U EDITOR vim
set -U fish_key_bindings vi
```

## Troubleshooting

### Common Issues

#### Fish Not in /etc/shells

```bash
# Add fish to shells
echo /usr/local/bin/fish | sudo tee -a /etc/shells

# Set as default
chsh -s /usr/local/bin/fish
```

#### Slow Startup

```bash
# Profile startup
fish --profile-startup /tmp/start.prof -ic exit
sort -nk2 /tmp/start.prof

# Common causes:
# - Heavy config.fish
# - Slow commands in prompt
# - Large history files
```

#### Colors Not Working

```bash
# Check terminal support
echo $TERM

# Reset color scheme
set -U fish_color_command normal
fish_config theme save

# Test colors
set_color red; echo "Red text"; set_color normal
```

#### Function Not Found

```bash
# Check function exists
functions | grep function_name

# Reload functions
source ~/.config/fish/functions/function_name.fish

# Check function directory
ls ~/.config/fish/functions/
```

### Getting Help

```bash
# Built-in help
help          # Open help in browser
help set      # Help for specific command

# Manual pages
man fish
man fish_config

# Command information
type set      # Show command type and location
functions --details fish_prompt  # Function source

# Debug mode
fish --debug-level 2  # Verbose debugging
```

### Debugging Scripts

```bash
# Check syntax without running
fish -n script.fish

# Run with debug output
fish -d all script.fish

# Trace execution
fish --debug-level 2 --debug-categories ast script.fish

# Test individual functions
function_name arg1 arg2
```

## Conclusion

Fish Shell provides a modern, intuitive command-line experience with features like intelligent completions, syntax highlighting, and a clean scripting syntax. Its focus on usability makes it excellent for both beginners and experienced users.

Key takeaways:
- Start with the web configuration tool (`fish_config`) for easy customization
- Use functions instead of aliases for complex operations
- Take advantage of Fish's smart completions and autosuggestions
- Store persistent settings with universal variables
- Write clean, readable scripts with Fish's straightforward syntax

Happy fishing! 🐠