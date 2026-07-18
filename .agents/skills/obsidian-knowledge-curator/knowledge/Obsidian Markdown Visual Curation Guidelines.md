# Obsidian Markdown Visual Curation Guidelines

Use this guide when the source contains images, comparisons, workflows, parameters, prompts, troubleshooting, decisions, or long reusable examples. It complements the sibling `obsidian-markdown` skill; it is not a second syntax contract.

## Core Principle

Use Markdown components as visual organization, not decoration. The note should feel intentionally curated, but not component-heavy.

Keep:

- flexible body structure shaped by the material
- readable rhythm between prose and structured blocks
- high-signal examples, prompts, parameters, caveats, decisions, and failure fixes
- faithful compression that removes noise and duplication without deleting unique reusable substance
- useful images as evidence or visual references
- source clarity when external material or web search is used

Avoid:

- fixed article templates
- summary-only rewrites of high-signal source material
- generic tables that merely rearrange prose
- callouts around every important sentence
- image dumps without captions or observations
- decorative images
- hidden comments for reader-relevant uncertainty
- non-native Markdown layouts unless the vault explicitly supports them

## Note Shape

The final note should be useful when reopened later, without requiring the raw source.

Required shape remains defined in `SKILL.md`: valid YAML frontmatter, one H1, material-shaped body sections, and `## Sources` only when external sources were actually used.

Prefer short openings that orient the reader quickly. Name sections after the material's real concepts, steps, decisions, problems, or reusable patterns. Do not add sections just because this guide mentions a component.

Compression should improve density, not erase substance. Keep the main flow readable, then move long but reusable examples, prompts, logs, parameter notes, and failure details into folded callouts, tables, code blocks, or appendix-like sections when needed.

## Component Decision Matrix

| Need | Prefer | Guardrail |
|---|---|---|
| Main takeaway or final judgment | `summary` callout | Use only when the conclusion is worth remembering. |
| Limitation, version trap, source uncertainty, risk | `warning` callout | Missing it should plausibly cause misuse. |
| Compact execution heuristic | `tip` callout | Keep it short; move explanations into prose. |
| Long prompt, raw example, source excerpt, failed attempt, alternate version | Folded `example` callout | Preserve useful detail without interrupting reading. |
| Comparison, parameters, diagnostics, trade-offs | Table | Use only when alignment helps. |
| Workflow, decision tree, dependency, timeline | Mermaid | Skip diagrams that restate obvious steps. |
| Screenshot or visual reference | Image + caption or observations | Explain what to notice. |
| Reusable section from another note | Embed | Avoid embedding long sections that overwhelm this note. |
| Side context | Footnote | Keep reader-critical context visible in the body. |
| Real vault relationship | Wikilink | Do not link every casual keyword. |

## Visual Rhythm

Use structured blocks to break long text only when they add meaning.

Good rhythm patterns:

- explanation -> image -> caption
- conclusion -> callout
- comparison -> table
- workflow -> Mermaid
- prompt -> code block -> parameter notes
- screenshot -> observation list
- reference gallery -> short synthesis
- warning -> folded raw details

Bad rhythm patterns:

- every paragraph becomes a callout
- tables with only one meaningful column
- diagrams for two obvious steps
- several images with no synthesis
- long raw excerpts in the main flow

## Callouts

Use callouts as attention layers. Prefer a small palette:

```markdown
> [!summary]
> Main takeaway, practical conclusion, or final judgment.

> [!warning] Caveat
> Important limitation, fragile assumption, version issue, or risk.

> [!tip]
> Compact execution heuristic.

> [!example]- Details
> Long prompt, raw example, source excerpt, failed attempt, or secondary material.

> [!question] Open question
> Unresolved issue, research gap, or future verification point.
```

Use folded callouts for content that is valuable but too heavy for the main reading path:

- raw prompts
- logs
- long examples
- source excerpts
- failed attempts
- alternate versions
- detailed parameter notes
- secondary screenshots

Do not leave a `question` callout for something that can be resolved quickly from official or primary sources during curation.

## Images

Images should be part of the reasoning, not decoration.

When a source visual supports the material, retain it in the finished note instead of replacing it with prose alone.

Good image uses:

- screenshots
- before / after comparison
- visual references
- UI locations
- lighting, pose, composition, style, or color analysis
- node graphs
- evidence material
- product, costume, outfit, or mood references

Use width control when an image would dominate the page:

```markdown
![[05_Attachments/note-slug/image-01.webp|600]]
```

Typical widths: UI detail `300-450`; normal screenshot `500-700`; visual reference `600-900`; large comparison image no width limit when needed.

Add captions that extract the lesson:

```markdown
![[05_Attachments/lighting-rim-example.webp|700]]

*The rim light is brighter than the key, so the subject reads as backlit rather than evenly lit.*
```

A caption should explain what to notice, not merely describe the visible content.

## Image Comparison

Use tables for compact before / after or variant comparison.

```markdown
| Before | After |
|---|---|
| ![[before.webp\|320]] | ![[after.webp\|320]] |
| Flat contrast, weak separation. | Stronger silhouette and warmer skin tone. |
```

Useful for retouching, color grading, AIGC edits, lighting changes, UI states, and prompt result comparison.

## Reference Gallery

Use small image tables as contact sheets.

```markdown
| Reference A | Reference B | Reference C |
|---|---|---|
| ![[ref-a.webp\|220]] | ![[ref-b.webp\|220]] | ![[ref-c.webp\|220]] |
| Soft backlight | Hard rim light | Low-key mood |
```

Good for moodboards, outfit references, cosplay references, lighting references, pose references, UI inspiration, and model output comparison.

## Observation Lists

For visual analysis, prefer image + short observations over long prose.

```markdown
![[composition-example.webp|650]]

Key observations:
- The subject is placed near the left third.
- Empty space creates direction and tension.
- The background line leads back toward the face.
```

This is especially useful for photography, AIGC, styling, 3D, UI, and design notes.

## Tables

Use tables as thinking tools, not as decoration.

High-value table shapes:

```markdown
| Option | Best for | Strength | Weakness | When to avoid |
|---|---|---|---|---|
| A | Fast draft | Easy setup | Less control | Final production |
```

```markdown
| Parameter | Effect | Useful range | Failure symptom |
|---|---|---:|---|
| Strength | Edit intensity | 0.35-0.65 | Identity drift |
```

```markdown
| Step | Input | Operation | Output | Check |
|---|---|---|---|---|
| 1 | Source image | Mask subject | Clean mask | Edge not broken |
```

```markdown
| Prompt part | Purpose | Replaceable field | Example |
|---|---|---|---|
| Subject | Defines main object | character / person | red-haired girl |
```

Avoid tables when a list reads better.

## Code Blocks And Prompts

Use code blocks for exact reusable content: commands, configs, prompts, templates, scripts, syntax, regex, YAML, and Mermaid.

Keep long prompts, logs, and exact examples in folded callouts when they are valuable but too heavy for the main flow.

When showing Markdown that itself contains code blocks, use a longer outer fence.

````markdown
```markdown
> [!warning]
> This is a reusable callout template.
```
````

## Mermaid

Use Mermaid when visual logic is clearer than prose:

- workflow
- troubleshooting path
- decision tree
- concept map
- dependency graph
- timeline
- source-to-output pipeline

Keep diagrams small. Split dense diagrams instead of forcing everything into one graph.

## Links And Embeds

Use clean wikilinks for real knowledge relationships:

- reusable concepts
- related workflows
- source notes
- visual references
- parent topics or subtopics
- specific headings
- repeated ideas worth connecting

Prefer heading links when the whole note is too broad. Use block links only for highly reusable small fragments.

Use embeds for reusable prompt templates, parameter presets, repeated warnings, shared definitions, checklist snippets, or visual reference blocks. Avoid embedding very long sections.

## Footnotes And Hidden Comments

Use footnotes for side context that would interrupt the sentence.

Use hidden comments only for short editor-only reminders:

```markdown
%% Check whether this example still works in the latest version. %%
```

Do not use hidden comments for caveats, uncertainty, or source context that the reader needs. Surface those in the note body, a callout, a footnote, or `## Sources`.

## Avoid Non-Native Syntax

Prefer native Obsidian Markdown: callouts, foldable callouts, wikilinks, embeds, image width control, tables, Mermaid, footnotes, comments, and code blocks.

Avoid by default:

- MkDocs tab syntax
- Docusaurus MDX components
- plugin-specific blocks
- CSS-dependent layouts
- heavy HTML

Only use non-native syntax when the vault explicitly supports it.

## Preflight

- Does every visual or structured block have a job?
- Does compression remove only noise, duplication, or superseded material?
- Are unique examples, parameters, prompts, procedures, caveats, decisions, and failure fixes still present or intentionally merged?
- Does the note avoid durable frontmatter, wikilinks, Markdown links, and Sources entries that point to transient inputs such as `00_Inbox/`?
- Is the Chinese prose natural, precise, and free of awkward merged phrasing?
- Are useful source images localized, sized, and explained when needed?
- Are long prompts, logs, and raw excerpts preserved without dominating the main flow?
- Are tables used for comparison or structure rather than decoration?
- Are callouts limited to meaningful attention layers?
- Are factual conflicts resolved or clearly surfaced?
- Are internal links real vault relationships rather than keyword decoration?
- Does the note still feel like a flexible, reusable Obsidian knowledge page?
