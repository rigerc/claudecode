# Golden File Templates

This directory contains templates for golden files used in Teastraw TUI testing.

## Golden File Structure

Golden files should contain the exact terminal output that your TUI application produces. They are used to validate that your application's UI remains consistent across changes.

## Template Examples

### Basic Welcome Screen
```
Welcome to TUI Application

Press 'q' to quit
Press 'h' for help

>
```

### Menu Navigation Screen
```
Main Menu
─────────

● Settings
  Help
  About
  Quit

Use arrow keys or j/k to navigate
Press Enter to select
Press 'q' to quit
```

### Form Screen
```
User Information Form

Name: [John Doe        ]
Email: [john@example.com]
Phone: [555-0123       ]

Tab: Next field    Enter: Submit    Esc: Cancel
```

### Error Message Screen
```
Error: Invalid input

Please enter a valid email address.

Press Enter to continue
```

### Success Message Screen
```
Success!

Your changes have been saved.

Press any key to continue...
```

## Best Practices for Golden Files

1. **Use descriptive names**: Prefix golden files with the test function name
2. **Include complete screen output**: Capture the entire terminal state
3. **Avoid dynamic content**: Exclude timestamps, random values, or changing data
4. **Test multiple states**: Create golden files for different application states
5. **Update regularly**: Update golden files when UI changes intentionally

## File Naming Convention

```
testdata/
├── TestNavigation_initial_screen.golden
├── TestNavigation_after_down_arrow.golden
├── TestForm_empty_form.golden
├── TestForm_filled_form.golden
├── TestForm_success_message.golden
├── TestError_invalid_input.golden
└── TestError_file_not_found.golden
```

## Generating Golden Files

Use the test runner with the `-update` flag:

```bash
# Update all golden files
go test ./tests/tui/... -update

# Update specific test golden files
go test -run TestNavigation -update

# Update golden files with verbose output
go test -v ./tests/tui/... -update
```

## Validating Golden Files

Golden files should contain:
- Complete terminal screen content
- Proper formatting and spacing
- All visible text and UI elements
- Error messages and success states

Golden files should NOT contain:
- ANSI color codes (unless testing color output)
- Cursor positioning sequences
- Dynamic timestamps or IDs
- Random data or values