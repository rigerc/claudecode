# Progressive Disclosure Architecture

## Overview
Claude Skills use a 3-level progressive disclosure system to optimize token usage and ensure skills load efficiently.

## Levels

### Level 1: Metadata (Always Loaded)
- **Content**: YAML frontmatter with name, description, allowed-tools
- **Size**: <200 characters optimal (~30 tokens)
- **Purpose**: Skill discovery and basic activation decisions
- **Always in context**: Claude reads this for every available skill

### Level 2: Core Instructions (Loaded on Activation)
- **Content**: Main SKILL.md body with instructions and examples
- **Size**: ~50 lines target, 150 max
- **Purpose**: Primary guidance for using the skill
- **Loaded when**: Skill matches user request and activates

### Level 3: Supporting Files (Loaded on Demand)
- **Content**: references/, scripts/, templates/, assets/
- **Size**: Unlimited
- **Purpose**: Detailed documentation, utilities, examples
- **Loaded when**: Referenced from Level 2 content

## Validation Rules

### Level 1 Constraints
- Description length: <200 characters optimal
- Must include trigger keywords
- Should specify when to use the skill
- Name must be kebab-case and match directory

### Level 2 Constraints
- Line count: ~50 target, 150 maximum
- Word count: <1000 recommended, <5000 max
- Token budget: <6500 tokens
- Code blocks: 1-2 optimal
- Sections: 3-5 recommended

### Level 3 Constraints
- All referenced files must exist
- No orphaned files (files not referenced from Level 2)
- Nesting depth analysis
- Progressive disclosure structure compliance

## Best Practices

1. **Keep Level 1 focused**: Metadata should be discovery-oriented
2. **Optimize Level 2**: Core instructions should be concise but complete
3. **Use Level 3 extensively**: Move details, examples, and references here
4. **Reference strategically**: Only load supporting files when needed
5. **Validate frequently**: Use claude-skills-cli validate to check compliance