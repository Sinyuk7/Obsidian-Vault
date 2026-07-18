---
name: obsidian-knowledge-curator
description: Turn one or more user-specified raw materials from this Obsidian vault into one polished, readable, image-friendly Obsidian Markdown note in 06_To_Classify. Use only when the user explicitly names the source file or files to curate. For 00_Inbox inputs, add an auditable curation marker that identifies the finished note without deleting the raw material. The skill preserves unique reusable substance while compressing noise and duplicates, may enrich or verify content with web search when useful, follows Obsidian Markdown syntax, and only enters image handling when the raw material contains useful images or image links.
---

# Obsidian Knowledge Curator

Turn specified raw material into one finished Obsidian note. The output always goes to `06_To_Classify/` for later human classification.

This skill does not import, delete, move, or archive raw inputs. It marks successfully curated `00_Inbox/` inputs so a separate, user-confirmed cleanup pass can identify them.

## Use Only When

- The user explicitly names one or more source files, notes, or raw materials.
- The requested result is a polished Obsidian knowledge note.
- The output should be one review-ready Markdown note in `06_To_Classify/`.

If the user does not name the input file or files, ask for the exact source path instead of scanning `00_Inbox/` and guessing.

## Core Rules

- Output exactly one main note by default. Split only if the user asks or the sources clearly contain separate standalone topics.
- Write the final note to `06_To_Classify/<clear-note-title>.md`.
- Do not classify the finished note into `01_Projects/`, `02_Knowledge/`, or `03_Resources`.
- Do not delete, move, rename, archive, or otherwise clean source files.
- After the finished note has been written and validated, add or update only the YAML frontmatter of every `00_Inbox/` source with `curation_status: curated`, `curated_note: "[[06_To_Classify/<clear-note-title>]]"`, and `curated_at: "YYYY-MM-DD"`.
- Preserve source body text and existing unrelated frontmatter. Do not add these tracking properties to sources outside `00_Inbox/`.
- If an Inbox source already has `curation_status: curated`, verify its `curated_note` first. Do not overwrite that marker or create a duplicate curation output without the user's direction.
- Use Chinese by default. Keep Proper Nouns and source titles in their original language.
- Treat `00_Inbox/` inputs as transient raw materials that may be deleted later; do not create durable links or frontmatter source references to them.
- Create a higher-density note, not a shorter-at-any-cost summary.
- Preserve unique high-value examples, parameters, prompts, procedures, caveats, decisions, version differences, and failure fixes.
- Compress only duplicate, noisy, irrelevant, boilerplate, or superseded material.
- Merge repeated or overlapping material into clearer reusable guidance instead of dropping useful distinctions.
- Design the note structure from the material. Do not force fixed body sections.
- Use relative vault paths in note content. Never write local absolute filesystem paths into the note.

## Workflow

1. Read only the source file or files the user specified.
2. Read `../obsidian-markdown/SKILL.md` before writing the final note. Treat it as the syntax contract.
3. Read `knowledge/Obsidian Markdown Visual Curation Guidelines.md` before shaping the final note. Treat it as the visual curation guide, not as a second syntax contract.
4. Inventory the source's reusable units before drafting:
   - concepts, claims, examples, parameters, prompts, procedures, caveats, decisions, version differences, failure fixes, open questions, and useful visuals
   - duplicated or overlapping units that can be merged
   - noisy, irrelevant, boilerplate, empty, or superseded material that can be removed
   - gaps, conflicts, or outdated claims that would benefit from official or primary-source verification
5. Build a useful refined version of the material:
   - infer a clear structure when the raw material is messy, unstructured, or assembled from multiple sources
   - preserve unique useful substance, not necessarily the original order or wording
   - compress repeated, noisy, irrelevant, boilerplate, and empty material without losing useful distinctions
   - keep long but valuable details in tables, code blocks, folded callouts, or appendix-like sections when they would interrupt the main reading path
   - keep enough detail that the final note can be used without reopening the raw source
6. Search official or primary sources when current facts, version behavior, conflicting claims, or missing context would materially improve the note. Proactive enrichment is allowed when it makes the note more useful, but do not turn every task into a research report.
7. If the raw material contains useful images, screenshots, diagrams, or image links, use the image handling rules below. If not, skip image handling entirely.
8. Write the note to `06_To_Classify/` without durable references to transient input paths.
9. Audit the output for source coverage, transient input references, language quality, knowledge value, valid Obsidian Markdown, valid YAML frontmatter, and working relative embeds.
10. After the output is valid, mark each `00_Inbox/` input in its YAML frontmatter with `curation_status`, `curated_note`, and `curated_at`. Do not mark a source if writing or validating the output failed.
11. From the vault root, run `python -X utf8 90_System\vault_integrity.py check` after writing the note and markers. Fix any issue caused by the new note or marker before reporting completion. Existing unrelated vault issues may be reported separately.

## Inbox Tracking And Cleanup

The source marker is an audit record, not automatic permission to delete. It lets the user see exactly which Inbox materials have a verified curated output while keeping the finished note independent of disposable inputs.

- Find marked candidates with `rg -l '^curation_status:\s*curated\s*$' 00_Inbox`.
- Before deleting any candidate, confirm its `curated_note` resolves, run `python -X utf8 90_System\vault_integrity.py check --strict`, then run `python -X utf8 90_System\vault_integrity.py delete-check "<source-path>" --strict`.
- Delete only in a separate, explicit user-confirmed cleanup request. Never delete as part of curation, even when the user asks for it in the same prompt.
- If the source marker cannot be safely written, report the source as unmarked. Do not claim it is ready for cleanup.

## Transient Inputs And Sources

The user-specified vault files are raw material for this curation pass, not stable citations. This is especially true for `00_Inbox/`, which is a temporary capture area that receives a source-side curation marker and may be deleted later in a separate cleanup pass.

- Do not add `00_Inbox/...` paths to frontmatter properties such as `source`, `sources`, `origin`, or `related`.
- Do not create wikilinks or Markdown links to `00_Inbox/...` files in the final note.
- Do not include `00_Inbox/...` files in `## Sources`; that section is only for external sources actually used during web search or source enrichment.
- Do not add a generic "based on raw notes" section that names transient input files.
- It is acceptable to mention in the final response that the note was created from specified inputs, but do not encode those transient paths into the durable note.
- If a raw input is not transient and the user explicitly asks to preserve provenance, prefer a stable external URL, publication metadata, or a durable vault note outside `00_Inbox/`; otherwise omit source provenance rather than linking disposable material.

## Curation Quality Standard

The goal is faithful refinement: the final note may be shorter than the source, but its information density and reuse value should be higher. Do not reduce high-signal material to a terse outline unless the source itself is genuinely low signal.

Use these rules when deciding what to keep, merge, compress, or remove:

- Keep unique examples, parameter ranges, prompt templates, commands, procedures, caveats, decisions, source-specific observations, version differences, failure modes, and fixes.
- Merge duplicate or overlapping explanations into a clearer statement, while preserving meaningful edge cases and distinctions.
- Compress low-value background, repeated setup, copied navigation, verbose transitions, repeated claims, and capture artifacts.
- Remove only material that is duplicate, irrelevant, empty, decorative, obsolete after correction, or not useful for future reuse.
- For long high-value material, preserve it outside the main flow with folded `example` callouts, tables, code blocks, diagrams, or short appendix-like sections.
- The opening summary can be brief, but it must not replace the reusable body detail.

Before considering the note finished, check:

- Coverage: each unique high-value source unit is retained, merged intentionally, corrected with a source, or removed for a clear reason.
- Transient references: the finished note contains no durable links, frontmatter values, or `## Sources` entries pointing to `00_Inbox/` raw inputs.
- Language: Chinese prose is natural and precise; translated or merged material does not create grammar errors or vague claims.
- Value: the note is more navigable, accurate, and reusable than the raw source, not merely shorter.
- Inbox tracking: every successfully curated `00_Inbox/` source has valid `curation_status`, `curated_note`, and `curated_at` frontmatter; the finished note has no reverse link to those sources.

## Note Shape

The body should be a refined, readable knowledge page. It can reorganize the source, combine multiple inputs, add helpful transitions, and use tables, callouts, diagrams, or images when they improve comprehension.

Use `knowledge/Obsidian Markdown Visual Curation Guidelines.md` for detailed note-shape and visual rhythm decisions. Keep this section short so the skill stays compact.

Minimum requirements:

- valid YAML frontmatter at the top
- one H1 title
- substantive body sections shaped by the material
- `## Sources` only when web search or external sources were actually used

Do not add fixed sections just because this skill mentions them. 正文标准是阅读舒适、信息完整、密度更高、可复用；有信息价值的图片才需要图文并茂。

## Obsidian Markdown Essentials

Use `../obsidian-markdown/SKILL.md` as the source of truth. Do not duplicate a separate Obsidian syntax guide inside this skill.

Frontmatter must be valid YAML. Add only properties that help the note, such as `title`, `tags`, `aliases`, or `status`; do not invent a large schema. Do not use `source` or similar provenance fields for transient vault inputs such as `00_Inbox/...`.

Use wikilinks for internal vault notes and standard Markdown links for external URLs.

## Web Search

Web search is allowed when it improves the final note:

- use official docs, primary sources, papers, or original project pages when possible
- use search to resolve identified gaps, version conflicts, outdated claims, missing context, or externally verifiable facts
- incorporate search results into the note as corrections, context, constraints, comparisons, or caveats; do not just append links
- add `## Sources` only if external sources were used
- never use `## Sources` for temporary vault inputs such as `00_Inbox/...`
- keep source citations concise; the finished note should still be a personal knowledge page, not an academic report

## Images

Image handling is conditional, not core. Enter this path only when the specified raw material contains useful images, screenshots, diagrams, or image links.

- Do not fetch decorative images just to make the note look richer.
- Preserve and localize visuals that explain the content.
- Use `references/image-assets.md` for image handling guidance.
- Use `scripts/optimize_images.py` for raster optimization when local images would otherwise be too large.
- Embed local images with Obsidian syntax such as `![[05_Attachments/note-slug/image-01.webp]]`.

## Final Response

Report only:

- created note path
- marked Inbox source paths, if any
- external sources used, if any
- localized or optimized attachment files, if any

State that source cleanup was not performed. If an Inbox source could not be marked, state that clearly.

## Bundled Resources

- `knowledge/Obsidian Markdown Visual Curation Guidelines.md` - detailed note-shape and visual curation guidance.
- `references/image-assets.md` - optional image localization and compression guidance.
- `scripts/optimize_images.py` - optional raster image optimization helper.
- `evals/evals.json` - behavior checks for this workflow.
