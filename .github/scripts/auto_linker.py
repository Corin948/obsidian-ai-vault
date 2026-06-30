#!/usr/bin/env python3
"""
Auto-Linker Script

Finds orphaned notes (0 backlinks) and suggests:
1. Related notes to link to (based on tag overlap and content similarity)
2. Tags that should be added based on content analysis
3. MOCs that should be updated

Updates notes in-place and creates a summary report.
"""

import os
import re
import yaml
from pathlib import Path
from collections import defaultdict

VAULT_ROOT = Path(".")
EXCLUDE_DIRS = {".git", ".github", ".obsidian", ".claude", ".kimi", "99-Attachments", "08-Templates"}

def get_all_notes():
    """Find all markdown files in the vault."""
    notes = []
    for path in VAULT_ROOT.rglob("*.md"):
        if any(part in EXCLUDE_DIRS for part in path.parts):
            continue
        if path.name == "README.md":
            continue
        notes.append(path)
    return notes

def parse_frontmatter(content):
    """Extract YAML frontmatter from a note."""
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            try:
                return yaml.safe_load(parts[1]), parts[2]
            except yaml.YAMLError:
                return {}, content
    return {}, content

def extract_links(content):
    """Extract all Obsidian wikilinks from content."""
    pattern = r'\[\[(.*?)\]\]'
    return re.findall(pattern, content)

def extract_tags_from_content(content):
    """Extract inline tags like #tag from content."""
    pattern = r'#([a-zA-Z0-9_-]+)'
    return set(re.findall(pattern, content))

def calculate_tag_overlap(note1_tags, note2_tags):
    """Calculate Jaccard similarity between two tag sets."""
    if not note1_tags or not note2_tags:
        return 0.0
    intersection = note1_tags & note2_tags
    union = note1_tags | note2_tags
    return len(intersection) / len(union)

def suggest_links(orphan_path, orphan_tags, orphan_content, all_notes_data):
    """Suggest the top 3 most related notes for an orphaned note."""
    suggestions = []
    for note_path, note_data in all_notes_data.items():
        if note_path == orphan_path:
            continue
        overlap = calculate_tag_overlap(orphan_tags, note_data["tags"])
        if overlap > 0:
            suggestions.append((note_path, overlap, note_data["title"]))
    
    suggestions.sort(key=lambda x: x[1], reverse=True)
    return suggestions[:3]

def suggest_tags(content, existing_tags):
    """Simple keyword-based tag suggestion."""
    keywords = {
        "meeting": "meeting",
        "project": "project",
        "idea": "idea",
        "research": "research",
        "book": "book",
        "article": "article",
        "psychology": "psychology",
        "design": "design",
        "code": "code",
        "python": "python",
        "javascript": "javascript",
        "ai": "ai",
        "ml": "machine-learning",
        "learning": "learning",
        "habit": "habit",
        "productivity": "productivity",
        "writing": "writing",
    }
    content_lower = content.lower()
    suggested = set()
    for keyword, tag in keywords.items():
        if keyword in content_lower and tag not in existing_tags:
            suggested.add(tag)
    return list(suggested)

def update_note_with_suggestions(note_path, suggestions, new_tags):
    """Add suggested links and tags to a note."""
    content = note_path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(content)
    
    if not fm:
        return False
    
    if new_tags:
        existing_tags = set(fm.get("tags", []))
        existing_tags.update(new_tags)
        fm["tags"] = sorted(list(existing_tags))
        fm["auto-tags-added"] = new_tags
    
    suggestions_section = "\n\n## Suggested Connections (Auto-Generated)\n"
    for sugg_path, score, title in suggestions:
        link_name = sugg_path.stem.replace("-", " ").title()
        suggestions_section += f"- [[{link_name}]] — related by shared tags (similarity: {score:.2f})\n"
    
    if "## Suggested Connections" not in body:
        body += suggestions_section
    
    new_content = "---\n" + yaml.dump(fm, sort_keys=False, allow_unicode=True) + "---" + body
    note_path.write_text(new_content, encoding="utf-8")
    return True

def main():
    notes = get_all_notes()
    all_notes_data = {}
    
    for note_path in notes:
        content = note_path.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(content)
        links = extract_links(body)
        tags = set(fm.get("tags", []))
        tags.update(extract_tags_from_content(body))
        all_notes_data[note_path] = {
            "frontmatter": fm,
            "body": body,
            "links": links,
            "tags": tags,
            "title": note_path.stem.replace("-", " ").title(),
        }
    
    backlink_count = defaultdict(int)
    for note_data in all_notes_data.values():
        for link in note_data["links"]:
            for target_path in all_notes_data:
                if target_path.stem.lower() == link.lower().replace(" ", "-").split("|")[0]:
                    backlink_count[target_path] += 1
                    break
    
    orphans = []
    for note_path, count in backlink_count.items():
        if count == 0 and note_path.parent.name not in EXCLUDE_DIRS:
            orphans.append(note_path)
    
    for note_path, note_data in all_notes_data.items():
        if not note_data["links"] and note_path not in orphans:
            if note_path.parent.name not in EXCLUDE_DIRS:
                orphans.append(note_path)
    
    changes_made = False
    report_lines = [f"# Auto-Linker Report ({len(orphans)} orphaned notes found)\n"]
    
    for orphan_path in orphans:
        orphan_data = all_notes_data[orphan_path]
        suggestions = suggest_links(orphan_path, orphan_data["tags"], orphan_data["body"], all_notes_data)
        new_tags = suggest_tags(orphan_data["body"], orphan_data["tags"])
        
        if suggestions or new_tags:
            updated = update_note_with_suggestions(orphan_path, suggestions, new_tags)
            if updated:
                changes_made = True
            
            report_lines.append(f"\n## {orphan_path}")
            if suggestions:
                report_lines.append("Suggested links:")
                for s in suggestions:
                    report_lines.append(f"- {s[2]} ({s[1]:.2f})")
            if new_tags:
                report_lines.append(f"Suggested tags: {', '.join(new_tags)}")
    
    report_path = VAULT_ROOT / ".github" / "reports" / "auto_linker_report.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(report_lines), encoding="utf-8")
    
    if changes_made:
        print("changes=true")
    else:
        print("changes=false")

if __name__ == "__main__":
    main()
