#!/bin/bash
# Setup pre-commit hooks for Claude Extensions validation

set -e

echo "🔧 Setting up pre-commit hooks..."

# Create .git/hooks directory if it doesn't exist
mkdir -p .git/hooks

# Create pre-commit hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
# Pre-commit hook for Claude Extensions plugin validation

echo "🔍 Running pre-commit validation..."

# Store the current directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

# Check if we're modifying plugins or marketplace files
CHANGED_FILES=$(git diff --cached --name-only)

# Flags to track what needs validation
VALIDATE_PLUGINS=false
VALIDATE_MARKETPLACE=false
NEEDS_BUILD=false

# Check changed files
for file in $CHANGED_FILES; do
    if [[ "$file" == plugins/* ]]; then
        VALIDATE_PLUGINS=true
        NEEDS_BUILD=true
    fi

    if [[ "$file" == ".claude-plugin/marketplace.json" ]]; then
        VALIDATE_MARKETPLACE=true
    fi

    if [[ "$file" == "scripts/build-marketplace.py" ]]; then
        NEEDS_BUILD=true
    fi
done

# Run validations based on changes
if [ "$VALIDATE_PLUGINS" = true ]; then
    echo "  📁 Plugin changes detected - running validation..."
    make check || {
        echo "❌ Plugin validation failed. Please fix the issues before committing."
        exit 1
    }
fi

if [ "$VALIDATE_MARKETPLACE" = true ]; then
    echo "  📋 Marketplace changes detected - validating..."
    if ! jq empty .claude-plugin/marketplace.json 2>/dev/null; then
        echo "❌ Invalid marketplace.json"
        exit 1
    fi
fi

# Rebuild if plugins or build script changed
if [ "$NEEDS_BUILD" = true ]; then
    echo "  🏗️  Rebuilding marketplace and README..."
    python scripts/build-marketplace.py > /dev/null 2>&1

    # Check if marketplace or README changed
    if [ -n "$(git status --porcelain .claude-plugin/marketplace.json README.md 2>/dev/null)" ]; then
        echo "  📝 Marketplace files updated - adding to commit..."
        git add .claude-plugin/marketplace.json README.md 2>/dev/null || true
    fi
fi

# Quick markdown lint check if markdownlint is available
if command -v markdownlint-cli2 >/dev/null 2>&1; then
    # Only lint changed markdown files
    MARKDOWN_FILES=$(echo "$CHANGED_FILES" | grep '\.md$' || true)
    if [ -n "$MARKDOWN_FILES" ]; then
        echo "  📝 Linting changed markdown files..."
        echo "$MARKDOWN_FILES" | xargs markdownlint-cli2 2>/dev/null || {
            echo "❌ Markdown linting failed. Run 'make lint' for details."
            exit 1
        }
    fi
fi

echo "✅ Pre-commit validation passed!"
EOF

# Make the hook executable
chmod +x .git/hooks/pre-commit

echo "✅ Pre-commit hooks installed successfully!"
echo ""
echo "Pre-commit hooks will now:"
echo "- Validate plugins when plugin files are changed"
echo "- Validate marketplace.json when it's changed"
echo "- Rebuild marketplace and README automatically"
echo "- Run markdown linting on changed files"
echo ""
echo "To disable hooks temporarily: git commit --no-verify"