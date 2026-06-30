# Obsidian AI Vault — Automation Guide

## Overview

This vault runs three GitHub Actions workflows to automate knowledge management:

1. **Auto-Linker** (`auto-linker.yml`) — Daily at 2 AM UTC
2. **Meeting Processor** (`meeting-processor.yml`) — On every push to `02-Meetings/`
3. **Stale Note Cleaner** (`stale-note-cleaner.yml`) — Weekly on Sunday at 3 AM UTC

---

## Auto-Linker

**What it does:**
- Scans all notes for orphaned notes (0 backlinks)
- Analyzes content and tags to suggest related notes
- Suggests tags based on keyword analysis
- Adds a "Suggested Connections" section to orphaned notes
- Opens a Pull Request with the changes for you to review

**How to use:**
- Let it run automatically (daily)
- Or trigger manually: Actions → Auto-Linker → Run workflow
- Review the PR before merging — the suggestions are algorithmic, not perfect

**Token tip:** This reduces AI token usage by pre-computing links, so Claude/Kimi don't have to analyze the entire vault to find connections.

---

## Meeting Processor

**What it does:**
- Triggers when you push a new meeting note to `02-Meetings/`
- Extracts action items using regex patterns
- Structures the note with sections: Raw Notes, Summary, Discussion Points, Decisions, Action Items
- Updates the relevant Project MOC with action items
- Changes `status: unprocessed` to `status: processed`

**Workflow:**
1. Create a meeting note using the template (`08-Templates/Meeting-Note.md`)
2. Paste raw notes/transcript in the "Raw Notes" section
3. Push to GitHub
4. GitHub Action structures it automatically
5. Pull the changes back to Obsidian

**Token tip:** The GitHub Action does the heavy lifting (structure extraction), so you only ask Claude/Kimi for *analysis* of the structured meeting, not raw transcription processing.

---

## Stale Note Cleaner

**What it does:**
- Weekly scan for notes that have been unprocessed too long
- Inbox notes > 7 days old
- Fleeting notes > 7 days old
- Meeting notes with `status: unprocessed` > 3 days old
- Generates a report in `.github/reports/stale_notes.md`

**How to use:**
- Check the report weekly
- Either process the notes or delete them
- The report serves as a "nag" without modifying your vault

---

## Manual Trigger

All workflows support manual triggering:
1. Go to GitHub → Actions
2. Select the workflow
3. Click "Run workflow"

---

## Future Enhancements

- **LLM-powered linking:** Replace keyword-based tag suggestions with an LLM API call (OpenAI, Claude, Kimi) for smarter suggestions. Add API key to repository secrets.
- **Transcription integration:** Connect with Whisper or other transcription APIs to convert audio files in `99-Attachments/` into structured meeting notes.
- **Knowledge graph visualization:** Export note relationships to a graph format for visualization.
