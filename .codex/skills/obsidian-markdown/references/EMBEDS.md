# Embeds

Embed known local content only when inline display improves understanding. Use a normal link when an embed would interrupt the reading flow. Do not invent filenames, attachment paths, headings, or block IDs.

```markdown
![[Note Name]]
![[Note Name#Heading]]
![[Note Name#^block-id]]
![[05_Attachments/topic/image.webp|640]]
![[document.pdf#page=3]]
![[My Canvas.canvas]]
```

## Rules

- Locate the exact attachment or note before creating an embed when the vault is accessible.
- Add an observation or caption when an image carries reasoning. Do not add decorative images.
- Use width controls when an image would dominate the page.
- Use a block ID only for content likely to be referenced again. Do not add speculative block IDs.
- Embed a Canvas only when its shapes add context; embedded Canvas views do not expose all card text as normal note body text.
- Escape the pipe in a wikilink or embed placed inside a Markdown table: `![[image.webp\|320]]`.
