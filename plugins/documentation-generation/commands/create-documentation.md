---
description: Command for using the generate-documentation skill
argument-hint: "description"
allowed-tools: Read, Write, Edit, Glob, Grep, WebFetch, WebSearch, Task, TodoWrite, mcp__context7__resolve-library-id, mcp__context7__get-library-docs
---

# Create Documentation

Use the generate-documentation skill to create comprehensive documentation based on a description.

## Parameters
- **description** (required): Description of what to document (feature, API, component, code, or topic)

## Instructions

1. **Analyze the description**:
   - Parse the description to understand what needs to be documented
   - If it's a file path, analyze that file and related components
   - If it's a feature name, search for relevant code and implementation
   - If it's a topic, research the subject and find relevant code/examples
   - Use `Glob` and `Grep` to find all related files and patterns

2. **Determine documentation type**:
   - Analyze the description to determine the most appropriate documentation type
   - Choose from: api, getting-started, tutorial, reference, overview
   - Default to "overview" if type is unclear

3. **Research and analyze**:
   - Read the relevant source files if applicable
   - Use context7 to research any libraries or frameworks used
   - Identify undocumented features or unclear code
   - Look for existing documentation to understand gaps
   - Search for examples and best practices

4. **Confirm library/framework identification**:
   - If a library or framework is identified during research, ask for user confirmation before proceeding
   - Present the identified library/framework and briefly explain why it was selected
   - Wait for user confirmation before continuing to documentation generation
   - If user identifies a different library/framework, proceed with their selection

5. **Generate documentation**:
   - Use the appropriate template from the generate-documentation skill
   - Create comprehensive, accurate documentation
   - Include practical examples and code snippets
   - Save to "docs/" directory

6. **Follow best practices**:
   - Ensure technical accuracy
   - Include clear examples
   - Add troubleshooting information when relevant
   - Use proper markdown formatting

## Examples

```bash
# Document a specific API endpoint
/create-documentation "user authentication API endpoints"

# Create getting started guide for a framework
/create-documentation "React hooks getting started guide"

# Document a feature
/create-documentation "file upload functionality"

# Create tutorial for a tool
/create-documentation "Docker container deployment tutorial"

# Document a library or package
/create-documentation "Express.js middleware patterns"

# Create overview documentation
/create-documentation "microservices architecture overview"
```

## Output

Documentation will be generated and saved to the specified location with:
- Clear structure and organization
- Comprehensive coverage of the target
- Practical examples and code snippets
- Links to related documentation
- Troubleshooting guidance where appropriate