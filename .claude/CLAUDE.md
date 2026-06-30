This is a hierarchical Obsidian knowledge vault. Claude Code should treat this as a living knowledge graph, not just a folder of text files.

## Vault Architecture

- **00-Inbox/** — Drop zone. Notes here are unprocessed.
- **01-Daily-Notes/** — Daily journals. Format: `YYYY-MM-DD.md`.
- **02-Meetings/** — Meeting notes. Format: `YYYY-MM-DD-Topic.md`. May contain raw transcripts.
- **03-Projects/** — Active projects. Each has its own MOC.
- **04-MOCs/** — Maps of Content (index notes). These are the AI's PRIMARY entry points.
- **05-Permanent-Notes/** — Atomic Zettelkasten notes. One idea per note. Self-contained.
- **06-Fleeting-Notes/** — Temporary captures. Stale after 7 days.
- **07-Resources/** — Book/article summaries.
- **08-Templates/** — Obsidian templates.
- **99-Attachments/** — Images, PDFs, audio.

## Naming Conventions

- **Dates:** Always `YYYY-MM-DD` format in filenames and frontmatter.
- **Titles:** Descriptive, kebab-case for filenames. Example: `cognitive-load-theory.md`.
- **MOCs:** Suffix with `-MOC`. Example: `machine-learning-MOC.md`.
- **Tags:** Use kebab-case in YAML frontmatter. Example: `tags: [permanent-note, psychology]`.

## YAML Frontmatter Rules

Every note must have YAML frontmatter:
```yaml
---
date: YYYY-MM-DD
tags: [tag1, tag2]
status: seedling | budding | evergreen | unprocessed | archived
---
```

- **seedling:** New idea, undeveloped.
- **budding:** Has some connections, being developed.
- **evergreen:** Mature, heavily linked, self-contained.
- **unprocessed:** In inbox or fleeting, needs work.
- **archived:** No longer relevant but kept for reference.

## Link Syntax

- Use Obsidian wikilinks: `[[Note Title]]` or `[[Note Title|Display Text]]`.
- Prefer links over folders for relationships.
- Every permanent note should have at least 3 outbound links.

## MOC Rules (Critical for Token Efficiency)

1. **MOCs are indexes.** They contain metadata, lists of related notes, and brief descriptions.
2. **AI should ALWAYS read the MOC first** when asked about a topic.
3. **Update MOCs after creating/modifying notes.** A stale MOC is worse than no MOC.
4. **MOCs should fit on one screen.** If longer, split into sub-MOCs.

## How to Modify Notes

- Preserve all YAML frontmatter.
- Preserve Obsidian link syntax `[[...]]`.
- When splitting a note, update the original to point to the new note.
- When creating a new note, update the relevant MOC.

## Automation Rules

- GitHub Actions process meeting notes and orphaned notes. Do not conflict with the automation.
- If a note has `status: unprocessed`, it's fair game for AI to process and restructure.
- Action items extracted by AI should use `- [ ] Task description @owner` format.
