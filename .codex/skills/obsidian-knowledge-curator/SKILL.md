---
name: obsidian-knowledge-curator
description: Turn one or more user-specified raw materials from 00_Inbox into one or more polished, readable, image-friendly Obsidian Markdown notes in 06_To_Classify, then delete the specified raw notes after every output, visual asset, and reference check passes. Use only when the user explicitly names the source file or files to curate. The skill preserves unique reusable substance while compressing noise and duplicates, may enrich or verify content with web search when useful, follows Obsidian Markdown syntax, and preserves useful source visuals.
---

# Obsidian Knowledge Curator

Turn specified raw material into one or more finished Obsidian notes. Every output goes to `06_To_Classify/` for later human classification.

This skill turns explicitly named `00_Inbox/` raw notes into one or more review-ready notes, then moves the raw notes to the Obsidian trash after validation.

## Use Only When

- The user explicitly names one or more source files, notes, or raw materials.
- Every source is a Markdown note under `00_Inbox/`.
- The requested result is a polished Obsidian knowledge note.
- The output should be one or more review-ready Markdown notes in `06_To_Classify/`.

If the user does not name the input file or files, ask for the exact source path instead of scanning `00_Inbox/` and guessing.

## Core Rules

- Cluster source units by retrieval intent before drafting. Write one note per independent, reusable cluster; produce one or more notes as the material requires.
- Keep same-question conflicts in one note when source differences can be scoped, compared, or corrected. Split only when clusters answer different reader questions and each can stand alone with its own title and body.
- Write every final note to `06_To_Classify/<clear-note-title>.md`.
- Do not classify the finished note into `01_Projects/`, `02_Knowledge/`, or `03_Resources`.
- For every useful source image, screenshot, diagram, or accessible image link, localize a copy or optimized derivative to `05_Attachments/<note-slug>/`, embed it near the relevant explanation, and include a caption or observation.
- Delete every specified raw note only after every output, required visual asset, and deletion preflight succeeds. Use `obsidian delete path="<source-path>"`; do not use `permanent`.
- If output writing, validation, or any deletion preflight fails, leave every source note untouched and report the failure.
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
   - useful visuals, their source path or URL, and whether they can be localized
5. Group the inventoried units by retrieval intent. Merge units that answer the same reader question. Split units only when they form independent, reusable topics. Record same-topic conflicts for comparison or correction within the relevant note.
6. Build one useful refined note per cluster:
   - infer a clear structure when the raw material is messy, unstructured, or assembled from multiple sources
   - preserve unique useful substance, not necessarily the original order or wording
   - compress repeated, noisy, irrelevant, boilerplate, and empty material without losing useful distinctions
   - keep long but valuable details in tables, code blocks, folded callouts, or appendix-like sections when they would interrupt the main reading path
   - keep enough detail that the final note can be used without reopening the raw source
7. Search official or primary sources when current facts, version behavior, conflicting claims, or missing context would materially improve the notes. Proactive enrichment is allowed when it makes the notes more useful, but do not turn every task into a research report.
8. Localize and embed every useful source visual. Prefer an optimized derivative, but embed a local original when optimization would lose it or fail. If a material visual cannot be retained, do not delete the raw notes.
9. Write every note to `06_To_Classify/` without durable references to transient input paths.
10. Audit every output for cluster coverage, transient input references, language quality, knowledge value, valid Obsidian Markdown, valid YAML frontmatter, working relative embeds, and usable local visual assets.
11. From the vault root, run `python -X utf8 90_System/vault_integrity.py check --strict`. Fix any issue caused by the new notes or assets before continuing. Existing unrelated issues that make this command fail block deletion.
12. Run `python -X utf8 90_System/vault_integrity.py delete-check "<source-path>" --strict` for every source. If every command succeeds, run `obsidian delete path="<source-path>"` for every source.

## Source Deletion

Deletion is part of a successful curation, not a separate cleanup phase. The source notes go to the Obsidian trash and remain recoverable there. Never delete only some sources from a multi-source curation: a failed output, visual-asset check, or deletion preflight leaves every source in place.

## Transient Inputs And Sources

The user-specified `00_Inbox/` notes are raw material for this curation pass, not stable citations. They are deleted after every finished note, useful visual, and deletion preflight succeeds.

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
- Partitioning: each output answers one coherent reader question; independent topics are not forced into one note, and same-topic conflicts are compared or corrected instead of silently split.
- Transient references: the finished note contains no durable links, frontmatter values, or `## Sources` entries pointing to `00_Inbox/` raw inputs.
- Visuals: every useful source visual is embedded near its explanation from a valid local path, or its retention failure blocks source deletion.
- Language: Chinese prose is natural and precise; translated or merged material does not create grammar errors or vague claims.
- Value: the note is more navigable, accurate, and reusable than the raw source, not merely shorter.
- Source removal: every specified `00_Inbox/` source has passed `delete-check --strict` and was moved to the Obsidian trash; the finished note has no reverse link to those sources.

## Note Shape

Each body should be a refined, readable knowledge page. It can reorganize source material within its cluster, add helpful transitions, and use tables, callouts, diagrams, or images when they improve comprehension.

Use `knowledge/Obsidian Markdown Visual Curation Guidelines.md` for detailed note-shape and visual rhythm decisions. Keep this section short so the skill stays compact.

Minimum requirements:

- valid YAML frontmatter at the top
- one H1 title per output
- substantive body sections shaped by the material
- `## Sources` only when web search or external sources were actually used

Do not add fixed sections just because this skill mentions them. 正文标准是阅读舒适、信息完整、密度更高、可复用；有信息价值的图片才需要图文并茂。

## Obsidian Markdown Essentials

Use `../obsidian-markdown/SKILL.md` as the source of truth. Do not duplicate a separate Obsidian syntax guide inside this skill.

Frontmatter must be valid YAML. Add only properties that help the note, such as `title`, `tags`, or `aliases`; do not invent a large schema. Do not use `source` or similar provenance fields for transient vault inputs such as `00_Inbox/...`.

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

Image handling is required when the specified raw material contains useful images, screenshots, diagrams, or accessible image links.

- Do not fetch decorative images just to make the note look richer.
- Preserve and localize every visual that explains the content. Embed it adjacent to the explanation with a caption or observation.
- Use `references/image-assets.md` for image handling guidance.
- Use `scripts/optimize_images.py` for raster optimization when local images would otherwise be too large.
- Embed local images with Obsidian syntax such as `![[05_Attachments/note-slug/image-01.webp]]`.

## Final Response

Report only:

- created note paths
- deleted source paths
- external sources used, if any
- localized or optimized attachment files

If any deletion preflight failed, state that the sources were retained.

## Bundled Resources

- `knowledge/Obsidian Markdown Visual Curation Guidelines.md` - detailed note-shape and visual curation guidance.
- `references/image-assets.md` - optional image localization and compression guidance.
- `scripts/optimize_images.py` - optional raster image optimization helper.
- `evals/evals.json` - behavior checks for this workflow.
