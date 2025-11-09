#!/bin/bash
# CI/CD validation script for Claude Extensions

set -e

echo "🚀 Running CI/CD validation..."

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Track errors
ERRORS=0
WARNINGS=0

# Step 1: Validate JSON syntax
print_status $BLUE "Step 1/4: Validating JSON syntax..."
print_status $BLUE "  Checking marketplace.json..."
if jq empty .claude-plugin/marketplace.json 2>/dev/null; then
    print_status $GREEN "  ✅ marketplace.json is valid"
else
    print_status $RED "  ❌ marketplace.json has syntax errors"
    ((ERRORS++))
fi

# Check all plugin.json files
for plugin_dir in plugins/*/; do
    if [ -d "$plugin_dir" ]; then
        plugin_name=$(basename "$plugin_dir")
        plugin_json="$plugin_dir/.claude-plugin/plugin.json"

        if [ -f "$plugin_json" ]; then
            if jq empty "$plugin_json" 2>/dev/null; then
                print_status $GREEN "  ✅ $plugin_name/plugin.json is valid"
            else
                print_status $RED "  ❌ $plugin_name/plugin.json has syntax errors"
                ((ERRORS++))
            fi
        else
            print_status $YELLOW "  ⚠️  $plugin_name missing plugin.json"
            ((WARNINGS++))
        fi
    fi
done

# Step 2: Run comprehensive validation
print_status $BLUE "\nStep 2/4: Running comprehensive plugin validation..."
if python scripts/validate-plugins.py --format json > validation-results.json 2>&1; then
    # Parse JSON results
    ERROR_COUNT=$(jq '[.[] | select(.severity == "error")] | length' validation-results.json 2>/dev/null || echo "0")
    WARNING_COUNT=$(jq '[.[] | select(.severity == "warning")] | length' validation-results.json 2>/dev/null || echo "0")

    if [ "$ERROR_COUNT" -eq 0 ]; then
        print_status $GREEN "  ✅ Comprehensive validation passed"
    else
        print_status $RED "  ❌ Found $ERROR_COUNT validation errors"
        ((ERRORS += ERROR_COUNT))
    fi

    if [ "$WARNING_COUNT" -gt 0 ]; then
        print_status $YELLOW "  ⚠️  Found $WARNING_COUNT warnings"
        ((WARNINGS += WARNING_COUNT))
    fi
else
    print_status $RED "  ❌ Comprehensive validation failed"
    ((ERRORS++))
fi

# Step 3: Build and validate generated files
print_status $BLUE "\nStep 3/4: Building marketplace and README..."
if python scripts/build-marketplace.py > /dev/null 2>&1; then
    print_status $GREEN "  ✅ Build completed successfully"

    # Validate generated marketplace again
    if python scripts/validate-plugins.py --marketplace .claude-plugin/marketplace.json > /dev/null 2>&1; then
        print_status $GREEN "  ✅ Generated marketplace is valid"
    else
        print_status $RED "  ❌ Generated marketplace validation failed"
        ((ERRORS++))
    fi
else
    print_status $RED "  ❌ Build failed"
    ((ERRORS++))
fi

# Step 4: Check for required files
print_status $BLUE "\nStep 4/4: Checking required files..."
REQUIRED_FILES=(".claude-plugin/marketplace.json" "scripts/build-marketplace.py" "scripts/validate-plugins.py")

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        print_status $GREEN "  ✅ $file exists"
    else
        print_status $RED "  ❌ $file is missing"
        ((ERRORS++))
    fi
done

# Summary
print_status $BLUE "\n" "=" * 50
print_status $BLUE "CI/CD Validation Summary"

if [ "$ERRORS" -eq 0 ]; then
    if [ "$WARNINGS" -eq 0 ]; then
        print_status $GREEN "🎉 All validations passed! Ready for deployment."
        exit 0
    else
        print_status $YELLOW "⚠️  All critical validations passed with $WARNINGS warnings."
        exit 0
    fi
else
    print_status $RED "❌ Validation failed with $ERRORS errors and $WARNINGS warnings."

    # Show error details if validation results exist
    if [ -f validation-results.json ]; then
        print_status $RED "\nError Details:"
        jq -r '.[] | select(.severity == "error") | "  ❌ \(.file): \(.message)"' validation-results.json
    fi

    exit 1
fi