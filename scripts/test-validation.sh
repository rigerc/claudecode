#!/bin/bash

# Simple test to validate the marketplace structure

echo "Testing marketplace validation..."

# Test 1: Check if marketplace.json is valid
echo "1. Testing marketplace.json..."
if python3 -m json.tool .claude-plugin/marketplace.json > /dev/null 2>&1; then
    echo "✅ marketplace.json is valid"
else
    echo "❌ marketplace.json is invalid"
    exit 1
fi

# Test 2: Check if plugins exist
echo "2. Testing plugin directories..."
plugins=($(jq -r '.plugins[].name' .claude-plugin/marketplace.json))
echo "Found plugins: ${plugins[*]}"

for plugin in "${plugins[@]}"; do
    plugin_path="plugins/$plugin"
    if [[ -d "$plugin_path" ]]; then
        echo "✅ $plugin directory exists"
    else
        echo "❌ $plugin directory missing"
    fi
done

# Test 3: Check basic plugin structure
echo "3. Testing plugin structure..."
for plugin in "${plugins[@]}"; do
    plugin_path="plugins/$plugin"
    manifest_path="$plugin_path/.claude-plugin/plugin.json"
    readme_path="$plugin_path/README.md"

    if [[ -f "$manifest_path" ]]; then
        echo "✅ $plugin has plugin.json"
    else
        echo "❌ $plugin missing plugin.json"
    fi

    if [[ -f "$readme_path" ]]; then
        echo "✅ $plugin has README.md"
    else
        echo "❌ $plugin missing README.md"
    fi
done

echo "Validation complete!"