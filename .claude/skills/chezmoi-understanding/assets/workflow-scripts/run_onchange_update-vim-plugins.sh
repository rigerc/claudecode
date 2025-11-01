#!/bin/bash
# Vim plugin update script
# This script runs whenever its content changes

set -e

echo "Updating vim plugins..."

# Check if vim is available
if ! command -v vim &> /dev/null; then
    echo "vim is not installed. Skipping plugin update."
    exit 0
fi

# Check if vim-plug is installed
if [[ ! -f "$HOME/.vim/autoload/plug.vim" ]]; then
    echo "vim-plug is not installed. Installing..."
    curl -fLo ~/.vim/autoload/plug.vim --create-dirs \
        https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
fi

# Update plugins using vim-plug
echo "Running vim-plug update..."
vim +PlugUpdate +qall

echo "Vim plugins updated successfully!"

# Optional: Clean up unused plugins
read -p "Clean up unused plugins? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Cleaning up unused plugins..."
    vim +PlugClean! +qall
    echo "Cleanup completed."
fi

# Show plugin status
echo ""
echo "Plugin Status:"
vim +PlugStatus +qall