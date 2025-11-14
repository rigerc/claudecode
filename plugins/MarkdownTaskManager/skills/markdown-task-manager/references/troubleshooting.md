---
name: markdown-task-manager
description: Use when managing tasks, the system is a Kanban task manager based on local Markdown files (`kanban.md` and `archive.md`). It follows a strict format compatible with the task-manager.html web application.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - TodoWrite
---

## Troubleshooting

### File and Format Issues

**Problem**: kanban.md or archive.md files don't exist
- **Cause**: Initial setup not completed or files deleted accidentally
- **Solution**: Run automatic setup via SessionStart hook or manual setup script
- **Manual fix**: Copy template files from assets/ directory to project root
- **Verification**: Ensure both kanban.md and archive.md exist in project directory

**Problem**: Tasks not displaying correctly in task-manager.html
- **Cause**: Format violations, especially using `##` or `###` headings inside tasks
- **Solution**: Review task format and remove any nested headings
- **Check**: Ensure strict adherence to the mandatory template format
- **Fix**: Replace nested headings with bold subsections like `**Technical decisions**:`

**Problem**: Task ID not incrementing correctly
- **Cause**: Last Task ID comment not updated or formatted incorrectly
- **Solution**: Verify `<!-- Config: Last Task ID: XXX -->` format is exact
- **Check**: Ensure comment is at the top of kanban.md file
- **Fix**: Manually update the comment with the correct last used ID

### Task Management Issues

**Problem**: Cannot find specific task in kanban.md
- **Cause**: Task moved to wrong section or ID formatting issues
- **Solution**: Search for task ID using grep: `grep "TASK-XXX" kanban.md`
- **Debug**: Check all column sections and archive.md for missing tasks
- **Prevention**: Always move tasks using complete task blocks

**Problem**: Duplicate task IDs in the system
- **Cause**: Manual editing errors or concurrent task creation conflicts
- **Solution**: Identify duplicate IDs and renumber affected tasks
- **Fix**: Update Last Task ID comment to reflect highest actual task ID
- **Prevention**: Always check current last ID before creating new tasks

**Problem**: Subtasks not being tracked correctly
- **Cause**: Incorrect checkbox format or missing `**Subtasks**:` section
- **Solution**: Use proper Markdown checkbox format: `- [ ]` and `- [x]`
- **Check**: Ensure `**Subtasks**:` section exists and is properly formatted
- **Example**:
  ```markdown
  **Subtasks**:
  - [ ] First incomplete subtask
  - [x] Completed subtask
  ```

### Performance and Scalability Issues

**Problem**: kanban.md file becoming too large and slow to process
- **Cause**: Too many active tasks or insufficient archiving
- **Solution**: Regularly archive completed tasks to keep active list manageable
- **Maintenance**: Set threshold (e.g., archive tasks older than 30 days)
- **Optimization**: Archive tasks in batches to maintain performance

**Problem**: Web interface (task-manager.html) loading slowly
- **Cause**: Large kanban.md file with many tasks and complex formatting
- **Solution**: Optimize task descriptions and archive old completed tasks
- **Performance**: Limit active tasks to under 50 for optimal web interface performance
- **Alternative**: Consider splitting large projects into multiple kanban files

### Integration Issues

**Problem**: Git integration not working properly
- **Cause**: Inconsistent commit message format or missing task references
- **Solution**: Always include task ID in commit messages: `(TASK-XXX)`
- **Best practice**: Use format: `type: description (TASK-XXX - progress)`
- **Branch naming**: Use consistent pattern: `feature/TASK-XXX-description`

**Problem**: SessionStart hook not running automatically
- **Cause**: Plugin not enabled or hook configuration issues
- **Solution**: Verify MarkdownTaskManager plugin is enabled in Claude Code
- **Debug**: Check hook logs for any error messages
- **Manual**: Run setup script manually: `.claude/hooks/scripts/auto-setup.sh`

### Data Integrity Issues

**Problem**: Corrupted kanban.md due to editing conflicts
- **Cause**: Simultaneous edits or merge conflicts in version control
- **Solution**: Restore from backup or manually reconstruct using git history
- **Prevention**: Use file locking or coordinate editing sessions
- **Recovery**: Check git reflog for previous versions if needed

**Problem**: Archive.md becoming disorganized
- **Cause**: Inconsistent archiving process or missing separators
- **Solution**: Ensure proper `---` separators between archived tasks
- **Maintenance**: Regularly review and reorganize archive structure
- **Format**: Maintain consistent date ordering within archives

### Browser Compatibility Issues

**Problem**: task-manager.html not displaying correctly in certain browsers
- **Cause**: Browser compatibility issues or JavaScript errors
- **Solution**: Test in modern browsers and check browser console for errors
- **Debug**: Open browser developer tools to identify specific issues
- **Alternative**: Use text-based task management if web interface unavailable

### Common Error Messages and Solutions

**"Task not found" errors**
- Verify task ID exists in kanban.md
- Check for ID formatting (TASK-XXX with leading zeros)
- Search in archive.md if task might be archived
- Review recent commits for task references

**"Invalid format" warnings**
- Check for nested headings inside task descriptions
- Verify `**Subtasks**:` and `**Notes**:` sections use colons
- Ensure no `##` or `###` headings within task content
- Review mandatory template compliance

**"File not found" errors**
- Confirm kanban.md and archive.md exist in project root
- Check file permissions and accessibility
- Run setup script if files are missing
- Verify working directory is correct

### Performance Optimization Tips

**File Management**
- Archive completed tasks regularly (keep only last 30 days in active)
- Use concise task descriptions to minimize file size
- Implement batch archiving for efficiency
- Consider separate kanban files for very large projects

**Workflow Optimization**
- Create task templates for common task types
- Use batch operations for multiple similar tasks
- Implement regular maintenance schedules
- Use consistent naming and categorization patterns

**Web Interface Performance**
- Limit active tasks to under 50 for optimal performance
- Use task filtering and search features in task-manager.html
- Clear browser cache periodically
- Consider browser extensions for better Markdown rendering

### Getting Help

1. **File verification**: Check kanban.md format using template examples
2. **Setup verification**: Run manual setup script to verify installation
3. **Log analysis**: Check Claude Code logs for hook or plugin errors
4. **Template reference**: Review complete examples in skill documentation
5. **Community support**: Check plugin repository for known issues and solutions