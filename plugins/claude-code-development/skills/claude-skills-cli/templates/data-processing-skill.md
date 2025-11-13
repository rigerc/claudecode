---
name: data-processor
description: Processing and analyzing data files in CSV, JSON, and Excel formats. Use for data cleaning, transformation, and analysis tasks.
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Data Processor

## Overview
Processing and analyzing various data formats including CSV, JSON, and Excel files for data cleaning, transformation, and analysis tasks.

## When to Use
Use this skill when:
- Working with CSV files and need data cleaning or analysis
- Processing JSON data and require transformation or validation
- Analyzing Excel spreadsheets and need insights or formatting
- Converting between different data formats
- Performing data quality checks and validation

## Instructions
1. **Identify Data Format**: Determine the file type and structure
2. **Analyze Requirements**: Understand what processing is needed
3. **Choose Processing Method**: Select appropriate approach based on data size and complexity
4. **Execute Processing**: Apply transformations, cleaning, or analysis
5. **Validate Results**: Ensure data integrity and expected outcomes

## Data Format Handling

### CSV Files
- Use Read to examine structure and headers
- Check for delimiters, quoting, and encoding issues
- Identify data types and formatting problems
- Apply cleaning rules as needed

### JSON Files
- Parse and validate JSON structure
- Check for nested objects and arrays
- Extract relevant fields for processing
- Validate data types and required fields

### Excel Files
- Identify sheets and data ranges
- Check for merged cells and formatting
- Handle formulas and calculated values
- Extract data for analysis

## Common Processing Tasks

### Data Cleaning
- Remove duplicates and empty rows
- Fix formatting inconsistencies
- Handle missing values
- Standardize text case and spacing

### Data Transformation
- Convert between data types
- Restructure data layouts
- Create derived fields
- Aggregate and summarize data

### Data Analysis
- Generate summary statistics
- Create data profiles
- Identify patterns and outliers
- Validate business rules

## Examples

### Example 1: CSV Cleaning
**User request**: "Clean up this messy CSV file with inconsistent dates and duplicate rows"
**Workflow**:
1. Read the CSV file to examine structure
2. Use Grep to identify date format patterns
3. Remove duplicate rows
4. Standardize date formats
5. Validate data integrity

### Example 2: JSON Transformation
**User request**: "Convert this nested JSON into a flat CSV format"
**Workflow**:
1. Parse JSON structure to identify nesting
2. Extract required fields from nested objects
3. Create flat CSV structure
4. Transform and export data

### Example 3: Excel Analysis
**User request**: "Analyze this sales data and create a summary report"
**Workflow**:
1. Read Excel file and identify data ranges
2. Generate summary statistics
3. Identify trends and patterns
4. Create analysis report

## Best Practices
- Always create backups before modifying data
- Validate data structure before processing
- Handle encoding and locale issues appropriately
- Document transformation steps for reproducibility
- Test processing on small samples first

## Troubleshooting
### Issue: File not reading correctly
**Solution**: Check file encoding, delimiters, and structure

### Issue: Data type errors
**Solution**: Explicitly handle type conversions and validation

### Issue: Memory issues with large files
**Solution**: Process data in chunks or use streaming approaches

For format-specific guidance, see [data format reference](references/data-formats.md).