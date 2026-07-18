# Callouts

Use callouts as semantic attention layers, not layout decoration. Prefer the vault's existing palette and labels.

| Need | Prefer | Guardrail |
| --- | --- | --- |
| Main takeaway | `summary` or `abstract` | Use only when it improves retrieval. |
| Practical heuristic | `tip` | Keep explanation in nearby prose. |
| Risk, limitation, or fragile assumption | `warning` | Use when omission could cause misuse. |
| Long example, prompt, excerpt, or raw detail | Folded `example` | Keep valuable secondary detail out of the main flow. |
| Unresolved issue | `question` | Resolve it first when the answer is cheap to verify. |
| Quotation | `quote` | Preserve source context. |

```markdown
> [!summary]
> Main conclusion or retrieval cue.

> [!example]- Detailed example
> Valuable detail that can stay collapsed.

> [!warning] Caveat
> A limitation that changes the decision.
```

Use `-` for collapsed-by-default and `+` for expanded-by-default. Do not nest callouts or use more than three in a typical note unless an established repeated semantic system requires it.
