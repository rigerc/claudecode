#!/bin/bash

# Add new extension with one command

set -euo pipefail

usage() {
    echo "Usage: $0 <type> <name> [description]"
    echo ""
    echo "Types:"
    echo "  command    - Add a new slash command"
    echo "  skill      - Add a new skill"
    echo "  agent      - Add a new agent"
    echo "  hook       - Add a new hook"
    echo ""
    echo "Examples:"
    echo "  $0 command deploy \"Deploy application to production\""
    echo "  $0 skill database \"Database management and optimization\""
    echo "  $0 agent security \"Security analysis and vulnerability assessment\""
    exit 1
}

if [[ $# -lt 2 ]]; then
    usage
fi

TYPE="$1"
NAME="$2"
DESCRIPTION="${3:-New $TYPE extension}"

# Validate type
case "$TYPE" in
    command|skill|agent|hook)
        ;;
    *)
        echo "❌ Invalid type: $TYPE"
        usage
        ;;
esac

# Normalize name (kebab-case)
NORMALIZED_NAME=$(echo "$NAME" | sed 's/[^a-zA-Z0-9]/-/g' | tr '[:upper:]' '[:lower:]' | sed 's/--*/-/g' | sed 's/^-\|-$//g')

echo "🚀 Adding $TYPE: $NORMALIZED_NAME"
echo "📝 Description: $DESCRIPTION"

case "$TYPE" in
    command)
        COMMAND_DIR=".claude/commands"
        COMMAND_FILE="$COMMAND_DIR/$NORMALIZED_NAME.md"

        mkdir -p "$COMMAND_DIR"

        cat > "$COMMAND_FILE" << EOF
# $NAME

$DESCRIPTION

## Usage
/$NORMALIZED_NAME [args]

## Description
Detailed description of what this command does...

## Examples
\`\`\`bash
/$NORMALIZED_NAME --help
\`\`\`
EOF

        echo "✅ Created command: $COMMAND_FILE"
        ;;

    skill)
        SKILL_DIR=".claude/skills/$NORMALIZED_NAME"
        SKILL_FILE="$SKILL_DIR/SKILL.md"

        mkdir -p "$SKILL_DIR"

        cat > "$SKILL_FILE" << EOF
# $NAME

$DESCRIPTION

## Usage
Use this skill when [describe when to use this skill].

## Capabilities
- [Capability 1]
- [Capability 2]
- [Capability 3]

## Examples
\`\`\`
Example usage...
\`\`\`
EOF

        echo "✅ Created skill: $SKILL_FILE"
        ;;

    agent)
        AGENT_DIR=".claude/agents"
        AGENT_FILE="$AGENT_DIR/$NORMALIZED_NAME.md"

        mkdir -p "$AGENT_DIR"

        cat > "$AGENT_FILE" << EOF
# $NAME

$DESCRIPTION

## Expertise
- [Area of expertise 1]
- [Area of expertise 2]
- [Area of expertise 3]

## Usage
Use this agent for [specific tasks and scenarios].

## Examples
\`\`\`
Example usage...
\`\`\`
EOF

        echo "✅ Created agent: $AGENT_FILE"
        ;;

    hook)
        HOOK_DIR=".claude/hooks"
        HOOK_FILE="$HOOK_DIR/$NORMALIZED_NAME.md"

        mkdir -p "$HOOK_DIR"

        cat > "$HOOK_FILE" << EOF
# $NAME

$DESCRIPTION

## Trigger
This hook triggers when [describe trigger condition].

## Actions
- [Action 1]
- [Action 2]
- [Action 3]

## Configuration
\`\`\`json
{
  "enabled": true,
  "options": {}
}
\`\`\`
EOF

        echo "✅ Created hook: $HOOK_FILE"
        ;;
esac

echo
echo "🎉 Extension created successfully!"
echo
echo "📝 Next steps:"
echo "   1. Edit the generated file to add your specific implementation"
echo "   2. Run 'make generate' to update the marketplace"
echo "   3. Or run 'make watch' to auto-regenerate on changes"
echo
if command -v make &> /dev/null; then
    echo "🔄 Regenerating marketplace..."
    make generate
    echo "✅ Marketplace updated!"
else
    echo "💡 Run 'python3 scripts/generate-marketplace.py' to update marketplace"
fi