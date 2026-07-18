# Image Asset Handling

Use this reference when a curated note needs local images or image-like attachments.

## Goals

- Keep the vault and GitHub repository small.
- Preserve images that carry information.
- Avoid creating unnecessary duplicate final attachments.
- Keep Obsidian embeds stable and relative to the vault root.
- Support informational visuals when the source material contains them.
- Localize every useful image before the curation workflow deletes the raw source note.

## Default Policy

- Prefer optimized WebP for screenshots, web captures, photos, and other raster images.
- Use PNG only when lossless output is important, such as small UI diagrams, text-heavy images where WebP artifacts are visible, or transparent line art.
- Keep SVG as SVG when it is already clean and trusted.
- Skip animated GIF conversion unless the user explicitly accepts losing animation or provides a video/WebP animation workflow.
- Do not download or preserve decorative images just to make a note look richer.
- When source images, screenshots, diagrams, or UI captures explain the topic, treat them as first-class content. Localize a copy or optimized derivative and embed it near the relevant explanation.
- When no useful source image exists, do not create or fetch images just to satisfy an aesthetic expectation.
- If a material visual cannot be localized, retain the raw source note instead of silently dropping the visual and deleting its context.

## Optimization Script

Use `scripts/optimize_images.py` for raster images before embedding them.

Typical command from the vault root:

```powershell
python .codex\skills\obsidian-knowledge-curator\scripts\optimize_images.py `
  00_Inbox\raw-image.png `
  --output-dir 05_Attachments\note-slug `
  --format webp `
  --quality 82 `
  --max-edge 1800 `
  --name-prefix image
```

The script:

- requires Pillow
- writes optimized copies
- does not delete source files
- outputs a JSON manifest with created, skipped, and error entries
- skips outputs that are not at least 5% smaller by default

Use `--always-write` only when WebP consistency matters more than byte savings. Use `--overwrite` only when replacing a known generated output.

## Embedding

Embed optimized local files with Obsidian syntax:

```markdown
![[05_Attachments/note-slug/image-01.webp]]
```

Do not embed local files with absolute paths.

## Originals

- Keep original image assets unless the user separately asks to clean them up; deleting the raw source note does not delete its attachments. Copy useful originals or write optimized derivatives to `05_Attachments/<note-slug>/` before deleting the note.
- If the original has source value and the user asks to preserve it as a resource, place that copy under `03_Resources/<note-slug>/` and embed the optimized derivative from `05_Attachments/<note-slug>/`.
- If optimization is skipped because the result is larger or visually worse, embed the original only when its size is acceptable and it carries important information.

## Size Heuristics

- Prefer keeping individual embedded images under 500 KB when practical.
- Resize very large screenshots or photos to a maximum edge around 1600-1800 px unless fine detail is required.
- For text-heavy screenshots, inspect the optimized output before choosing it for the final note.
