---
name: troubleshooting
description: Comprehensive troubleshooting guide for API documentation generation, including common issues, solutions, and performance considerations
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - WebFetch
  - TodoWrite
---

# API Documentation Generator - Troubleshooting

## Documentation Generation Issues

### Problem: Incomplete documentation generated
- **Cause**: Missing source files or incomplete API specifications
- **Solution**: Provide all relevant source files including OpenAPI specs, docstrings, and type definitions
- **Check**: Verify that all API endpoints are covered in source code

### Problem: Poor formatting or structure
- **Cause**: Inconsistent source documentation format
- **Solution**: Standardize docstring formats and ensure consistent style
- **Fix**: Request specific formatting preferences and table structures

### Problem: Missing examples or code snippets
- **Cause**: Lack of example usage in source code
- **Solution**: Provide sample requests/responses or request example generation
- **Enhance**: Add real-world usage scenarios to documentation

## Source Format Issues

### Problem: OpenAPI spec parsing errors
- **Cause**: Invalid YAML/JSON syntax or missing required fields
- **Solution**: Validate OpenAPI spec with online validator before processing
- **Debug**: Check for missing paths, components, or schema definitions

### Problem: Python docstring extraction failing
- **Cause**: Non-standard docstring formats or missing function signatures
- **Solution**: Use consistent docstring format (Google, NumPy, or reST)
- **Fix**: Ensure proper indentation and format in docstrings

### Problem: JSDoc/TSDoc comments not recognized
- **Cause**: Incorrect comment syntax or missing annotation tags
- **Solution**: Use proper `/** */` syntax and standard JSDoc tags
- **Verify**: Check TypeScript type exports and interface definitions

## Content Quality Issues

### Problem: Generated documentation lacks detail
- **Cause**: Minimal or unclear source documentation
- **Solution**: Enhance source code with detailed descriptions and examples
- **Improve**: Add parameter descriptions, return value details, and usage examples

### Problem: Inconsistent terminology or naming
- **Cause**: Different naming conventions across source files
- **Solution**: Standardize naming conventions and terminology
- **Fix**: Create glossary or mapping for consistent terminology

### Problem: Missing error documentation
- **Cause**: Error handling not documented in source code
- **Solution**: Document all possible error conditions and responses
- **Enhance**: Add error codes, messages, and troubleshooting information

## Performance and Scalability Issues

### Problem: Large API documentation generation is slow
- **Cause**: Processing many files or complex API specifications
- **Solution**: Split documentation into multiple files or process incrementally
- **Optimize**: Use caching for repeated generations

### Problem: Memory usage during generation
- **Cause**: Loading large source files or complex schemas into memory
- **Solution**: Process files in smaller chunks or use streaming
- **Monitor**: Track memory usage during large documentation projects

## Integration and Tooling Issues

### Problem: Documentation conflicts with existing files
- **Cause**: Overwriting existing documentation without proper merging
- **Solution**: Use version control and review changes before committing
- **Backup**: Create backups of existing documentation before generation

### Problem: Tool compatibility issues
- **Cause**: Different tool versions or incompatible dependencies
- **Solution**: Ensure consistent tool versions and compatible formats
- **Test**: Validate generated documentation with different tools

## Quality Assurance

### Validation Checklist
- [ ] All API endpoints documented
- [ ] Parameters and responses fully described
- [ ] Examples work correctly
- [ ] Error conditions covered
- [ ] Navigation and cross-references functional
- [ ] Formatting consistent throughout
- [ ] Code examples syntax highlighted
- [ ] Links and references valid

## Common Error Messages and Solutions

### "Failed to parse OpenAPI specification"
- Validate JSON/YAML syntax with online validator
- Check for missing required fields (info, paths)
- Ensure proper indentation and formatting

### "No documentation found in source files"
- Verify docstring formats are recognized
- Check that functions/classes are properly commented
- Ensure source files are included in processing

### "Generated documentation missing sections"
- Review source code for missing documentation
- Check filtering criteria excluding important sections
- Verify template includes all necessary sections

### "Code examples not rendering correctly"
- Ensure proper code block formatting in source
- Check language specification for syntax highlighting
- Validate example code for syntax errors

## Getting Help

1. **Review source files**: Ensure complete and consistent documentation
2. **Check tool versions**: Verify compatibility of parsing tools
3. **Test with smaller subsets**: Isolate problematic files or sections
4. **Consult templates**: Compare with working examples in templates directory
5. **Validate intermediate results**: Check parsing output before final generation

## Performance Considerations

### Large API Documentation Performance

#### Optimizing Processing Speed
- Process source files in parallel when possible
- Use incremental parsing for large codebases
- Cache parsing results for repeated generations
- Split very large APIs into multiple documentation files

#### Memory Management
- Process large files in chunks to avoid memory overflow
- Use streaming parsers for large OpenAPI specifications
- Clear intermediate data structures after processing each file
- Monitor memory usage during documentation generation

#### File I/O Optimization
- Batch file operations to reduce disk I/O
- Use temporary files for intermediate processing
- Minimize file system calls during parsing
- Compress large output files when appropriate

### Scalability Strategies

#### Incremental Documentation Updates
- Track changes in source files to only process modified content
- Implement change detection for efficient updates
- Use timestamps or file hashes to identify changed files
- Cache parsing results for unchanged source files

#### Distributed Processing
- Split documentation generation across multiple processes
- Use worker processes for CPU-intensive parsing operations
- Implement job queues for large documentation projects
- Consider cloud-based processing for very large APIs

#### Template Optimization
- Pre-compile documentation templates for faster rendering
- Use efficient template engines with caching
- Minimize template complexity and nesting
- Optimize regular expressions and string operations

### Performance Monitoring

#### Key Metrics to Track
- Documentation generation time per file
- Memory usage during processing
- CPU utilization during parsing
- File I/O throughput
- Cache hit rates for incremental processing

#### Benchmarking Guidelines
```bash
# Time documentation generation
time python scripts/generate_docs.py

# Profile memory usage
/usr/bin/time -v python scripts/generate_docs.py

# Monitor processing progress
python scripts/generate_docs.py --verbose --progress
```

#### Performance Profiling
```python
# Add performance monitoring to generation scripts
import time
import psutil
import logging

def monitor_performance(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss

        result = func(*args, **kwargs)

        end_time = time.time()
        end_memory = psutil.Process().memory_info().rss

        logging.info(f"Function {func.__name__}: {end_time - start_time:.2f}s, "
                    f"Memory: {(end_memory - start_memory) / 1024 / 1024:.2f}MB")
        return result
    return wrapper
```

### Best Practices for High Performance

#### Source Code Organization
- Organize API documentation into logical modules
- Use consistent naming conventions for easier parsing
- Separate API specifications from implementation code
- Maintain clean separation between different API versions

#### Processing Optimization
- Use appropriate data structures for efficient lookups
- Implement lazy loading for large documentation sets
- Optimize regular expressions for performance
- Minimize string operations and memory allocations

#### Output Optimization
- Generate compressed output formats when possible
- Use efficient serialization for large data structures
- Implement pagination for very large API documentation
- Provide incremental loading options for web-based documentation

### Performance Anti-Patterns

#### Avoid These Issues:
- Loading entire codebase into memory simultaneously
- Processing files sequentially when parallel processing is possible
- Recompiling templates for each generation
- Using inefficient parsing algorithms for large files
- Ignoring memory leaks in long-running processes

#### Performance Improvements:
- Implement streaming parsers for large files
- Use worker pools for CPU-intensive operations
- Cache frequently accessed data and templates
- Optimize database queries for API data extraction
- Profile and optimize bottlenecks in the generation pipeline