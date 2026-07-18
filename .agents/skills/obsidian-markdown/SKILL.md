---
name: obsidian-markdown
description: Create, restructure, and polish notes intended for Obsidian with vault-consistent properties, wikilinks, embeds, callouts, block references, and native Markdown. Use when creating or editing Obsidian .md notes, improving note structure or readability, converting supplied material into an Obsidian note, or working with Obsidian-specific syntax. Inspect and preserve existing vault conventions before introducing properties, tags, aliases, links, folders, attachment paths, or CSS classes. Do not use for generic Markdown, YAML frontmatter, documentation, or static-site content not intended for Obsidian.
---

# Obsidian Note Authoring

Create notes that are accurate, readable, maintainable, and consistent with the active vault. Treat Obsidian syntax as semantic tools, not decoration.

## Core Rules

- Preserve facts, terminology, citations, uncertainty, and requested scope.
- Prefer clear native Markdown before Obsidian-specific syntax.
- Add properties, links, embeds, callouts, block IDs, tags, or CSS classes only when each has a concrete organizational or reading benefit.
- Match existing vault conventions. Do not introduce a competing schema or visual system without an explicit request.
- Do not invent existing notes, aliases, headings, block IDs, attachment paths, citations, dates, or property values.
- Do not add empty sections or placeholders unless creating a reusable template.
- Do not force every note into the same shape.

## Workflow

### 1. Determine the task mode

Classify the request as one or more of: create, edit, restructure, polish, convert supplied material, merge, split, template, repair syntax, or add vault-aware metadata.

Preserve valid structure and conventions when editing an existing note unless the user requests a redesign.

### 2. Inspect vault conventions

When the vault is accessible and the change is structural, read applicable `AGENTS.md`, nearby notes in the target folder, and relevant templates before drafting. Inspect only enough material to establish:

- property names and types;
- filename, title, and heading conventions;
- date, tag, alias, link, attachment, callout, and CSS-class conventions.

For an indexed code or code-documentation task, use CodeGraph before text search when `.codegraph/` exists. Do not use CodeGraph for ordinary note formatting.

When no vault context is available, use minimal portable Markdown. Avoid speculative properties, links, embeds, and metadata.

### 3. Choose a note shape

Choose a fitting archetype before choosing components. Use archetypes as optional modules, never mandatory templates. Read [NOTE-ARCHETYPES.md](references/NOTE-ARCHETYPES.md) when structure is unclear.

### 4. Design information hierarchy

Identify the note's purpose, central conclusion or question, major groups, supporting evidence, practical implications, and unresolved questions or actions.

- Use headings that name real content. Do not skip heading levels.
- Use paragraphs for explanation, lists for discrete items, tables for aligned comparison, and code blocks for literal text or code.
- For a substantive note, prefer an opening summary only when it improves retrieval and matches vault practice. Do not force a summary callout into short notes, captures, or templates.
- Use horizontal rules only for a meaningful mode change and only when they match local practice.

### 5. Add properties selectively

Preserve the existing property schema. Add properties only for established search, Bases, templates, publishing, project tracking, or classification needs. Keep values small, atomic, and machine-readable. Read [PROPERTIES.md](references/PROPERTIES.md) before adding or changing properties.

### 6. Add links and embeds carefully

Create wikilinks only for meaningful concepts and known vault targets. Locate the actual target note, heading, alias, or attachment before linking when the vault is accessible.

Do not wikilink every noun. Create unresolved links only when the user requests prospective links or the concept clearly merits a future standalone note. Use an embed only when inline content improves comprehension; otherwise prefer a normal link. Read [EMBEDS.md](references/EMBEDS.md) and [SYNTAX-CAVEATS.md](references/SYNTAX-CAVEATS.md) for edge cases.

### 7. Use semantic visual components

Use callouts for summaries, limitations, examples, questions, actions, and quotations that should sit outside the main narrative. Use zero to three callouts in a typical note unless an established repeated semantic system needs more.

Use bold for key terms or conclusions, highlight for rare review points, inline code for literal commands or syntax, and blockquotes for quotations. Avoid decorative emojis, consecutive highlighted paragraphs, nested callouts, and callouts around ordinary prose. Read [CALLOUTS.md](references/CALLOUTS.md) for component choices.

Use Mermaid only when a workflow, dependency, decision, timeline, or relationship is harder to understand in prose or a compact table. Use Dataview only when the vault already uses it or the user explicitly requests it; do not assume plugins are installed.

### 8. Validate proportionally

Check that frontmatter is valid YAML, headings are coherent, known targets exist, links and embeds are syntactically valid, and formatting improves scanning without overpowering content.

For new notes with vault links or substantial restructures, run:

```bash
python -X utf8 90_System/vault_integrity.py check --strict
```

Report unrelated pre-existing failures; do not change unrelated notes to make the check pass. Run `move`, `delete-check`, or `fix --safe` only when the requested operation requires it and follow the vault's `AGENTS.md` rules.

## Editing Rules

- Preserve factual qualifiers, citations, intentional terminology, valid links, and valid metadata.
- Consolidate duplication and improve transitions without reducing high-value detail to an outline.
- Convert dense prose into lists or tables only when information is genuinely discrete or aligned.
- Convert walls of bullets into prose when explanation, causality, or nuance matters.
- Return a complete note only when requested; otherwise return the requested fragment.

## References

- [NOTE-ARCHETYPES.md](references/NOTE-ARCHETYPES.md): choose optional structural modules.
- [PROPERTIES.md](references/PROPERTIES.md): properties, tags, aliases, and link-valued fields.
- [EMBEDS.md](references/EMBEDS.md): embeds and attachment rules.
- [CALLOUTS.md](references/CALLOUTS.md): callout semantics and folding.
- [SYNTAX-CAVEATS.md](references/SYNTAX-CAVEATS.md): edge cases and rendering limits.
