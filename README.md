# Obsidian AI Vault

An opinionated Obsidian vault template with Git sync, Claude Code / Kimi Code integration, and GitHub Actions automation.

## Architecture Philosophy

- **AI lives OUTSIDE Obsidian** — Claude Code and Kimi Code CLI read the vault as files, write back as files. No plugins needed inside Obsidian.
- **Token-optimized context** — MOCs (Maps of Content) act as compressed indexes. AI reads MOCs first, then drills down.
- **Structured frontmatter** — Every note has YAML metadata so AI can filter without reading full content.
- **Atomic notes** — Small, focused notes reduce the context window needed per query.

## Folder Structure

```
.
├── .github/workflows/       # Automation workflows
├── .claude/                 # Claude Code context rules
├── .kimi/                   # Kimi Code IDE instructions
├── 00-Inbox/                # Drop zone for new notes
├── 01-Daily-Notes/          # Daily journal entries (YYYY-MM-DD format)
├── 02-Meetings/             # Meeting notes (YYYY-MM-DD-Topic format)
├── 03-Projects/             # Active project folders
├── 04-MOCs/                 # Maps of Content (index notes)
├── 05-Permanent-Notes/      # Zettelkasten-style atomic notes
├── 06-Fleeting-Notes/       # Quick captures (to be processed)
├── 07-Resources/            # Book summaries, articles, references
├── 08-Templates/            # Obsidian templates
└── 99-Attachments/           # Images, PDFs, audio files
```

## Git Sync Setup

1. Install the [Obsidian Git](https://github.com/denolehov/obsidian-git) plugin in Obsidian.
2. Configure backup interval (e.g., every 10 minutes).
3. Set commit message template: `vault backup: {{date}}`.

## AI Integration

### Claude Code

Claude Code automatically reads `.claude/CLAUDE.md` when opening this repository. It knows your vault structure, naming conventions, and how to interact with notes.

Key commands:
```bash
# Analyze today's notes and suggest links
claude "Review 01-Daily-Notes/2025-01-15.md and suggest 3 permanent notes to create."

# Structure a meeting note
claude "Structure 02-Meetings/2025-01-15-Product-Review.md with action items and owners."

# Find orphaned notes and suggest links
claude "Find all notes in 05-Permanent-Notes/ with zero backlinks and suggest connections."
```

### Kimi Code (Desktop IDE)

Kimi Code reads `.kimi/instructions.md` when loading this workspace. The file defines the vault as a knowledge base and provides query patterns.

## Automation (GitHub Actions)

| Workflow | Trigger | What It Does |
|---|---|---|
| `auto-linker.yml` | Schedule (daily), manual | Finds orphaned notes, analyzes content, opens PRs with suggested links/tags |
| `meeting-processor.yml` | On push to `02-Meetings/` | Structures raw meeting notes, extracts action items, updates project MOCs |

## Token Optimization Rules (For AI)

1. **Read MOCs first** — Always check `04-MOCs/` before asking about a topic.
2. **Filter by frontmatter** — Use `tags`, `status`, and `project` YAML fields to narrow scope.
3. **Respect atomicity** — One idea per note. If a note is >500 words, suggest splitting.
4. **Prefer links over folders** — Use `[[Note]]` links to build the graph; folders are for organization, not discovery.
5. **Update MOCs after changes** — When you create or modify a note, update the relevant MOC so the index stays current.

## Quick Start

1. Clone this repo: `git clone https://github.com/Corin948/obsidian-ai-vault.git`
2. Open the folder as a vault in Obsidian.
3. Install Obsidian Git plugin and configure sync.
4. Open the folder in Kimi Code IDE.
5. Open the folder in Claude Code CLI.

---
*Built for AI-augmented knowledge management.*
