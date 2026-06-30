You are working inside an Obsidian knowledge vault. Treat this workspace as a living knowledge graph, not just a folder of markdown files.

## Workspace Structure

- **00-Inbox/** — Unprocessed notes. Fair game for restructuring.
- **01-Daily-Notes/** — Daily journals (`YYYY-MM-DD.md`).
- **02-Meetings/** — Meeting notes (`YYYY-MM-DD-Topic.md`). Raw transcripts may be present.
- **03-Projects/** — Active projects with their own MOCs.
- **04-MOCs/** — Maps of Content (indexes). ALWAYS check these first when exploring a topic.
- **05-Permanent-Notes/** — Atomic notes (one idea per note).
- **06-Fleeting-Notes/** — Temporary (stale after 7 days).
- **07-Resources/** — Book/article summaries.
- **08-Templates/** — Templates for new notes.
- **99-Attachments/** — Media files.

## When Helping the User

1. **Preserve frontmatter** — Every `.md` file has YAML frontmatter. Never delete it.
2. **Preserve links** — Use `[[Note Title]]` syntax. Suggest links to related notes.
3. **Suggest atomicity** — If a note is too long (>500 words), suggest splitting it.
4. **Update MOCs** — When creating a new note, remind the user to update the relevant MOC.
5. **Use kebab-case tags** — `tags: [machine-learning, psychology]` in frontmatter.

## Response Style

- Be concise. This is a knowledge vault, not a chatbot playground.
- When suggesting edits, show the exact text to change.
- When suggesting new notes, provide the full YAML frontmatter and a template.
- Prefer linking over explaining. If the user asks about a concept that exists as a note, suggest they read the note first.
