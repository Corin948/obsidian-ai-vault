# Claude Code Integration Guide

Claude Code reads this vault as a file tree. This guide explains how to use Claude Code effectively with your Obsidian vault.

## Context Awareness

Claude Code automatically reads `.claude/CLAUDE.md` when you open this repo. That file contains the vault's architecture, naming conventions, and interaction rules.

## Key Workflows

### 1. Daily Review
```bash
claude "Review my daily notes from this week and identify recurring themes."
```
*Claude reads the Daily Notes folder, extracts patterns, and suggests permanent notes or MOCs to create.*

### 2. Meeting Processing
```bash
claude "Structure the meeting note 02-Meetings/2025-01-15-Product-Review.md. Extract action items and suggest owners."
```
*Claude reads the raw meeting note, structures it, and updates the relevant project MOC.*

### 3. Orphaned Note Analysis
```bash
claude "Find all notes in 05-Permanent-Notes/ with zero backlinks. For each, suggest 2-3 related notes to link to."
```
*Claude scans the vault graph, identifies orphans, and suggests connections.*

### 4. MOC Generation
```bash
claude "I just created 5 notes about machine learning. Generate a MOC in 04-MOCs/Machine-Learning-MOC.md that indexes them."
```
*Claude creates a compressed index note linking all related notes.*

### 5. Tag Consistency
```bash
claude "Audit all tags in the vault. Find inconsistent naming (e.g., 'machine-learning' vs 'machine_learning'). Suggest a standard."
```

## Token Optimization

**Claude Code is token-smart by default, but you can help it:**

1. **Always mention the MOC first** — "Check 04-MOCs/Machine-Learning-MOC.md before answering."
2. **Use date ranges** — "Review Daily Notes from 2025-01-01 to 2025-01-15."
3. **Filter by frontmatter** — "Find all notes with `status: seedling` and suggest how to develop them."
4. **Batch operations** — "Process all .md files in 00-Inbox/ in one pass."

## Project-Specific Rules

Place a `.claude/CLAUDE.md` file in any project subfolder (e.g., `03-Projects/My-Project/.claude/CLAUDE.md`). Claude will read it when working in that directory, giving you project-specific context.

## Safety

- Claude Code writes directly to files. Review its changes before committing.
- Use `git diff` to see what Claude modified.
- The `.claude/CLAUDE.md` file instructs Claude to preserve YAML frontmatter and Obsidian link syntax.
