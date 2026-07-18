# Properties

Use YAML frontmatter only when properties support an established vault workflow. Preserve nearby property names, value types, date formats, and quoting style.

```yaml
---
title: My Note Title
aliases:
  - Alternative Name
tags:
  - project/active
status: active
due: 2026-07-19
completed: false
---
```

## Rules

- Keep each property small, atomic, and machine-readable. Keep explanation in the body.
- Use one value type consistently for the same property across related notes.
- Use `tags`, `aliases`, and `cssclasses` only when they match existing convention or serve a clear purpose.
- Do not add `title` only to repeat a filename or H1 unless the vault already uses it.
- Do not create duplicate property names or nested schemas without an established vault convention.
- Markdown does not render inside property values.

## Property Types

| Type | Example |
| --- | --- |
| Text | `status: active` |
| Number | `rating: 4.5` |
| Checkbox | `completed: false` |
| Date | `due: 2026-07-19` |
| Date and time | `reviewed: 2026-07-19T14:30:00` |
| List | `tags: [project, active]` |

Obsidian has no separate Link property type. Store wikilinks in a quoted Text or List value:

```yaml
related: "[[Other Note]]"
related:
  - "[[Note A]]"
  - "[[Note B]]"
```

## Tags And Aliases

- A tag must contain at least one non-numeric character. `#1984` is invalid; `#book1984` is valid.
- Use tags for broad classification or workflow states, aliases for durable alternate names, and `[[Note|Display text]]` for one local display choice.
- Do not create tags, aliases, or nested tag trees merely to make frontmatter look complete.
