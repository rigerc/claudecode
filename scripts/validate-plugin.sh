#!/bin/bash

# Plugin Validation Script for Claude Code Marketplace
# Validates plugin structure, metadata, and quality standards

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Validation results
VALIDATIONS_PASSED=0
VALIDATIONS_FAILED=0
VALIDATIONS_WARNING=0

# Logging functions
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
    ((VALIDATIONS_PASSED++))
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
    ((VALIDATIONS_FAILED++))
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
    ((VALIDATIONS_WARNING++))
}

# Usage information
usage() {
    echo "Usage: $0 <plugin-path>"
    echo "Example: $0 plugins/my-plugin"
    exit 1
}

# Check if plugin path is provided
if [[ $# -eq 0 ]]; then
    usage
fi

PLUGIN_PATH="$1"

# Check if plugin path exists
if [[ ! -d "$PLUGIN_PATH" ]]; then
    log_error "Plugin directory '$PLUGIN_PATH' does not exist"
    exit 1
fi

log_info "Validating plugin at: $PLUGIN_PATH"

# Validation functions

validate_plugin_json() {
    log_info "Validating plugin.json..."

    local plugin_json="$PLUGIN_PATH/.claude-plugin/plugin.json"

    if [[ ! -f "$plugin_json" ]]; then
        log_error "plugin.json not found at .claude-plugin/plugin.json"
        return 1
    fi

    # Check if it's valid JSON
    if ! python3 -m json.tool "$plugin_json" > /dev/null 2>&1; then
        log_error "plugin.json is not valid JSON"
        return 1
    fi

    # Check required fields
    local required_fields=("name" "version" "description" "author" "license")

    for field in "${required_fields[@]}"; do
        if ! jq -e ".$field" "$plugin_json" > /dev/null 2>&1; then
            log_error "Required field '$field' missing in plugin.json"
            return 1
        fi
    done

    # Check version format (semver)
    local version=$(jq -r '.version' "$plugin_json")
    if ! [[ "$version" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        log_warning "Version '$version' doesn't follow semantic versioning (x.y.z)"
    fi

    # Check if name is kebab-case
    local name=$(jq -r '.name' "$plugin_json")
    if ! [[ "$name" =~ ^[a-z0-9-]+$ ]]; then
        log_warning "Plugin name '$name' should use kebab-case"
    fi

    log_success "plugin.json is valid with all required fields"
}

validate_directory_structure() {
    log_info "Validating directory structure..."

    local required_dirs=(".claude-plugin")
    local plugin_name=$(basename "$PLUGIN_PATH")

    for dir in "${required_dirs[@]}"; do
        if [[ ! -d "$PLUGIN_PATH/$dir" ]]; then
            log_error "Required directory '$dir' not found"
            return 1
        fi
    done

    # Check for plugin.json in correct location
    if [[ ! -f "$PLUGIN_PATH/.claude-plugin/plugin.json" ]]; then
        log_error "plugin.json not found in .claude-plugin directory"
        return 1
    fi

    log_success "Directory structure is valid"
}

validate_readme() {
    log_info "Validating README.md..."

    local readme="$PLUGIN_PATH/README.md"

    if [[ ! -f "$readme" ]]; then
        log_error "README.md not found"
        return 1
    fi

    # Check if README has minimum content
    local readme_size=$(stat -f%z "$readme" 2>/dev/null || stat -c%s "$readme" 2>/dev/null || echo "0")
    if [[ "$readme_size" -lt 500 ]]; then
        log_warning "README.md seems too short (< 500 characters)"
    fi

    # Check for common sections
    local required_sections=("## Overview" "## Installation" "## Usage")

    for section in "${required_sections[@]}"; do
        if ! grep -q "$section" "$readme"; then
            log_warning "README.md missing section: $section"
        fi
    done

    log_success "README.md exists and has content"
}

validate_license() {
    log_info "Validating license..."

    local license_files=("LICENSE" "LICENSE.md" "LICENSE.txt")
    local license_found=false

    for license_file in "${license_files[@]}"; do
        if [[ -f "$PLUGIN_PATH/$license_file" ]]; then
            license_found=true
            break
        fi
    done

    if [[ "$license_found" == false ]]; then
        log_error "No license file found (LICENSE, LICENSE.md, or LICENSE.txt)"
        return 1
    fi

    log_success "License file found"
}

validate_components() {
    log_info "Validating plugin components..."

    local plugin_json="$PLUGIN_PATH/.claude-plugin/plugin.json"
    local has_components=false

    # Check if components section exists and has items
    if jq -e '.components' "$plugin_json" > /dev/null 2>&1; then
        local component_types=("commands" "skills" "agents" "hooks")

        for component_type in "${component_types[@]}"; do
            local count=$(jq ".components.$component_type | length // 0" "$plugin_json" 2>/dev/null || echo "0")
            if [[ "$count" -gt 0 ]]; then
                has_components=true
                log_info "Found $count $component_type"

                # Validate component files exist
                local component_dir="$PLUGIN_PATH/${component_type}"
                if [[ "$component_type" == "skills" ]]; then
                    component_dir="$PLUGIN_PATH/skills"
                fi

                if [[ -d "$component_dir" ]]; then
                    local file_count=$(find "$component_dir" -name "*.md" -o -name "SKILL.md" | wc -l)
                    if [[ "$file_count" -eq 0 ]]; then
                        log_warning "$component_type directory exists but contains no files"
                    fi
                fi
            fi
        done
    fi

    if [[ "$has_components" == false ]]; then
        log_warning "No components found in plugin.json"
    else
        log_success "Plugin components validated"
    fi
}

validate_dependencies() {
    log_info "Validating dependencies..."

    local plugin_json="$PLUGIN_PATH/.claude-plugin/plugin.json"

    # Check if dependencies section exists
    if jq -e '.dependencies' "$plugin_json" > /dev/null 2>&1; then
        local claude_code_version=$(jq -r '.dependencies["claude-code"] // "unknown"' "$plugin_json")

        if [[ "$claude_code_version" != "unknown" ]]; then
            log_success "Claude Code dependency specified: $claude_code_version"
        else
            log_warning "Claude Code version dependency not specified"
        fi
    else
        log_warning "No dependencies section found in plugin.json"
    fi
}

check_security_issues() {
    log_info "Checking for security issues..."

    # Check for common security issues in plugin files
    local security_issues=0

    # Check for hardcoded credentials in shell scripts
    if find "$PLUGIN_PATH" -name "*.sh" -exec grep -l "password\|secret\|token\|key" {} \; 2>/dev/null | head -1 | grep -q .; then
        log_warning "Potential hardcoded credentials found in shell scripts"
        ((security_issues++))
    fi

    # Check for executable files in suspicious locations
    if find "$PLUGIN_PATH" -name "*.exe" -o -name "*.bin" | head -1 | grep -q .; then
        log_warning "Executable files found - ensure they are safe"
        ((security_issues++))
    fi

    # Check for network connections in scripts
    if find "$PLUGIN_PATH" -name "*.sh" -exec grep -l "curl\|wget\|nc\|netcat" {} \; 2>/dev/null | head -1 | grep -q .; then
        log_warning "Network operations found in scripts - ensure they are safe"
        ((security_issues++))
    fi

    if [[ "$security_issues" -eq 0 ]]; then
        log_success "No obvious security issues found"
    fi
}

validate_metadata_consistency() {
    log_info "Validating metadata consistency..."

    local plugin_json="$PLUGIN_PATH/.claude-plugin/plugin.json"
    local plugin_name=$(jq -r '.name' "$plugin_json")
    local directory_name=$(basename "$PLUGIN_PATH")

    # Check if plugin name matches directory name
    if [[ "$plugin_name" != "$directory_name" ]]; then
        log_warning "Plugin name '$plugin_name' doesn't match directory name '$directory_name'"
    fi

    # Check if category is valid
    local category=$(jq -r '.category // ""' "$plugin_json")
    local valid_categories=("Development" "Documentation" "Agents" "Media" "Other")

    if [[ -n "$category" ]] && [[ ! " ${valid_categories[@]} " =~ " $category " ]]; then
        log_warning "Category '$category' is not a standard category"
    fi

    log_success "Metadata consistency validated"
}

# Main validation function
main() {
    echo "========================================"
    echo "🔍 Claude Code Plugin Validator"
    echo "========================================"
    echo

    # Run all validations
    validate_plugin_json
    validate_directory_structure
    validate_readme
    validate_license
    validate_components
    validate_dependencies
    check_security_issues
    validate_metadata_consistency

    echo
    echo "========================================"
    echo "📊 Validation Results"
    echo "========================================"
    echo -e "✅ Passed:  $VALIDATIONS_PASSED"
    echo -e "⚠️  Warnings: $VALIDATIONS_WARNING"
    echo -e "❌ Failed:  $VALIDATIONS_FAILED"
    echo

    if [[ "$VALIDATIONS_FAILED" -gt 0 ]]; then
        echo -e "${RED}❌ Plugin validation failed!${NC}"
        echo "Please fix the errors before submitting."
        exit 1
    elif [[ "$VALIDATIONS_WARNING" -gt 0 ]]; then
        echo -e "${YELLOW}⚠️  Plugin validation passed with warnings${NC}"
        echo "Consider addressing the warnings for better quality."
        exit 0
    else
        echo -e "${GREEN}✅ Plugin validation passed successfully!${NC}"
        echo "Your plugin is ready for submission."
        exit 0
    fi
}

# Run main function
main "$@"