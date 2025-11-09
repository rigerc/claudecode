# Makefile for Claude Extensions Plugin Collection

.PHONY: help build clean lint test validate

# Default target
help:
	@echo "Claude Extensions Plugin Collection"
	@echo ""
	@echo "Available targets:"
	@echo "  build     - Build marketplace.json and README.md from plugins/"
	@echo "  validate  - Validate plugin structure and generated files"
	@echo "  lint      - Lint markdown files in plugins/"
	@echo "  test      - Run all tests and validations"
	@echo "  clean     - Clean generated files"
	@echo "  help      - Show this help message"

# Build marketplace configuration and README
build:
	@echo "🏗️  Building marketplace configuration and README..."
	@python scripts/build-marketplace.py
	@echo "✅ Build complete!"

# Validate plugin structure and generated files
validate:
	@echo "🔍 Validating plugin structure..."
	@python scripts/build-marketplace.py > /dev/null 2>&1
	@echo "✅ Plugin structure valid!"
	@echo ""
	@echo "🔍 Validating generated files..."
	@jq empty .claude-plugin/marketplace.json || (echo "❌ Invalid marketplace.json" && exit 1)
	@echo "✅ Generated files valid!"

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
test: validate lint
	@echo ""
	@echo "🎉 All tests passed!"

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