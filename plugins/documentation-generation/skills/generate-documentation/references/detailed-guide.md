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

## Troubleshooting

### Research and Analysis Issues

**Problem**: Unable to find relevant information about libraries or frameworks
- **Cause**: Library name confusion, outdated documentation, or incorrect search terms
- **Solution**: Use multiple search strategies including context7, web search, and source code analysis
- **Debug**: Try alternative library names or check parent organization names

**Problem**: Code analysis reveals incomplete or unclear functionality
- **Cause**: Poorly documented source code or complex implementation patterns
- **Solution**: Combine static analysis with dynamic testing and experimentation
- **Enhance**: Create test cases to verify code behavior and document findings

**Problem**: Conflicting information from different sources
- **Cause**: Outdated documentation, version differences, or incorrect implementation
- **Solution**: Prioritize official documentation and verify with current code
- **Resolve**: Test different approaches and document what actually works

### Documentation Generation Issues

**Problem**: Generated documentation lacks technical depth
- **Cause**: Insufficient research or incomplete understanding of the subject
- **Solution**: Spend more time on research phase and consult multiple sources
- **Improve**: Include code examples, configuration details, and practical use cases

**Problem**: Documentation structure is disorganized or hard to follow
- **Cause**: Poor planning or inappropriate document type for the content
- **Solution**: Create detailed outline before writing and choose appropriate documentation format
- **Fix**: Restructure content with clear hierarchy and logical flow

**Problem**: Examples don't work or are outdated
- **Cause**: Code examples not tested or based on older versions
- **Solution**: Test all examples before inclusion and verify current compatibility
- **Validate**: Run examples in clean environment to ensure they work

### Tool and Integration Issues

**Problem**: Context7 integration failing or returning limited results
- **Cause**: Library not found in Context7 database or network connectivity issues
- **Solution**: Verify library name spelling and try alternative search terms
- **Backup**: Fall back to web search and official documentation sources

**Problem**: File system permissions preventing documentation creation
- **Cause**: Insufficient permissions to write to docs/ directory or create new files
- **Solution**: Check directory permissions and use appropriate file creation commands
- **Workaround**: Create documentation in alternative location and move files manually

**Problem**: Generated documentation doesn't match existing style
- **Cause**: Inconsistent formatting or different documentation standards
- **Solution**: Analyze existing documentation patterns and match the style
- **Standardize**: Create style guide for consistent documentation across project

### Content Quality Issues

**Problem**: Documentation is too technical for target audience
- **Cause**: Writing for wrong audience or insufficient explanation of concepts
- **Solution**: Clearly identify audience and adjust language complexity accordingly
- **Improve**: Add beginner-friendly sections and glossaries for technical terms

**Problem**: Missing important edge cases or error conditions
- **Cause**: Incomplete testing or lack of real-world usage experience
- **Solution**: Research common issues and error scenarios from community resources
- **Enhance**: Include troubleshooting sections and FAQ for common problems

**Problem**: Documentation becomes outdated quickly
- **Cause**: Rapid development cycles or changing API requirements
- **Solution**: Implement documentation review process and version control
- **Maintain**: Create automated checks for documentation accuracy

### Performance and Scalability Issues

**Problem**: Documentation generation taking too long for large projects
- **Cause**: Inefficient file processing or large codebase analysis
- **Solution**: Optimize analysis patterns and process files in parallel when possible
- **Improve**: Use caching for repeated analysis and incremental updates

**Problem**: Memory usage issues during documentation generation
- **Cause**: Loading large files or processing complex data structures
- **Solution**: Process files in chunks and clear unused data structures
- **Monitor**: Track memory usage and implement limits for large operations

### Common Error Scenarios and Solutions

**"Unable to locate library documentation"**
- Verify library name and spelling
- Check alternative names or parent projects
- Search web for official documentation sites
- Look for GitHub repositories with comprehensive README files

**"Generated examples don't work"**
- Test examples in isolated environment
- Check for missing dependencies or setup requirements
- Verify example matches current version of library/framework
- Include setup instructions with examples

**"Documentation structure is confusing"**
- Review similar projects for structure patterns
- Create user personas and map their documentation needs
- Use consistent section organization and navigation
- Include table of contents for longer documents

**"Content is too technical/non-technical"**
- Define target audience clearly before writing
- Use analogies and real-world examples for complex concepts
- Provide multiple difficulty levels (beginner, intermediate, advanced)
- Include glossaries for technical terminology

### Quality Assurance Process

**Pre-Publication Checklist**
- [ ] All code examples tested and working
- [ ] Information verified with official documentation
- [ ] Structure logical and easy to navigate
- [ ] Language appropriate for target audience
- [ ] Cross-references and links functional
- [ ] Consistent formatting throughout
- [ ] Spelling and grammar checked
- [ ] Technical accuracy verified by subject matter expert

**Post-Publication Review**
- Collect user feedback on clarity and usefulness
- Monitor for reported errors or outdated information
- Track documentation usage patterns
- Schedule regular reviews and updates
- Maintain changelog for documentation improvements

### Getting Help

1. **Check multiple sources**: Verify information across official docs, community resources, and source code
2. **Test with examples**: Create working examples to validate understanding
3. **Get feedback**: Have subject matter experts review technical accuracy
4. **Iterate and improve**: Continuously update documentation based on user feedback
5. **Use templates**: Leverage existing documentation templates and patterns for consistency

## Performance Considerations

### Documentation Generation Performance

**Research Phase Optimization**
- Use targeted searches instead of broad web searches when possible
- Cache frequently accessed library documentation
- Prioritize official documentation over secondary sources
- Limit research scope to relevant sections and avoid information overload

**Analysis Phase Efficiency**
- Process files in parallel when analyzing large codebases
- Use appropriate file filtering to avoid unnecessary processing
- Implement incremental analysis for repeated documentation updates
- Cache parsing results for unchanged files

**Content Generation Speed**
- Use templates and boilerplate content for consistent formatting
- Batch similar operations together (e.g., table generation)
- Implement lazy loading for large datasets or examples
- Use efficient string operations and minimize memory allocations

### Memory and Resource Management

**Efficient File Processing**
- Process large files in chunks to avoid memory overflow
- Use streaming parsers for large source files
- Clear intermediate data structures after processing each section
- Monitor memory usage during large documentation projects

**Resource Cleanup**
- Close file handles and network connections promptly
- Clear temporary files and cache data after use
- Use context managers for resource allocation
- Implement proper cleanup in automation scripts

### Scalability Strategies

**Large Project Documentation**
- Split documentation into multiple focused files
- Use modular documentation architecture
- Implement incremental updates for changed sections only
- Create documentation generation pipelines for automation

**Concurrent Processing**
- Use multiprocessing for CPU-intensive analysis tasks
- Implement worker pools for parallel file processing
- Use async operations for network requests and I/O
- Consider distributed processing for very large projects

### Caching and Optimization

**Research Result Caching**
- Cache Context7 API responses to avoid repeated requests
- Store web search results for commonly researched topics
- Implement local cache for frequently accessed documentation
- Use cache invalidation strategies for outdated information

**Analysis Result Caching**
- Cache AST parsing results for source code files
- Store extracted metadata and documentation patterns
- Implement file hash-based cache invalidation
- Use persistent cache for long-running documentation projects

### Performance Monitoring

**Key Metrics**
- Documentation generation time per project
- Memory usage during analysis and generation
- Network request count and response times
- File processing throughput
- Cache hit rates and effectiveness

**Benchmarking Tools**
```bash
# Time documentation generation
time python generate_docs.py

# Profile memory usage
/usr/bin/time -v python generate_docs.py

# Monitor network requests
strace -c -p $(pgrep python) 2>&1 | grep -E "(connect|send|recv)"
```

**Performance Profiling**
```python
import time
import cProfile
import pstats
from functools import wraps

def profile_performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()

        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()

        profiler.disable()

        stats = pstats.Stats(profiler)
        stats.sort_stats('cumulative')
        stats.print_stats(10)  # Top 10 functions

        print(f"Function {func.__name__} executed in {end_time - start_time:.2f}s")
        return result
    return wrapper
```

### Best Practices for High Performance

**Optimization Strategies**
1. **Batch Operations**: Group similar operations together
2. **Lazy Loading**: Load data only when needed
3. **Parallel Processing**: Use multiple cores for analysis tasks
4. **Smart Caching**: Cache frequently accessed data
5. **Efficient Algorithms**: Choose appropriate data structures and algorithms

**Resource Management**
1. **Memory Efficiency**: Process data in chunks, clear unused objects
2. **Network Optimization**: Minimize API calls, use efficient protocols
3. **I/O Optimization**: Batch file operations, use async I/O
4. **Process Management**: Use appropriate process/threading models

**Quality vs Performance Balance**
1. **Prioritize Critical Paths**: Optimize frequently used operations
2. **Measurable Improvements**: Profile before and after optimizations
3. **Incremental Optimization**: Focus on bottlenecks first
4. **User Experience**: Maintain documentation quality while improving speed