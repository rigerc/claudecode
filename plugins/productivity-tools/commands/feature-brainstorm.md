---
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, mcp__context7__resolve-library-id, mcp__context7__get-library-docs
description: Analyze the current project and suggest improvements to features or new features that are in line with the project's goals. The suggestions should be high-level, realistic, be in the context of a personal or open source project and without code.
---

# Feature Brainstorm

## Usage

```
/feature-brainstorm [focus-area]
```

## Parameters

- **focus-area** (optional): Specific area to focus on (e.g., "performance", "ux", "architecture", "security", "documentation")

## Description

This command analyzes your current project to provide thoughtful suggestions for:
- Feature improvements and enhancements
- New feature ideas aligned with project goals
- User experience improvements
- Technical debt reduction opportunities
- Architecture and performance optimizations

The analysis considers:
- Project type and technology stack
- Current codebase structure and patterns
- Best practices for the specific domain
- Realistic implementation complexity
- Personal/open source project constraints

## Implementation

1. **Project Analysis Phase**
   - Detect project type and main technologies
   - Analyze project structure and architecture
   - Identify existing features and patterns
   - Review configuration files and dependencies

2. **Context Understanding**
   - Read README and documentation if available
   - Analyze package.json, go.mod, requirements.txt, etc.
   - Identify project goals and target audience
   - Understand current development stage

3. **Feature Brainstorming**
   - Generate improvement suggestions based on project type
   - Suggest new features that align with project goals
   - Consider user experience enhancements
   - Propose technical improvements

4. **Prioritization Framework**
   - Categorize suggestions by impact vs. effort
   - Consider personal/open source project constraints
   - Focus on realistic, achievable improvements
   - Highlight quick wins vs. long-term investments

## Suggestion Categories

### User Experience & Interface
- Workflow improvements
- Accessibility enhancements
- Mobile responsiveness
- Performance optimizations
- User onboarding improvements

### Technical Enhancements
- Code quality and maintainability
- Performance and scalability
- Security improvements
- Testing and reliability
- Documentation and developer experience

### Feature Expansions
- Core feature enhancements
- Integration opportunities
- Automation possibilities
- Data analysis and insights
- Community and collaboration features

## Examples

```bash
# General feature brainstorming for the entire project
/feature-brainstorm

# Focus on performance improvements
/feature-brainstorm performance

# Focus on user experience
/feature-brainstorm ux

# Focus on architecture improvements
/feature-brainstorm architecture
```

## Output Format

The command provides:
- **Project Summary**: Brief overview of project type and goals
- **Current Strengths**: What the project does well
- **Improvement Opportunities**: Categorized suggestions with:
  - High-level description
  - Impact vs. effort assessment
  - Implementation considerations
  - User benefit description
- **Quick Wins**: Low-effort, high-impact suggestions
- **Long-term Vision**: Strategic improvement ideas

## Notes

- Suggestions are intentionally high-level and strategic
- No code implementations provided (as requested)
- Focus is on realistic improvements for personal/open source projects
- Considerations include resource constraints and maintainability
- All suggestions are context-aware and project-specific

## Best Practices

- Use this command early in project planning phases
- Combine with `/code-review` for technical implementation details
- Re-run periodically as project evolves
- Consider creating todo items from high-priority suggestions
- Use suggestions to inform roadmap planning