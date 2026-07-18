# Syntax Caveats

- Use a stable, readable block ID only when a block will be referenced. Restrict it to Latin letters, numbers, and hyphens.
- Escape `|` inside a wikilink or embed used in a Markdown table: `[[Note\|Display]]` and `![[image.webp\|320]]`.
- Do not expect Markdown to render inside HTML blocks.
- Mermaid node links styled as `internal-link` do not become Graph View links. Use real body wikilinks for vault relationships.
- Do not use Mermaid to restate a short obvious list. Prefer prose or a table when they communicate the relationship faster.
- Do not use Dataview syntax unless the vault already relies on the plugin or the user explicitly asks for it.
- Use standard Markdown links for external URLs. Use wikilinks for actual vault content.
