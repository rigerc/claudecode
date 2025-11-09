---
name: Documentation Generator
description: Research and generate comprehensive documentation for projects, APIs, features, and code. Use when documentation needs to be created, updated, or reviewed. Always research using context7 and available tools before writing. Proactively suggest documentation for undocumented features. Save output as Markdown in the project's docs/ directory.
allowed-tools: Read, Write, Edit, Glob, Grep, WebFetch, WebSearch, Task, TodoWrite, mcp__context7__resolve-library-id, mcp__context7__get-library-docs
---

# Documentation Generator

## Overview

This skill researches, analyzes, and generates comprehensive documentation for software projects. It combines code analysis, library documentation research, and best practices to create clear, useful documentation that helps developers understand and use your code effectively.

## When to Use

Use this skill when:
- Creating documentation for new features or APIs
- Updating existing documentation that's outdated
- Writing API references, getting started guides, or tutorials
- Documenting undocumented code or features
- Creating comprehensive README files
- Generating technical documentation for end users
- Reviewing and improving existing documentation quality

## Core Workflow

### Phase 1: Research & Analysis

1. **Understand the Scope**
   - Identify what needs documentation
   - Determine the target audience (developers, end users, etc.)
   - Analyze existing documentation for gaps

2. **Code Analysis**
   - Use `Glob` to find relevant source files
   - Use `Grep` to search for key patterns, functions, and classes
   - Use `Read` to analyze implementation details
   - Identify undocumented features or unclear code

3. **External Research**
   - Use `context7` to get up-to-date documentation for libraries and frameworks
   - Use `WebSearch` to research best practices and examples
   - Look for similar implementations for reference

### Phase 2: Documentation Planning

1. **Create Documentation Structure**
   - Determine appropriate documentation type (API docs, tutorial, reference, etc.)
   - Plan sections and organization
   - Identify required examples and code snippets

2. **Set Up Output Location**
   - Create or use `docs/` directory for project documentation
   - Follow project's existing documentation structure
   - Use appropriate file naming conventions

### Phase 3: Content Generation

1. **Write Clear, Comprehensive Content**
   - Start with clear overview and purpose
   - Provide practical examples and use cases
   - Include code snippets with explanations
   - Add troubleshooting and FAQ sections when relevant

2. **Follow Best Practices**
   - Use clear, concise language
   - Include table of contents for long documents
   - Use proper markdown formatting
   - Add cross-references between related documents

3. **Review and Refine**
   - Ensure accuracy of technical details
   - Check for consistency with existing docs
   - Verify code examples work correctly
   - Get feedback from stakeholders if possible

## Documentation Types

### API Documentation
- Function/method signatures
- Parameter descriptions and types
- Return value specifications
- Error handling
- Usage examples
- Authentication/authorization requirements

### Getting Started Guides
- Prerequisites and setup
- Installation instructions
- Basic usage examples
- Common workflows
- Next steps and further reading

### Technical Reference
- Detailed parameter specifications
- Advanced configuration options
- Architecture overview
- Performance considerations
- Security notes

### Tutorials
- Step-by-step instructions
- Real-world examples
- Screenshots and diagrams (when applicable)
- Expected outcomes
- Troubleshooting tips

## Research Tools and Techniques

### Context7 Integration
```bash
# Resolve library ID first
mcp__context7__resolve-library-id "library-name"

# Get comprehensive documentation
mcp__context7__get-library-docs "/org/project" "specific-topic"
```

### Code Analysis Patterns
```bash
# Find all API endpoints
Grep pattern: "@app\.(get|post|put|delete)" glob: "*.py"

# Find undocumented functions
Grep pattern: "def \w+\(" glob: "*.py" output_mode: "files_with_matches"

# Search for configuration options
Grep pattern: "config|setting" glob: "*.yml,*.yaml,*.json"
```

### Documentation Gap Analysis
1. List all public APIs/functions
2. Check existing documentation coverage
3. Identify missing or outdated sections
4. Prioritize based on usage and importance

## File Organization

```
docs/
├── README.md                 # Main documentation index
├── getting-started.md        # Setup and basic usage
├── api/                      # API documentation
│   ├── overview.md
│   ├── endpoints.md
│   └── examples.md
├── tutorials/                # Step-by-step guides
│   ├── basic-usage.md
│   └── advanced-features.md
├── reference/                # Technical reference
│   ├── configuration.md
│   └── troubleshooting.md
└── examples/                 # Code examples
    ├── basic/
    └── advanced/
```

## Quality Standards

### Content Requirements
- **Accuracy**: All technical details must be correct
- **Completeness**: Cover all important aspects without overwhelming users
- **Clarity**: Use simple, direct language appropriate for the audience
- **Examples**: Include practical, working code examples
- **Consistency**: Follow established style and formatting conventions

### Formatting Standards
- Use proper markdown syntax
- Include table of contents for documents longer than 2000 words
- Use code blocks with language specification
- Add proper heading hierarchy (H1, H2, H3...)
- Include cross-references between related documents

### Review Checklist
- [ ] All code examples are tested and working
- [ ] Documentation matches current implementation
- [ ] Links and references are valid
- [ ] Spelling and grammar are correct
- [ ] Structure is logical and easy to navigate
- [ ] Examples cover common use cases

## Proactive Documentation

Always suggest documentation for:
- New features or APIs that lack documentation
- Complex algorithms or business logic
- Configuration options and environment variables
- Error handling and edge cases
- Performance characteristics and limitations
- Security considerations
- Integration with external services

## Templates and Examples

### API Documentation Template
```markdown
# [API/Feature Name]

## Overview
[Brief description of what this API does]

## Endpoint
[HTTP method and path]

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|

## Response Format
[Expected response structure]

## Examples
[Code examples with explanations]

## Error Handling
[Common errors and solutions]
```

### Getting Started Template
```markdown
# Getting Started with [Product/Feature]

## Prerequisites
[List of requirements]

## Installation
[Step-by-step setup instructions]

## Basic Usage
[Simple example to get started]

## Next Steps
[Links to more advanced topics]
```

## Common Workflows

### Documenting a New API
1. Analyze the API implementation
2. Test all endpoints and parameters
3. Document request/response formats
4. Create usage examples
5. Add error handling documentation
6. Review with API developers

### Creating User Guides
1. Identify user personas and goals
2. Map out user journeys
3. Create step-by-step instructions
4. Include screenshots and examples
5. Test with actual users if possible
6. Iterate based on feedback

### Updating Outdated Docs
1. Compare documentation with current implementation
2. Identify what has changed
3. Update content accordingly
4. Add new features and deprecated items
5. Verify all examples still work
6. Update version history

## Integration with Other Skills

This skill works well with:
- **technical-docs-writer**: For creating user-facing documentation
- **readme-writer**: For project README files
- **code-reviewer**: For identifying code that needs documentation

## Tips for Success

1. **Always research first** - Never assume how something works without verifying
2. **Think about the audience** - Tailor language and depth to user needs
3. **Use concrete examples** - Abstract concepts are easier to understand with real examples
4. **Keep it updated** - Documentation quickly becomes outdated if not maintained
5. **Get feedback** - Have actual users review documentation for clarity and completeness
6. **Be proactive** - Don't wait for users to ask for documentation that should obviously exist