---
name: obsidian-knowledge-curator
description: Turn one or more user-specified raw materials from this Obsidian vault into one polished, readable, image-friendly Obsidian Markdown note in 06_To_Classify. Use only when the user explicitly names the source file or files to curate. The skill may enrich or verify content with web search when useful, follows Obsidian Markdown syntax, and only enters image handling when the raw material contains useful images or image links.
---

# Obsidian Knowledge Curator

Turn specified raw material into one finished Obsidian note. The output always goes to `06_To_Classify/` for later human classification.

This skill does not import source material and does not clean up, delete, move, or archive raw inputs. The user handles cleanup manually.

## Use Only When

- The user explicitly names one or more source files, notes, or raw materials.
- The requested result is a polished Obsidian knowledge note.
- The output should be one review-ready Markdown note in `06_To_Classify/`.

If the user does not name the input file or files, ask for the exact source path instead of scanning `00_Inbox/` and guessing.

## Core Rules

- Output exactly one main note by default. Split only if the user asks or the sources clearly contain separate standalone topics.
- Write the final note to `06_To_Classify/<clear-note-title>.md`.
- Do not classify the finished note into `01_Projects/`, `02_Knowledge/`, or `03_Resources`.
- Do not delete, move, rename, archive, or clean source files.
- Use Chinese by default. Keep Proper Nouns and source titles in their original language.
- Preserve high-value examples, parameters, prompts, procedures, caveats, decisions, and failure fixes.
- Merge repeated or overlapping material instead of compressing it away.
- Design the note structure from the material. Do not force fixed body sections.
- Use relative vault paths in note content. Never write local absolute filesystem paths into the note.

## Workflow

1. Read only the source file or files the user specified.
2. Read `../obsidian-markdown/SKILL.md` before writing the final note. Treat it as the syntax contract.
3. Build a useful refined version of the material:
   - infer a clear structure when the raw material is messy, unstructured, or assembled from multiple sources
   - preserve the original material's useful substance, not necessarily its original order
   - remove capture noise, duplicated paragraphs, irrelevant boilerplate, and empty filler
   - keep enough detail that the final note can be used without reopening the raw source
4. Search official or primary sources when current facts, version behavior, conflicting claims, or missing context would materially improve the note. Proactive enrichment is allowed when it makes the note more useful, but do not turn every task into a research report.
5. If the raw material contains useful images, screenshots, diagrams, or image links, use the image handling rules below. If not, skip image handling entirely.
6. Write the note to `06_To_Classify/`.
7. Validate the output for readable structure, retained substance, valid Obsidian Markdown, valid YAML frontmatter, and working relative embeds.

## Note Shape

The body should be a refined, readable knowledge page. It can reorganize the source, combine multiple inputs, add helpful transitions, and use tables, callouts, diagrams, or images when they improve comprehension.

Required:

- valid YAML frontmatter at the top
- one H1 title
- substantive body sections shaped by the material
- `## Sources` only when web search or external sources were actually used

Recommended when useful:

- tables for comparisons, parameters, trade-offs, or version differences
- callouts for warnings, caveats, important conclusions, or unresolved private context
- code blocks for commands, prompts, templates, exact syntax, or examples
- Mermaid diagrams for processes, relationships, or decision flows
- local image embeds for information-bearing visuals from the source material

Do not add fixed sections just because this skill mentions them. 正文标准是图文并茂、阅读舒适、信息完整、可复用。

## Obsidian Markdown Essentials

Use `../obsidian-markdown/SKILL.md` as the source of truth. These essentials are repeated here to reduce mistakes during curation:

```markdown
[[Note Name]]
[[Note Name|Display Text]]
[[Note Name#Heading]]
![[05_Attachments/note-slug/image-01.webp]]
![[image.png|300]]

> [!note]
> Useful highlighted context.

> [!warning] Caveat
> Important limitation or risk.
```

Frontmatter must be valid YAML. Add only properties that help the note, such as `title`, `tags`, `aliases`, `source`, or `status`; do not invent a large schema.

Use wikilinks for internal vault notes and standard Markdown links for external URLs.

## Web Search

Web search is allowed when it improves the final note:

- use official docs, primary sources, papers, or original project pages when possible
- resolve version conflicts and outdated claims instead of leaving them as generic uncertainty
- add `## Sources` only if external sources were used
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
- external sources used, if any
- localized or optimized attachment files, if any

Do not report source cleanup because this skill never performs cleanup.

## Bundled Resources

- `references/image-assets.md` - optional image localization and compression guidance.
- `scripts/optimize_images.py` - optional raster image optimization helper.
- `evals/evals.json` - behavior checks for this workflow.
