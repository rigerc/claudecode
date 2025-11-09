---
description: Command for using the generate-documentation skill
argument-hint: [target] [type] [output-dir]
allowed-tools: Read, Write, Edit, Glob, Grep, WebFetch, WebSearch, Task, TodoWrite, mcp__context7__resolve-library-id, mcp__context7__get-library-docs
---

# Create Documentation

Use the generate-documentation skill to create comprehensive documentation for the specified target.

## Parameters
- **target** (required): The feature, API, component, or code to document
- **type** (optional): Documentation type (api, getting-started, tutorial, reference, overview). Defaults to "overview"
- **output-dir** (optional): Output directory for documentation. Defaults to "docs/"

## Instructions

1. **Analyze the target**:
   - If `$1` is a file path, analyze that file and related components
   - If `$1` is a feature name, search for relevant code and implementation
   - Use `Glob` and `Grep` to find all related files and patterns

2. **Determine documentation type**:
   - If `$2` is specified, use that type
   - If no type specified, analyze the target to determine the most appropriate documentation type

3. **Research and analyze**:
   - Read the relevant source files
   - Use context7 to research any libraries or frameworks used
   - Identify undocumented features or unclear code
   - Look for existing documentation to understand gaps

4. **Generate documentation**:
   - Use the appropriate template from the generate-documentation skill
   - Create comprehensive, accurate documentation
   - Include practical examples and code snippets
   - Save to specified output directory (`$3` or "docs/")

5. **Follow best practices**:
   - Ensure technical accuracy
   - Include clear examples
   - Add troubleshooting information when relevant
   - Use proper markdown formatting

## Examples

```bash
# Create API documentation for a specific endpoint
/create-documentation src/api/user.js api

# Create getting started guide for the entire project
/create-documentation . getting-started docs/guides

# Create tutorial for a specific feature
/create-documentation authentication tutorial docs/tutorials
```

## Output

Documentation will be generated and saved to the specified location with:
- Clear structure and organization
- Comprehensive coverage of the target
- Practical examples and code snippets
- Links to related documentation
- Troubleshooting guidance where appropriate