# Simple Makefile for Claude Code Extensions Marketplace

.PHONY: help generate clean watch validate install-deps

# Default target
help:
	@echo "Claude Code Extensions Marketplace"
	@echo ""
	@echo "Available commands:"
	@echo "  make generate    - Generate marketplace.json and README from .claude/"
	@echo "  make watch       - Watch for changes and auto-regenerate"
	@echo "  make validate    - Validate marketplace configuration"
	@echo "  make clean       - Clean generated files"
	@echo "  make install-deps- Install dependencies"
	@echo "  make help        - Show this help"

# Generate marketplace from .claude directory
generate:
	@echo "🚀 Generating marketplace..."
	python3 scripts/generate-marketplace.py

# Watch for changes and auto-regenerate
watch:
	@echo "👀 Starting file watcher..."
	./scripts/watch-and-regenerate.sh

# Validate marketplace configuration
validate:
	@echo "🔍 Validating marketplace..."
	@if [ -f ".claude-plugin/marketplace.json" ]; then \
		python3 -m json.tool .claude-plugin/marketplace.json > /dev/null && \
		echo "✅ marketplace.json is valid" || \
		echo "❌ marketplace.json is invalid"; \
	else \
		echo "❌ marketplace.json not found - run 'make generate' first"; \
	fi

# Clean generated files
clean:
	@echo "🧹 Cleaning generated files..."
	@rm -f .claude-plugin/marketplace.json
	@echo "✅ Cleaned marketplace.json"
	@echo "💡 Run 'make generate' to recreate"

# Install dependencies
install-deps:
	@echo "📦 Installing dependencies..."
	@command -v python3 >/dev/null 2>&1 || { echo "❌ Python 3 required"; exit 1; }
	@command -v jq >/dev/null 2>&1 || { echo "⚠️  jq recommended for validation"; }
	@command -v inotifywait >/dev/null 2>&1 || echo "⚠️  inotify-tools recommended for watch command"
	@echo "✅ Dependencies checked"

# Show statistics
stats:
	@echo "📊 Extension Statistics:"
	@echo "   Commands: $$(find .claude/commands -name '*.md' 2>/dev/null | wc -l | tr -d ' ')"
	@echo "   Skills: $$(find .claude/skills -name 'SKILL.md' 2>/dev/null | wc -l | tr -d ' ')"
	@echo "   Agents: $$(find .claude/agents -name '*.md' 2>/dev/null | wc -l | tr -d ' ')"
	@echo "   Hooks: $$(find .claude/hooks -name '*.md' 2>/dev/null | wc -l | tr -d ' ')"
	@if [ -f ".claude-plugin/marketplace.json" ]; then \
		echo "   Marketplace plugins: $$(jq '.plugins | length' .claude-plugin/marketplace.json 2>/dev/null | tr -d ' ')"; \
	fi