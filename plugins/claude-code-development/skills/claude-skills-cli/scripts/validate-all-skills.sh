#!/bin/bash

# Validate all skills in the project
# This script finds all directories containing a SKILL.md file and validates them

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counter for results
TOTAL=0
PASSED=0
FAILED=0

echo -e "${BLUE}🔍 Finding all skill directories...${NC}"
echo

# Find all directories containing SKILL.md files
# Start from current working directory and look for skills directories
find . -type d -name "skills" | while read skills_dir; do
    echo -e "${YELLOW}📁 Checking skills directory: $skills_dir${NC}"
    
    # Find all subdirectories containing SKILL.md
    find "$skills_dir" -maxdepth 2 -type f -name "SKILL.md" | while read skill_file; do
        skill_dir=$(dirname "$skill_file")
        skill_name=$(basename "$skill_dir")
        
        echo -e "${BLUE}🔧 Validating skill: $skill_name${NC}"
        echo "   Path: $skill_dir"
        
        # Run claude-skill-cli validate
        if npx claude-skill-cli validate "$skill_dir"; then
            echo -e "${GREEN}✅ Validation passed for: $skill_name${NC}"
            ((PASSED++))
        else
            echo -e "${RED}❌ Validation failed for: $skill_name${NC}"
            ((FAILED++))
        fi
        
        ((TOTAL++))
        echo "----------------------------------------"
    done
done

echo
echo -e "${BLUE}📊 Validation Summary:${NC}"
echo -e "   Total skills: $TOTAL"
echo -e "${GREEN}   Passed: $PASSED${NC}"
echo -e "${RED}   Failed: $FAILED${NC}"

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 All skills validated successfully!${NC}"
    exit 0
else
    echo -e "${RED}💥 Some skills failed validation${NC}"
    exit 1
fi