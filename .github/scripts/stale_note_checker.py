#!/usr/bin/env python3
"""
Stale Note Checker

Finds notes that have been unprocessed for too long:
- Inbox notes > 7 days
- Fleeting notes > 7 days
- Meeting notes with status: unprocessed > 3 days

Creates a report in .github/reports/stale_notes.md
"""

import os
import yaml
from pathlib import Path
from datetime import datetime, timedelta

VAULT_ROOT = Path(".")
ISSUES_FILE = VAULT_ROOT / ".github" / "reports" / "stale_notes.md"

def parse_frontmatter(content):
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            try:
                return yaml.safe_load(parts[1]), parts[2]
            except yaml.YAMLError:
                return {}, content
    return {}, content

def get_note_date(note_path):
    content = note_path.read_text(encoding="utf-8")
    fm, _ = parse_frontmatter(content)
    
    date_str = fm.get("date")
    if date_str:
        try:
            return datetime.strptime(str(date_str), "%Y-%m-%d")
        except ValueError:
            pass
    
    stem = note_path.stem
    try:
        return datetime.strptime(stem[:10], "%Y-%m-%d")
    except ValueError:
        pass
    
    stat = note_path.stat()
    return datetime.fromtimestamp(stat.st_mtime)

def main():
    now = datetime.now()
    stale_notes = []
    
    for note_path in (VAULT_ROOT / "00-Inbox").glob("*.md"):
        if note_path.name == "README.md":
            continue
        date = get_note_date(note_path)
        if (now - date).days > 7:
            stale_notes.append((note_path, date, "Inbox > 7 days"))
    
    for note_path in (VAULT_ROOT / "06-Fleeting-Notes").glob("*.md"):
        if note_path.name == "README.md":
            continue
        date = get_note_date(note_path)
        if (now - date).days > 7:
            stale_notes.append((note_path, date, "Fleeting > 7 days"))
    
    for note_path in (VAULT_ROOT / "02-Meetings").glob("*.md"):
        if note_path.name == "README.md":
            continue
        content = note_path.read_text(encoding="utf-8")
        fm, _ = parse_frontmatter(content)
        if fm.get("status") == "unprocessed":
            date = get_note_date(note_path)
            if (now - date).days > 3:
                stale_notes.append((note_path, date, "Meeting unprocessed > 3 days"))
    
    ISSUES_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    if stale_notes:
        report_lines = [f"# Stale Notes Report ({len(stale_notes)} found)\n\n"]
        for path, date, reason in stale_notes:
            days_old = (now - date).days
            report_lines.append(f"- **{path}** — {reason} (created {date.strftime('%Y-%m-%d')}, {days_old} days ago)\n")
        
        report_lines.append("\n## Suggested Actions\n")
        report_lines.append("- Inbox/Fleeting notes: Process into permanent notes or discard\n")
        report_lines.append("- Meeting notes: Run `meeting_processor.yml` or structure manually\n")
        
        ISSUES_FILE.write_text("".join(report_lines), encoding="utf-8")
        print(f"Found {len(stale_notes)} stale notes. Report written to {ISSUES_FILE}")
    else:
        ISSUES_FILE.write_text("# Stale Notes Report\n\nNo stale notes found! 🎉\n", encoding="utf-8")
        print("No stale notes found.")

if __name__ == "__main__":
    main()
