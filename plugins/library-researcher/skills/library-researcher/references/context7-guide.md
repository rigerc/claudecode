# Context7 Integration Guide

This guide explains how to effectively use Context7 tools for library research.

## Context7 Tools Overview

The Library Researcher skill integrates with Context7 MCP tools to provide comprehensive library documentation.

### Available Tools

1. **mcp__context7__resolve-library-id**
   - **Purpose**: Convert library names to Context7-compatible IDs
   - **Usage**: First step in any library research
   - **Input**: Library name (e.g., "react", "express", "tensorflow")
   - **Output**: Context7 library ID with confidence score

2. **mcp__context7__get-library-docs**
   - **Purpose**: Retrieve comprehensive library documentation
   - **Usage**: After resolving library ID
   - **Input**: Context7 library ID, optional topic focus
   - **Output**: Detailed documentation with examples and API reference

## Research Workflow

### Step 1: Library Resolution

Always start by resolving the library name to get the correct Context7 ID:

```javascript
// Example: Research React
const result = await mcp__context7__resolve-library-id("react");
// Returns: { libraryId: "/facebook/react", confidence: 0.95, description: "..." }
```

**Best Practices**:
- Try multiple variations if first attempt fails
- Use official names when possible
- Consider alternative names (e.g., "nodejs" vs "node")

### Step 2: Documentation Retrieval

Once you have the library ID, retrieve documentation:

```javascript
// General documentation
const docs = await mcp__context7__get-library-docs("/facebook/react");

// Focused documentation
const apiDocs = await mcp__context7__get-library-docs("/facebook/react", "api,hooks");

// Version-specific documentation
const v18Docs = await mcp__context7__get-library-docs("/facebook/react/v18.2.0", "migration");
```

**Topic Focus Options**:
- "setup", "getting-started" - Installation and basic usage
- "api", "reference" - API documentation
- "examples", "tutorials" - Code examples and guides
- "performance", "optimization" - Performance characteristics
- "migration", "upgrading" - Version migration guides

### Step 3: Analysis and Synthesis

Process the retrieved documentation to extract key insights:

1. **Core Concepts**: Main principles and architecture
2. **API Overview**: Essential functions and classes
3. **Usage Patterns**: Common implementation approaches
4. **Best Practices**: Recommended patterns and pitfalls
5. **Integration**: How it works with other tools

## Advanced Context7 Usage

### Multiple Library Research

When comparing libraries, research each one separately:

```javascript
// Research both Express and FastAPI for comparison
const expressId = await mcp__context7__resolve-library-id("express");
const fastapiId = await mcp__context7__resolve-library-id("fastapi");

const expressDocs = await mcp__context7__get-library-docs(expressId.libraryId, "api,performance");
const fastapiDocs = await mcp__context7__get-library-docs(fastapiId.libraryId, "api,performance");
```

### Ecosystem Research

Research related libraries to understand the full ecosystem:

```javascript
// Research React ecosystem
const reactId = await mcp__context7__resolve-library-id("react");
const reduxId = await mcp__context7__resolve-library-id("redux");
const reactRouterId = await mcp__context7__resolve-library-id("react-router");

// Get comprehensive understanding
const reactDocs = await mcp__context7__get-library-docs(reactId.libraryId, "state-management");
const reduxDocs = await mcp__context7__get-library-docs(reduxId.libraryId, "integration");
```

### Version-Specific Research

Target specific versions for migration research:

```javascript
// Research React v18 migration
const v18Docs = await mcp__context7__get-library-docs("/facebook/react/v18.0.0", "migration,changes");

// Compare with older version
const v17Docs = await mcp__context7__get-library-docs("/facebook/react/v17.0.2", "api");
```

## Error Handling and Fallbacks

### Library Not Found

When a library isn't found in Context7:

```javascript
try {
  const result = await mcp__context7__resolve-library-id(libraryName);
  if (result.confidence < 0.5) {
    // Low confidence - try alternatives
    const alternatives = [`${libraryName}js`, `node-${libraryName}`, libraryName.toLowerCase()];
    // Try each alternative
  }
} catch (error) {
  // Fallback to web search for official documentation
  const webResults = await WebSearch(`${libraryName} official documentation`);
}
```

### Documentation Quality Issues

When documentation quality is low:

1. **Cross-reference with web search**
2. **Check library's official website**
3. **Look for community tutorials**
4. **Examine GitHub repository documentation**

## Context7 Library Database Coverage

### Well-Supported Categories

- **Frontend Frameworks**: React, Vue, Angular, Svelte
- **Backend Frameworks**: Express, Django, Flask, FastAPI
- **Databases**: PostgreSQL, MongoDB, MySQL, Redis
- **Development Tools**: Webpack, ESLint, Jest
- **Cloud Services**: AWS SDK, Google Cloud, Azure
- **Data Science**: TensorFlow, PyTorch, NumPy, Pandas

### Emerging Technologies

- **Newer frameworks** may have limited documentation
- **Niche libraries** might require alternative research methods
- **Proprietary tools** may not be in Context7 database

## Integration with Other Research Methods

### Context7 + Web Search

Use Context7 for official documentation and web search for:

- **Community tutorials and blog posts**
- **Real-world usage examples**
- **Performance benchmarks**
- **Migration stories and case studies**

### Context7 + GitHub Analysis

Complement Context7 research with:

- **GitHub repository analysis** (stars, issues, contributors)
- **Code examples from real projects**
- **Community discussions and issues**
- **Recent commits and release notes**

## Best Practices for Library Research

### Quality Assessment

When evaluating library information:

1. **Documentation Currency**: Check if documentation matches current version
2. **Example Accuracy**: Verify code examples work
3. **Completeness**: Ensure comprehensive coverage of topics
4. **Authority**: Prioritize official documentation

### Efficient Research Patterns

1. **Start Broad**: Begin with general overview
2. **Focus Down**: Drill into specific topics as needed
3. **Batch Similar**: Research related libraries together
4. **Cache Results**: Remember library IDs for future use

### Research Documentation

Document your research process:

```markdown
## Research Log for [Library Name]

### Context7 Resolution
- **Query**: [original search term]
- **Resolved ID**: [Context7 library ID]
- **Confidence**: [score]
- **Alternatives**: [other IDs considered]

### Documentation Retrieved
- **Topics**: [list of focused topics]
- **Version**: [specific version if targeted]
- **Quality**: [assessment of documentation quality]

### Key Insights
- [Main findings and analysis]
```

## Troubleshooting Common Issues

### Low Confidence Resolution

**Problem**: Context7 returns low confidence (< 0.7) for library ID

**Solutions**:
- Try alternative library names
- Check official documentation for correct naming
- Use web search to find official documentation links
- Look for alternative names or abbreviations

### Missing Documentation

**Problem**: Retrieved documentation is incomplete or outdated

**Solutions**:
- Specify different focus topics
- Try version-specific IDs
- Cross-reference with official website
- Use web search for recent tutorials

### Integration Conflicts

**Problem**: Information conflicts between Context7 and other sources

**Solutions**:
- Prioritize official documentation
- Check documentation dates
- Test conflicting approaches
- Consider library version differences

## Context7 API Reference

### mcp__context7__resolve-library-id

**Parameters**:
- `libraryName` (string): Name of the library to resolve

**Returns**:
- `libraryId` (string): Context7-compatible library ID
- `confidence` (number): Confidence score (0-1)
- `description` (string): Library description
- `alternatives` (array): Alternative library IDs if available

### mcp__context7__get-library-docs

**Parameters**:
- `context7CompatibleLibraryID` (string): Library ID from resolve function
- `topic` (string, optional): Focus area for documentation
- `tokens` (number, optional): Maximum tokens to retrieve (default: 5000)

**Returns**:
- `content` (string): Comprehensive documentation content
- `metadata` (object): Information about documentation source and version
- `examples` (array): Code examples if available

## Future Enhancements

### Planned Context7 Features

- **Batch Resolution**: Resolve multiple libraries in one call
- **Similar Library Detection**: Find alternative libraries automatically
- **Integration Examples**: Pre-built integration guides
- **Performance Benchmarks**: Standardized performance data

### Research Automation

- **Automatic Alternative Suggestions**: When library isn't found
- **Quality Scoring**: Automatic assessment of documentation quality
- **Update Notifications**: Alert when documentation is updated
- **Trending Libraries**: Identify popular emerging technologies

---

This guide ensures effective use of Context7 for comprehensive library research and documentation analysis.