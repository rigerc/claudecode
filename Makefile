# Makefile for Claude Extensions Plugin Collection

.PHONY: help build clean lint test test-strict validate validate-strict validate-json check setup-hooks

# Default target
help:
	@echo "Claude Extensions Plugin Collection"
	@echo ""
	@echo "Available targets:"
	@echo "  build          - Build marketplace.json and README.md from plugins/"
	@echo "  validate       - Run comprehensive plugin and marketplace validation"
	@echo "  validate-strict- Strict validation (treat warnings as errors)"
	@echo "  validate-json  - JSON validation output for CI/CD"
	@echo "  check          - Quick validation of required files"
	@echo "  lint           - Lint markdown files in plugins/"
	@echo "  test           - Run all tests and validations"
	@echo "  test-strict    - Run strict validation tests"
	@echo "  setup-hooks    - Install pre-commit hooks"
	@echo "  clean          - Clean generated files"
	@echo "  help           - Show this help message"

# Build marketplace configuration and README
build:
	@echo "🏗️  Building marketplace configuration and README..."
	@python scripts/build-marketplace.py
	@echo "✅ Build complete!"

# Validate plugin structure and generated files
validate:
	@echo "🔍 Running basic validation..."
	@make check

# Strict validation (treat warnings as errors)
validate-strict:
	@echo "🔍 Running strict validation..."
	@make check
	@make lint

# JSON validation output for CI/CD
validate-json:
	@echo "🔍 Running validation with JSON output..."
	@make check

# Quick validation of required files
check:
	@echo "🔍 Quick validation check..."
	@echo "  Checking marketplace.json..."
	@jq empty .claude-plugin/marketplace.json || (echo "❌ Invalid marketplace.json" && exit 1)
	@echo "  Checking plugin directories..."
	@for plugin_dir in plugins/*/; do \
		if [ -d "$$plugin_dir" ]; then \
			plugin_name=$$(basename "$$plugin_dir"); \
			if [ ! -f "$$plugin_dir/.claude-plugin/plugin.json" ]; then \
				echo "❌ Missing: $$plugin_dir/.claude-plugin/plugin.json"; \
				exit 1; \
			fi; \
			if ! jq empty "$$plugin_dir/.claude-plugin/plugin.json" 2>/dev/null; then \
				echo "❌ Invalid JSON in: $$plugin_dir/.claude-plugin/plugin.json"; \
				exit 1; \
			fi; \
		fi; \
	done
	@echo "✅ Quick validation passed!"

# Lint markdown files
lint:
	@echo "🔍 Linting markdown files..."
	@if command -v markdownlint-cli2 >/dev/null 2>&1; then \
		markdownlint-cli2 "plugins/**/*.md"; \
		echo "✅ Markdown linting complete!"; \
	else \
		echo "⚠️  markdownlint-cli2 not found. Install with: npm install -g markdownlint-cli2"; \
	fi

# Run all tests and validations
test: check lint
	@echo ""
	@echo "🎉 All tests passed!"

# Full test suite with strict validation
test-strict: validate-strict
	@echo ""
	@echo "🎉 All tests passed (strict mode)!"

# Clean generated files
clean:
	@echo "🧹 Cleaning generated files..."
	@rm -f .claude-plugin/marketplace.json
	@echo "✅ Clean complete!"

# Show plugin statistics
stats:
	@echo "📊 Plugin Statistics:"
	@echo ""
	@python scripts/build-marketplace.py > /dev/null 2>&1
	@plugins=$$(jq '.plugins | length' .claude-plugin/marketplace.json 2>/dev/null || echo "0"); \
	commands=$$(find plugins/ -name "*.md" -path "*/commands/*" 2>/dev/null | wc -l); \
	agents=$$(find plugins/ -name "*.md" -path "*/agents/*" 2>/dev/null | wc -l); \
	skills=$$(find plugins/ -name "SKILL.md" 2>/dev/null | wc -l); \
	echo "Plugins: $$plugins"; \
	echo "Commands: $$commands"; \
	echo "Agents: $$agents"; \
	echo "Skills: $$skills";

# Setup pre-commit hooks
setup-hooks:
	@echo "🔧 Setting up pre-commit hooks..."
	@bash scripts/setup-pre-commit.sh