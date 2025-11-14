---
description: Find SKILL.MD files with detailed-guide.md references and split long reference files into multiple focused files
argument-hint: "[skill-path-or-name]"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Split Skill References

This command helps you optimize skill reference files by finding SKILL.MD files that reference `detailed-guide.md` and splitting overly long reference files into multiple focused files.

## Process:
1. Find all SKILL.MD files in the codebase
2. Check which ones reference `detailed-guide.md`
3. Read those reference files to assess length and structure
4. If files are overly long (>2000 lines or contain multiple distinct topics), split them into:
   - Quick reference guide
   - Detailed usage examples
   - API reference
   - Troubleshooting guide
5. Update SKILL.MD files to reference the new split files

## Usage:
- **Without arguments**: Process all SKILL.MD files in the codebase
- **With skill path**: Focus on a specific skill directory or file

Let me start by finding all SKILL.MD files and checking their detailed-usage.md references.

# Find all SKILL.MD files
$SKILL_FILES = $(find . -name "SKILL.md" -type f)

# Check each SKILL.md for detailed-guide.md references
for skill_file in $SKILL_FILES; do
    echo "Checking: $skill_file"

    # Look for detailed-guide.md references
    if grep -q "detailed-guide\.md" "$skill_file"; then
        echo "  -> Found detailed-guide.md reference"

        # Extract the path to detailed-guide.md
        detailed_usaguidege_path=$(dirname "$skill_file")/$(grep -o "detailed-guide\.md" "$skill_file" | head -1)

        if [ -f "$detailed_guide_path" ]; then
            # Check file length
            line_count=$(wc -l < "$detailed_guide_path")
            echo "  -> detailed-guide.md has $line_count lines"

            if [ $line_count -gt 2000 ]; then
                echo "  -> RECOMMEND: Split this file (too long)"
            elif [ $line_count -gt 1000 ]; then
                echo "  -> CONSIDER: Split this file (moderately long)"
            else
                echo "  -> OK: File length is manageable"
            fi
        else
            echo "  -> WARNING: detailed-usage.md referenced but file not found"
        fi
    else
        echo "  -> No detailed-usage.md reference found"
    fi
    echo ""
done

Would you like me to proceed with splitting any files that are flagged as too long?