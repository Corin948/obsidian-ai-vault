# Kimi Code (Desktop IDE) Integration Guide

Kimi Code IDE loads this workspace as a project. This guide explains how to use Kimi Code effectively with your Obsidian vault.

## Workspace Setup

1. Open Kimi Code (Desktop IDE).
2. File → Open Folder → Select `obsidian-ai-vault`.
3. Kimi Code will automatically read `.kimi/instructions.md` to understand the vault structure.

## Key Workflows

### 1. Vault-Wide Search & Analysis
Use Kimi Code's file explorer to navigate. Ask Kimi in the chat:
```
Search all files in 05-Permanent-Notes/ for mentions of "cognitive load" and summarize the connections.
```

### 2. Meeting Note Structuring
```
Read 02-Meetings/2025-01-15-Product-Review.md. Extract action items, assign owners, and create a summary.
```

### 3. Note Creation from Context
```
Based on the current file I'm editing, suggest 2-3 related notes I should create and link.
```
*Kimi reads the current file's content and suggests connections.*

### 4. MOC Maintenance
```
The file 04-MOCs/Machine-Learning-MOC.md is outdated. Update it to include all notes with tag "machine-learning".
```

### 5. Refactoring
```
Find all notes in 00-Inbox/ older than 7 days. For each, suggest whether to move to Permanent Notes, link to a MOC, or delete.
```

## Token Efficiency Tips

1. **Use the sidebar context** — Kimi Code already indexes the file tree. Reference files by path.
2. **Multi-file editing** — Kimi can edit multiple files in one pass. Batch operations: "Update all MOCs to add `last-reviewed` date."
3. **Smart completions** — When typing in a note, Kimi suggests links based on existing note titles.

## Differences from Claude Code

- **Claude Code** is CLI-based, great for batch operations and git workflows.
- **Kimi Code** is IDE-based, great for real-time writing assistance and inline suggestions.
- **Use both:** Kimi for writing and editing; Claude for bulk analysis and automation.
