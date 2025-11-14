# Development Process

Step-by-step workflow for creating effective Claude Skills.

## Workflow

### 1. Gather & Research

**Determine if research is needed**:
- Skip research if user provides documentation or references
- Skip research if comprehensive docs/ directory already exists with relevant information
- Proceed with research if domain knowledge is missing or incomplete

**Research Phase** (only if needed):
- Use the `documentation-generation:library-researcher` skill or MCP tools to understand the technical ecosystem
- Research available APIs, frameworks, libraries, and established patterns
- Study official documentation and best practices
- Identify common workflows and use cases in the domain
- Look for existing solutions, tools, and community standards

**Gather Usage Examples**:
- Collect 3-5 concrete examples of how you've used this knowledge
- Save conversation snippets showing the repeated context
- Document the specific questions or tasks that triggered the need
- Note the exact information you provided each time
- Identify common patterns across usage

**Output**: Domain research documentation (if needed) + collection of real usage examples

### 2. Plan

Decide information hierarchy:

**SKILL.md (Level 2)** - Core patterns only:

- What the skill does
- When to use it
- Essential structure/commands
- Links to references

**references/ (Level 3)** - Detailed docs:

- Complete API documentation
- Detailed examples and tutorials
- Background and theory
- Edge cases and troubleshooting

**scripts/ (Level 3)** - Deterministic operations:

- Validation logic
- Code generation
- File transformations
- Data processing

**assets/ (Level 3)** - Static resources:

- Templates
- Configuration files
- Images and diagrams

### 34. Structure

#### Determine Skill Location

Before creating the directory, ask the user where to save the skill:

1. **Project** (`.claude/skills/`) - Available only in current project
2. **User** (`~/.claude/skills/`) - Available globally across all
   projects
3. **Plugin** (`plugins/<plugin>/skills/`) - Only available if the
   current project contains `.claude-plugin/marketplace.json`

Use the AskUserQuestion tool to present these options.

#### Create Directory Structure

Based on the user's choice, create the directory structure:

```bash
# For project location
mkdir -p .claude/skills/my-skill/{references,scripts,assets}
touch .claude/skills/my-skill/SKILL.md

# For user location
mkdir -p ~/.claude/skills/my-skill/{references,scripts,assets}
touch ~/.claude/skills/my-skill/SKILL.md

# For plugin location (replace <plugin-name> with actual plugin name)
mkdir -p ./plugins/<plugin-name>/skills/my-skill/{references,scripts,assets}
touch ./plugins/<plugin-name>/skills/my-skill/SKILL.md
```

### 4. Write

#### Write Description First

The description is critical for skill discovery. Format:

```
[Domain/Context] [operations/capabilities]. Use when [trigger scenarios].
```

Examples:

- ✅ "PostgreSQL schema and query patterns. Use when designing
  databases, writing queries, or optimizing performance."
- ✅ "Next.js 14 App Router conventions. Use when building Next.js
  apps, configuring routes, or implementing server components."
- ❌ "A skill for databases" (too vague)
- ❌ "This skill helps you work with PostgreSQL databases" (second
  person)

Target: <200 chars for optimal Level 1 efficiency

#### Write SKILL.md Body

Structure:

1. **Brief intro** (1-2 lines) - What this skill provides
2. **When to use** (3-5 bullets) - Triggering scenarios
3. **Core patterns** (3-5 sections) - Essential knowledge
4. **Links to references** - Point to detailed docs

Guidelines:

- Use imperative voice ("Use X for Y", not "You should use X")
- Provide concrete examples, not abstract concepts
- Keep it scannable with clear headings
- Target ~50 lines, max ~150 lines
- Link liberally to references/

#### Write References

No size limits - be as detailed as needed:

- Use descriptive filenames (api-endpoints.md, not reference.md)
- Structure with clear headings
- Include code examples
- Cover edge cases
- Provide context and rationale

### 6. Enhance

Add progressive enhancements:

**Scripts** - When operations are:

- Deterministic (same input = same output)
- Complex (would require Claude to generate code)
- Reusable (used frequently)

Examples: validators, code generators, formatters

**Assets** - When you need:

- Templates (boilerplate code, config files)
- Static files (images, data files)
- Resources that shouldn't be loaded into context

### 6. Validate & Iterate

**Validation** (REQUIRED after creation):

Use the `claude-skills-cli` skill to validate the skill structure:

```bash
# Validate with claude-skills-cli skill
```

The skill will:

- Check YAML frontmatter syntax
- Verify file structure
- Validate description meets guidelines (<200 chars, clear trigger
  scenarios)
- Ensure reference links are valid

Fix any validation errors before testing.

**Testing**:

- Start a new conversation
- Trigger the skill naturally (don't force it)
- Observe if Claude loads it appropriately
- Check if the content is helpful and sufficient

**Refining**:

- If skill loads too often → Make description more specific
- If skill never loads → Add trigger keywords to description
- If Claude asks for info that's in references → Add links in SKILL.md
- If SKILL.md feels bloated → Move content to references
- If you're repeating the same complex operation → Create a script

**Iteration Cycle**:

1. Use skill in real conversations
2. Note friction points and gaps
3. Refactor structure and content
4. Test again

## Common Pitfalls

**Starting Too Big**

- ❌ Writing 500 lines before testing
- ✅ Start with 30-line SKILL.md, iterate

**Generic Descriptions**

- ❌ "Helps with coding tasks"
- ✅ "React hooks patterns and performance optimization. Use when
  building React components or debugging re-renders."

**Bloated SKILL.md**

- ❌ Including complete API docs in SKILL.md
- ✅ Core patterns in SKILL.md, full docs in references/

**Missing Triggers**

- ❌ Description with no "Use when..." clause
- ✅ Clear triggering scenarios in description

**Second Person Voice**

- ❌ "You should use this pattern when you need..."
- ✅ "Use this pattern when..."

## Success Criteria

A well-designed skill:

- ✅ Loads automatically when relevant (no manual triggering)
- ✅ Provides exactly the context needed (not too much, not too
  little)
- ✅ Improves with each conversation (you notice missing pieces)
- ✅ Saves you time (no more re-explaining the same concepts)

## Tips

- **Start minimal**: Better to add than to remove
- **Test early**: Don't perfect in isolation
- **Use real examples**: Concrete beats abstract
- **Trust progressive disclosure**: Claude will ask for references
  when needed
- **Iterate based on usage**: Let real conversations drive refinement
- **Skip packaging**: Only package skills when sharing with others or
  uploading to Claude.ai - local skills work directly from the
  filesystem
