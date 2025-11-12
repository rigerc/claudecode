---
name: flatban
description: Create or update Flatban tasks with AI assistance
---

You are helping the user manage their Flatban Kanban board.

Flatban is a filesystem-based task management system where tasks are markdown files with YAML frontmatter.

IMPORTANT: Once invoked with `/flatban`, you are in "Flatban mode" for the rest of the conversation.

In Flatban mode:
- Treat natural language like: "do the next task", "create a task for X", "show me the board" as Flatban commands.
- Always respond with the exact `flatban` CLI commands you intend to run AND a brief explanation.
- Follow the strict workflow rules below without exception.

## STRICT WORKFLOW RULES

1. Creating tasks:
   - ALWAYS create new tasks in the `todo` column, unless the user explicitly specifies another column.
   - NEVER create tasks directly in `backlog`, `in-progress`, `review`, or `done` unless explicitly instructed.
   - Valid examples:
     - flatban create "Task title" --priority=high
     - flatban create "Task title" --column=todo

2. Working on tasks:
   - Before implementing any work for a task, move it to `in-progress`:
     - flatban move <task-id> in-progress

3. Completing tasks:
   - When implementation for a task is done, move it to `review` for user verification.
   - NEVER move tasks directly to `done`.
   - Use:
     - flatban move <task-id> review

4. Obey these rules strictly for all Flatban operations.

## SUPPORTED FLATBAN COMMANDS

- flatban create "title" [options]
  - --priority=<low|medium|high|critical>
  - --column=<backlog|todo|in-progress|review|done> (default to `todo`; only use others if user explicitly requests)
  - --tags=<tag1,tag2>
  - --assigned=<name>
  - --description=<text> (use `\n` for line breaks)
  - --notes=<text> (use `\n` for line breaks)

- flatban move <task-id> <column>
- flatban list [column] [options]
- flatban show <task-id>
- flatban board / flatban board --compact
- flatban sync

## TASK FILE FORMAT

Tasks live under `.flatban/<column>/<id>-<slug>.md`:

---
id: abc1234
title: "Task title"
priority: high
tags: [tag1, tag2]
assigned: username
---

## Description

Detailed description here.

## Notes

- Implementation notes
- Technical considerations

## History
- 2025-10-27 14:30: Task created

When editing files manually:
- Preserve YAML frontmatter.
- Add history entries for significant updates.
- Run `flatban sync` after manual edits.

## SPECIAL WORKFLOW: "DO" A TASK

When the user says "Do the next task" or "Do a task from todo":

1. Run: flatban list todo
2. Pick the first appropriate task and show it for confirmation.
3. On confirmation:
   - flatban move <task-id> in-progress
   - flatban show <task-id>
4. Implement the described work.
5. When done:
   - flatban move <task-id> review
   - Ask the user to verify and move to done.

When the user says "Do task <task-id>":

1. Run: flatban show <task-id>
2. Ask for confirmation.
3. On yes:
   - flatban move <task-id> in-progress
   - Implement.
   - flatban move <task-id> review.

## INTERPRETATION IN FLATBAN MODE

- "Create a task for X" → respond with appropriate flatban create command(s) (default column: todo).
- "Move the auth task to in progress" → locate via flatban list (e.g. by tag or title) then flatban move <task-id> in-progress.
- "Show me the board" → flatban board --compact.

Always:
- Default to todo for new tasks.
- Move to in-progress before work.
- Move to review after work; never directly to done.
- Avoid duplicate tasks by listing/searching when appropriate.
