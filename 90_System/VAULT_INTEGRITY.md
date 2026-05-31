# Vault Integrity System

`vault_integrity.py` is the vault maintenance gate for references, metadata paths, and cross-platform file safety.

Use it when you move, rename, delete, classify, import, or clean notes. Do not rely on memory after reorganizing files.

## Commands

Run from the vault root:

```powershell
python -X utf8 90_System\vault_integrity.py check
python -X utf8 90_System\vault_integrity.py check --strict
python -X utf8 90_System\vault_integrity.py suggest
python -X utf8 90_System\vault_integrity.py suggest --json
python -X utf8 90_System\vault_integrity.py fix --safe
python -X utf8 90_System\vault_integrity.py move "06_To_Classify/example.md" "02_Knowledge/AIGC/example.md"
python -X utf8 90_System\vault_integrity.py delete-check "00_Inbox/example.md"
```

`check` is read-only.

`suggest` is read-only and prints candidate repairs.

`fix --safe` writes files, but only for deterministic high-confidence wikilink fixes and configured JSON metadata path fixes. It does not rewrite concept links, fuzzy matches, or frontmatter provenance paths.

`move` moves a vault file and updates inbound wikilinks plus configured JSON metadata paths.

## What Is Checked

- Missing wikilinks and embeds in real vault note roots.
- Local Markdown links to missing files.
- Frontmatter path-like values that are absolute or missing.
- Stale paths in configured JSON metadata reports.
- Case collisions that can fail across Windows/macOS.
- Filename characters and trailing spaces/dots that are unsafe across systems.

The scanner intentionally excludes `.codex`, `.obsidian`, `.smart-env`, `.git`, and `90_System/__pycache__`, so skill documentation examples are not treated as real note links.

## Inbox Cleanup

Before deleting or emptying `00_Inbox`, run:

```powershell
python -X utf8 90_System\vault_integrity.py check
python -X utf8 90_System\vault_integrity.py delete-check "00_Inbox/file-to-delete.md" --strict
```

If a planned deletion is still linked from durable notes, `check` reports the source file and line that will break. Update the links or use `move` before deletion.

## Classification Moves

When moving a reviewed note from `06_To_Classify` into `02_Knowledge` or another durable folder, prefer:

```powershell
python -X utf8 90_System\vault_integrity.py move "06_To_Classify/note.md" "02_Knowledge/Topic/note.md"
```

This keeps inbound wikilinks aligned with the new path.

## Safe vs Manual Fixes

Safe automatic fixes:

- Old target has a unique matching file stem.
- Old target has a unique matching alias/title.
- Git rename detection reports a single old-to-new path.
- Configured JSON metadata points to the same unique moved file.

Manual review required:

- Fuzzy title matches.
- Multiple candidates.
- Missing concept pages such as `[[LoRA]]` or `[[Quantization]]`.
- Stale metadata paths where the new destination is semantic rather than exact.

Add intentional concept links to `allowed_virtual_links` in `90_System/vault_integrity_config.json`.

## Git Hook

Enable the local hook:

```powershell
git config core.hooksPath 90_System/git-hooks
```

The `pre-commit` hook runs:

```powershell
python -X utf8 90_System/vault_integrity.py check --strict --staged
```

Strict mode exits non-zero when blocking issues exist, preventing commits that would lock in broken references or cross-platform path problems.

## Cross-System Rules

- Store internal paths as vault-relative paths with `/`.
- Do not store `C:\Users\...` or other machine-specific paths in durable note frontmatter.
- Avoid filenames that differ only by case.
- Avoid Windows-invalid characters: `< > : " | ? *`.
- Avoid trailing spaces or dots in file/folder names.

## Maintenance Pattern

1. Import or curate notes.
2. Run `check`.
3. Review `suggest`.
4. Run `fix --safe` only if suggestions are deterministic.
5. Move/classify through `move`.
6. Run `check --strict` before committing.
