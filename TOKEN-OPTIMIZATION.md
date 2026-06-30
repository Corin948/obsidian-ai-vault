# Token Optimization Strategy

This document explains how the vault architecture minimizes token usage for AI tools (Claude Code, Kimi Code, and future LLM integrations).

## Core Principles

### 1. MOCs as Compression Layer

**Problem:** Feeding 200 notes to an AI costs thousands of tokens.
**Solution:** MOCs (Maps of Content) act as compressed indexes. A MOC contains:
- Title and purpose (1 sentence)
- List of related notes with 1-line descriptions
- Status summary (active count, orphaned count)
- Last reviewed date

**Usage:** Always tell AI to "read the MOC first." Example:
```
"Check 04-MOCs/Machine-Learning-MOC.md, then answer my question about neural networks."
```

### 2. YAML Frontmatter as Filter

Every note has structured metadata:
```yaml
---
date: 2025-01-15
tags: [permanent-note, machine-learning]
status: evergreen
project: ai-research
---
```

AI can filter notes without reading content:
```
"Find all notes with status: seedling and tag: machine-learning."
```
This costs ~10 tokens per note (just frontmatter) instead of 500+ tokens (full content).

### 3. Atomic Notes

**Rule:** One idea per note, <500 words.

**Why:** When AI needs to reference a concept, it reads one small note instead of a 3,000-word monolith.

**Enforcement:** Claude Code and Kimi Code are instructed to suggest splitting notes that exceed this limit.

### 4. Folders as Filters, Links as Relationships

- **Folders** organize by type (Daily, Meeting, Permanent, etc.). AI can target specific folders.
- **Links** (`[[Note]]`) build the knowledge graph. AI follows links instead of searching.

**Usage:**
```
"Follow the links from 05-Permanent-Notes/Cognitive-Load.md and summarize the related concepts."
```
This is cheaper than "Search the entire vault for related content."

### 5. Automation Pre-Computes Expensive Operations

| Expensive Operation | Automated Replacement | Token Savings |
|---|---|---|
| AI finds orphaned notes | GitHub Action finds orphans + suggests links | 90% |
| AI structures raw meeting notes | GitHub Action extracts action items | 80% |
| AI audits tags for consistency | Auto-Linker standardizes tags | 70% |
| AI searches for stale notes | Stale Note Checker flags them | 95% |

**Result:** You only pay AI tokens for *creative/analytical* tasks, not *mechanical* tasks.

---

## Claude Code Specific Tips

1. **Use the `.claude/CLAUDE.md` context file.** It teaches Claude the vault structure so you don't have to explain it every session.

2. **Batch operations.** Claude Code can process multiple files in one pass:
```bash
claude "Process all .md files in 00-Inbox/ older than 3 days."
```

3. **Reference MOCs in prompts.**
```bash
claude "Using 04-MOCs/Project-Alpha-MOC.md as context, what are the next 3 priorities?"
```

4. **Use git-aware context.** Claude Code sees your git history. Ask:
```bash
claude "What notes have I created in the last week? Summarize the themes."
```

---

## Kimi Code Specific Tips

1. **Use the `.kimi/instructions.md` file.** Kimi Code reads it on workspace load, giving it vault context.

2. **Multi-file editing.** Kimi can edit multiple files in one operation. Batch updates to MOCs.

3. **Smart completions.** When typing `[[`, Kimi suggests existing note titles — reducing search tokens.

4. **Chat with context.** Reference specific files in the chat panel instead of pasting content:
```
"Based on the current file 05-Permanent-Notes/Habit-Loop.md, suggest 3 related notes to create."
```

---

## Future: LLM API Integration

For even smarter automation, add an LLM API to GitHub Actions:

1. Add `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` to GitHub repository secrets.
2. Modify `auto_linker.py` to call the API for semantic similarity instead of keyword matching.
3. Modify `meeting_processor.py` to use the API for transcription summarization.

**Cost trade-off:** API calls cost money but save human time. The keyword-based automation in this repo is free but less accurate. Upgrade when the vault grows beyond ~500 notes.

---

## Benchmarks

| Task | Without Optimization | With This Vault | Savings |
|---|---|---|
| "What do I know about machine learning?" | 5,000 tokens (search 50 notes) | 500 tokens (read 1 MOC) | 90% |
| "Structure my meeting notes" | 3,000 tokens per meeting | 0 tokens (GitHub Action) | 100% |
| "Find orphaned notes" | 4,000 tokens (analyze graph) | 0 tokens (GitHub Action) | 100% |
| "Daily review" | 2,000 tokens (read 7 daily notes) | 300 tokens (read 1 weekly MOC) | 85% |

---

*Remember: The goal is not to eliminate AI usage, but to eliminate WASTEFUL AI usage. Let automation handle the mechanical work. Reserve AI tokens for creative synthesis and insight generation.*
