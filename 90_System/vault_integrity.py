from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import unicodedata
from dataclasses import asdict, dataclass, field
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Iterable


VAULT = Path(__file__).resolve().parents[1]
SYSTEM_DIR = VAULT / "90_System"
CONFIG_PATH = SYSTEM_DIR / "vault_integrity_config.json"

DEFAULT_CONFIG: dict[str, Any] = {
    "scan_roots": [
        "00_Inbox",
        "01_Projects",
        "02_Knowledge",
        "03_Resources",
        "04_Templates",
        "05_Attachments",
        "06_To_Classify",
    ],
    "exclude_dirs": [".git", ".obsidian", ".smart-env", ".codex", "90_System/__pycache__"],
    "metadata_json_files": ["90_System/drive_download_20260523_import_report.json"],
    "path_keys": [
        "source",
        "source_file",
        "sources",
        "target",
        "target_folder",
        "duplicate_of",
        "closest_existing",
        "attachment",
        "attachments",
    ],
    "allowed_virtual_links": [],
    "safe_fix_min_confidence": 0.98,
    "write_wikilink_targets_as_vault_paths": True,
    "strict_block_issue_types": [
        "missing_wikilink",
        "missing_embed",
        "missing_markdown_link",
        "absolute_frontmatter_path",
        "stale_metadata_path",
        "case_collision",
        "cross_platform_filename",
    ],
}

WIKI_RE = re.compile(r"(!?)\[\[([^\]\n]+)\]\]")
MD_LINK_RE = re.compile(r"(?<!!)\[[^\]\n]+\]\(([^)\n]+)\)")
FRONTMATTER_RE = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n?", re.S)
WINDOWS_ABS_RE = re.compile(r"^[A-Za-z]:[\\/]")
URL_RE = re.compile(r"^[a-z][a-z0-9+.-]*:", re.I)
INVALID_WINDOWS_CHARS = set('<>:"|?*')


@dataclass
class Issue:
    type: str
    file: str
    line: int | None = None
    target: str | None = None
    message: str = ""
    severity: str = "error"
    detail: dict[str, Any] = field(default_factory=dict)


@dataclass
class Suggestion:
    issue_type: str
    file: str
    line: int | None
    old_target: str
    new_target: str
    confidence: float
    reason: str
    safe: bool


@dataclass
class NoteMeta:
    path: Path
    rel: str
    stem: str
    title: str = ""
    aliases: list[str] = field(default_factory=list)


@dataclass
class ScanResult:
    issues: list[Issue]
    suggestions: list[Suggestion]
    counts: dict[str, int]


def load_config() -> dict[str, Any]:
    config = dict(DEFAULT_CONFIG)
    if CONFIG_PATH.exists():
        user_config = json.loads(CONFIG_PATH.read_text(encoding="utf-8-sig"))
        config.update(user_config)
    return config


def rel_path(path: Path) -> str:
    return path.resolve().relative_to(VAULT).as_posix()


def norm_rel(value: str) -> str:
    return value.replace("\\", "/").strip().strip("'\"")


def strip_md_suffix(value: str) -> str:
    return value[:-3] if value.lower().endswith(".md") else value


def normalize_key(value: str) -> str:
    value = unicodedata.normalize("NFKC", value)
    return value.replace("\\", "/").casefold().strip()


def normalize_title(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).casefold()
    value = re.sub(r"\.md$", "", value)
    value = re.sub(r"[_\-\s/\\]+", " ", value)
    value = re.sub(r"[^\w\u4e00-\u9fff. +]+", "", value)
    return value.strip()


def inside_vault(path: Path) -> bool:
    try:
        path.resolve().relative_to(VAULT)
        return True
    except ValueError:
        return False


def is_excluded(path: Path, config: dict[str, Any]) -> bool:
    rel = path.as_posix()
    parts = set(path.parts)
    for raw in config["exclude_dirs"]:
        item = norm_rel(raw)
        if "/" in item:
            if rel == item or rel.startswith(item + "/"):
                return True
        elif item in parts:
            return True
    return False


def is_in_scan_root(path: Path, config: dict[str, Any]) -> bool:
    if not path.parts:
        return False
    roots = set(config["scan_roots"])
    return path.parts[0] in roots and not is_excluded(path, config)


def iter_scan_files(config: dict[str, Any]) -> list[Path]:
    files: list[Path] = []
    for root in config["scan_roots"]:
        root_path = VAULT / root
        if not root_path.exists():
            continue
        for path in root_path.rglob("*"):
            if path.is_file() and not is_excluded(path.relative_to(VAULT), config):
                files.append(path)
    return sorted(files, key=lambda p: rel_path(p).casefold())


def iter_note_files(config: dict[str, Any]) -> list[Path]:
    return [path for path in iter_scan_files(config) if path.suffix.lower() == ".md"]


def strip_fenced_code(text: str) -> str:
    out: list[str] = []
    in_fence = False
    fence_marker = ""
    for line in text.splitlines():
        match = re.match(r"^\s*(```+|~~~+)", line)
        if match:
            marker = match.group(1)[0]
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif marker == fence_marker:
                in_fence = False
            out.append("")
            continue
        out.append("" if in_fence else line)
    return "\n".join(out)


def split_unescaped(value: str, separator: str) -> tuple[str, str]:
    escaped = False
    for index, char in enumerate(value):
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if char == separator:
            return value[:index], value[index + 1 :]
    return value, ""


def split_wikilink(raw: str) -> tuple[str, str, str]:
    before_display, display = split_unescaped(raw, "|")
    before_heading, heading = split_unescaped(before_display, "#")
    target = before_heading.strip()
    if heading:
        heading = "#" + heading
    if display:
        display = "|" + display
    return target, heading, display


def parse_frontmatter(text: str) -> str:
    match = FRONTMATTER_RE.match(text)
    return match.group(1) if match else ""


def unquote_yaml_scalar(value: str) -> str:
    value = value.strip()
    if value in {"", "[]", "null", "None", "none"}:
        return ""
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        value = value[1:-1]
    return value.replace('\\"', '"').replace("\\\\", "\\").strip()


def parse_frontmatter_scalar(frontmatter: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\s*(.*?)\s*$", frontmatter, re.M)
    return unquote_yaml_scalar(match.group(1)) if match else ""


def parse_frontmatter_list(frontmatter: str, key: str) -> list[str]:
    lines = frontmatter.splitlines()
    values: list[str] = []
    capture = False
    for line in lines:
        if re.match(rf"^{re.escape(key)}:\s*$", line):
            capture = True
            continue
        if capture:
            if re.match(r"^[A-Za-z_][\w-]*:", line):
                break
            match = re.match(r"\s*-\s*(.*?)\s*$", line)
            if match:
                value = unquote_yaml_scalar(match.group(1))
                if value:
                    values.append(value)
    return values


def parse_note_meta(path: Path) -> NoteMeta:
    text = path.read_text(encoding="utf-8", errors="ignore")
    frontmatter = parse_frontmatter(text)
    title = parse_frontmatter_scalar(frontmatter, "title")
    aliases = parse_frontmatter_list(frontmatter, "aliases")
    aliases = [alias for alias in aliases if alias.casefold() not in {"none", "null"}]
    return NoteMeta(path=path, rel=rel_path(path), stem=path.stem, title=title, aliases=aliases)


class VaultIndex:
    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config
        self.files = iter_scan_files(config)
        self.notes = [parse_note_meta(path) for path in iter_note_files(config)]
        self.note_by_rel: dict[str, Path] = {}
        self.note_by_rel_noext: dict[str, Path] = {}
        self.note_by_stem: dict[str, list[Path]] = {}
        self.note_by_alias: dict[str, list[Path]] = {}
        self.file_by_rel: dict[str, Path] = {}
        self.file_by_rel_noext: dict[str, Path] = {}
        self.file_by_name: dict[str, list[Path]] = {}
        self._build()

    def _build(self) -> None:
        for path in self.files:
            rel = rel_path(path)
            self.file_by_rel[normalize_key(rel)] = path
            self.file_by_rel_noext[normalize_key(strip_md_suffix(rel))] = path
            self.file_by_name.setdefault(normalize_key(path.name), []).append(path)
            self.file_by_name.setdefault(normalize_key(path.stem), []).append(path)
        for meta in self.notes:
            rel = meta.rel
            self.note_by_rel[normalize_key(rel)] = meta.path
            self.note_by_rel_noext[normalize_key(strip_md_suffix(rel))] = meta.path
            self.note_by_stem.setdefault(normalize_key(meta.stem), []).append(meta.path)
            if meta.title:
                self.note_by_alias.setdefault(normalize_key(meta.title), []).append(meta.path)
            for alias in meta.aliases:
                self.note_by_alias.setdefault(normalize_key(alias), []).append(meta.path)

    def resolve_wikilink(self, target: str, source: Path, embed: bool = False) -> tuple[str, list[Path]]:
        target = norm_rel(target)
        if not target:
            return "ok", [source]
        candidates: list[Path] = []
        lower = normalize_key(target)
        if "/" in target or target.lower().endswith(".md"):
            candidates.extend(self._resolve_path_like(target, source, embed))
        if not candidates:
            if lower in self.note_by_stem:
                candidates.extend(self.note_by_stem[lower])
            if lower in self.note_by_alias:
                candidates.extend(self.note_by_alias[lower])
        if embed and not candidates:
            if lower in self.file_by_name:
                candidates.extend(self.file_by_name[lower])
            if lower in self.file_by_rel:
                candidates.append(self.file_by_rel[lower])
            if lower in self.file_by_rel_noext:
                candidates.append(self.file_by_rel_noext[lower])
        unique = sorted(set(candidates), key=lambda p: rel_path(p).casefold())
        if len(unique) == 1:
            return "ok", unique
        if len(unique) > 1:
            return "ambiguous", unique
        return "missing", []

    def _resolve_path_like(self, target: str, source: Path, embed: bool) -> list[Path]:
        candidates: list[Path] = []
        target_noext = strip_md_suffix(target)
        for key in (target, target_noext):
            norm = normalize_key(key)
            if norm in self.note_by_rel:
                candidates.append(self.note_by_rel[norm])
            if norm in self.note_by_rel_noext:
                candidates.append(self.note_by_rel_noext[norm])
            if embed and norm in self.file_by_rel:
                candidates.append(self.file_by_rel[norm])
            if embed and norm in self.file_by_rel_noext:
                candidates.append(self.file_by_rel_noext[norm])
        source_relative = (source.parent / target).resolve()
        if inside_vault(source_relative) and source_relative.exists():
            candidates.append(source_relative)
        if target.lower().endswith(".md"):
            source_relative_noext = source_relative.with_suffix("")
            if inside_vault(source_relative_noext.with_suffix(".md")) and source_relative_noext.with_suffix(".md").exists():
                candidates.append(source_relative_noext.with_suffix(".md"))
        return candidates


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def is_allowed_virtual(target: str, config: dict[str, Any]) -> bool:
    normalized = normalize_key(target)
    allowed = {normalize_key(item) for item in config.get("allowed_virtual_links", [])}
    if normalized in allowed:
        return True
    for pattern in config.get("allowed_virtual_link_patterns", []):
        if re.search(pattern, target):
            return True
    return False


def yaml_path_values(frontmatter: str, config: dict[str, Any]) -> Iterable[tuple[int, str, str]]:
    current_key = ""
    path_keys = set(config["path_keys"])
    for idx, line in enumerate(frontmatter.splitlines(), start=2):
        scalar = re.match(r"^([A-Za-z_][\w-]*):\s*(.*?)\s*$", line)
        if scalar:
            current_key = scalar.group(1)
            value = unquote_yaml_scalar(scalar.group(2))
            if value:
                yield idx, current_key, value
            continue
        item = re.match(r"^\s*-\s*(.*?)\s*$", line)
        if item and current_key in path_keys:
            value = unquote_yaml_scalar(item.group(1))
            if value:
                yield idx, current_key, value


def looks_pathish(value: str, key: str, config: dict[str, Any]) -> bool:
    if key in set(config["path_keys"]):
        return True
    return bool(WINDOWS_ABS_RE.match(value) or "/" in value or "\\" in value)


def is_external_or_url(value: str) -> bool:
    if URL_RE.match(value) and not WINDOWS_ABS_RE.match(value):
        return True
    if WINDOWS_ABS_RE.match(value):
        return False
    return False


def vault_relative_exists(value: str) -> bool:
    normalized = norm_rel(value)
    if not normalized or WINDOWS_ABS_RE.match(normalized) or is_external_or_url(normalized):
        return True
    if normalized.startswith("#"):
        return True
    if "/" not in normalized and "\\" not in value:
        return True
    path = (VAULT / normalized).resolve()
    return inside_vault(path) and path.exists()


def check_wikilinks(index: VaultIndex, issues: list[Issue], counts: dict[str, int]) -> None:
    for path in index.notes:
        text = path.path.read_text(encoding="utf-8", errors="ignore")
        stripped = strip_fenced_code(text)
        for match in WIKI_RE.finditer(stripped):
            embed = bool(match.group(1))
            raw = match.group(2)
            target, _heading, _display = split_wikilink(raw)
            status, matches = index.resolve_wikilink(target, path.path, embed)
            counts["wikilinks_seen"] += 1
            if status == "ok":
                counts["wikilinks_ok"] += 1
                continue
            if status == "ambiguous":
                issues.append(
                    Issue(
                        type="ambiguous_wikilink",
                        file=path.rel,
                        line=line_number(stripped, match.start()),
                        target=target,
                        message="Wikilink matches multiple files.",
                        severity="warning",
                        detail={"candidates": [rel_path(p) for p in matches]},
                    )
                )
                continue
            issue_type = "missing_embed" if embed else "missing_wikilink"
            if is_allowed_virtual(target, index.config):
                issue_type = "virtual_wikilink"
                severity = "info"
            else:
                severity = "error"
            issues.append(
                Issue(
                    type=issue_type,
                    file=path.rel,
                    line=line_number(stripped, match.start()),
                    target=target,
                    message="Wikilink target is not present in the scanned vault roots.",
                    severity=severity,
                    detail={"embed": embed, "raw": raw},
                )
            )


def check_markdown_links(index: VaultIndex, issues: list[Issue], counts: dict[str, int]) -> None:
    for meta in index.notes:
        text = meta.path.read_text(encoding="utf-8", errors="ignore")
        stripped = strip_fenced_code(text)
        for match in MD_LINK_RE.finditer(stripped):
            href = match.group(1).strip().strip("<>")
            if not href or href.startswith("#") or is_external_or_url(href) or href.startswith("mailto:"):
                continue
            target = href.split("#", 1)[0]
            if not target:
                continue
            candidate = (meta.path.parent / target).resolve()
            if inside_vault(candidate) and not candidate.exists():
                issues.append(
                    Issue(
                        type="missing_markdown_link",
                        file=meta.rel,
                        line=line_number(stripped, match.start()),
                        target=href,
                        message="Local Markdown link target does not exist.",
                    )
                )
            counts["markdown_links_seen"] += 1


def check_frontmatter_paths(index: VaultIndex, issues: list[Issue]) -> None:
    for meta in index.notes:
        text = meta.path.read_text(encoding="utf-8", errors="ignore")
        frontmatter = parse_frontmatter(text)
        if not frontmatter:
            continue
        for line, key, value in yaml_path_values(frontmatter, index.config):
            if not looks_pathish(value, key, index.config):
                continue
            if WINDOWS_ABS_RE.match(value):
                issues.append(
                    Issue(
                        type="absolute_frontmatter_path",
                        file=meta.rel,
                        line=line,
                        target=value,
                        message="Frontmatter stores a machine-specific absolute path.",
                        detail={"key": key},
                    )
                )
            elif not vault_relative_exists(value):
                issues.append(
                    Issue(
                        type="missing_frontmatter_path",
                        file=meta.rel,
                        line=line,
                        target=value,
                        message="Frontmatter path-like value does not exist in the vault.",
                        severity="warning",
                        detail={"key": key},
                    )
                )


def check_metadata_json(config: dict[str, Any], issues: list[Issue]) -> None:
    path_keys = set(config["path_keys"])
    for raw_path in config.get("metadata_json_files", []):
        path = VAULT / raw_path
        if not path.exists():
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8-sig"))
        except json.JSONDecodeError as exc:
            issues.append(
                Issue(
                    type="invalid_metadata_json",
                    file=norm_rel(raw_path),
                    line=exc.lineno,
                    message=str(exc),
                )
            )
            continue
        for json_path, key, value in iter_json_path_values(data):
            if key not in path_keys or not isinstance(value, str) or not value:
                continue
            normalized = norm_rel(value)
            if WINDOWS_ABS_RE.match(normalized) or is_external_or_url(normalized):
                continue
            if "/" not in normalized and "\\" not in value:
                continue
            if not (VAULT / normalized).exists():
                issues.append(
                    Issue(
                        type="stale_metadata_path",
                        file=norm_rel(raw_path),
                        target=value,
                        message="Metadata JSON points to a missing vault path.",
                        detail={"json_path": json_path, "key": key},
                    )
                )


def iter_json_path_values(data: Any, prefix: str = "$") -> Iterable[tuple[str, str, Any]]:
    if isinstance(data, dict):
        for key, value in data.items():
            child = f"{prefix}.{key}"
            if isinstance(value, (dict, list)):
                yield from iter_json_path_values(value, child)
            else:
                yield child, key, value
    elif isinstance(data, list):
        for index, value in enumerate(data):
            yield from iter_json_path_values(value, f"{prefix}[{index}]")


def check_cross_platform(index: VaultIndex, issues: list[Issue]) -> None:
    seen_case: dict[str, str] = {}
    seen_nfc: dict[str, str] = {}
    for path in index.files:
        rel = rel_path(path)
        case_key = rel.casefold()
        if case_key in seen_case and seen_case[case_key] != rel:
            issues.append(
                Issue(
                    type="case_collision",
                    file=rel,
                    target=seen_case[case_key],
                    message="Two paths differ only by case and may collide across systems.",
                )
            )
        else:
            seen_case[case_key] = rel
        nfc_key = unicodedata.normalize("NFC", rel)
        if nfc_key in seen_nfc and seen_nfc[nfc_key] != rel:
            issues.append(
                Issue(
                    type="unicode_normalization_collision",
                    file=rel,
                    target=seen_nfc[nfc_key],
                    message="Two paths differ only by Unicode normalization.",
                    severity="warning",
                )
            )
        else:
            seen_nfc[nfc_key] = rel
        for part in Path(rel).parts:
            if part in {".", ".."}:
                continue
            bad = sorted(ch for ch in part if ch in INVALID_WINDOWS_CHARS)
            if bad or part.endswith(" ") or part.endswith("."):
                issues.append(
                    Issue(
                        type="cross_platform_filename",
                        file=rel,
                        target=part,
                        message="Path component is risky across Windows/macOS/Git.",
                        detail={"bad_chars": bad, "trailing_space_or_dot": part.endswith((" ", "."))},
                    )
                )


def build_suggestions(index: VaultIndex, issues: list[Issue]) -> list[Suggestion]:
    suggestions: list[Suggestion] = []
    rename_map = git_rename_map()
    for issue in issues:
        if issue.type not in {"missing_wikilink", "missing_embed", "stale_metadata_path", "missing_frontmatter_path"}:
            continue
        target = issue.target or ""
        if not target:
            continue
        candidate_items = candidate_paths(index, target, rename_map)
        for candidate, confidence, reason, safe in candidate_items:
            if issue.type in {"stale_metadata_path", "missing_frontmatter_path"}:
                new_target = rel_path(candidate)
            else:
                new_target = format_link_target(candidate, index.config)
            suggestions.append(
                Suggestion(
                    issue_type=issue.type,
                    file=issue.file,
                    line=issue.line,
                    old_target=target,
                    new_target=new_target,
                    confidence=confidence,
                    reason=reason,
                    safe=safe and confidence >= float(index.config.get("safe_fix_min_confidence", 0.98)),
                )
            )
    return suggestions


def git_rename_map() -> dict[str, str]:
    rename_map: dict[str, str] = {}
    for args in (["diff", "--name-status", "-M"], ["diff", "--cached", "--name-status", "-M"]):
        try:
            result = subprocess.run(
                ["git", *args],
                cwd=VAULT,
                text=True,
                encoding="utf-8",
                errors="ignore",
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                check=False,
            )
        except OSError:
            continue
        for line in result.stdout.splitlines():
            parts = line.split("\t")
            if len(parts) == 3 and parts[0].startswith("R"):
                old, new = norm_rel(parts[1]), norm_rel(parts[2])
                rename_map[normalize_key(old)] = new
                rename_map[normalize_key(strip_md_suffix(old))] = strip_md_suffix(new)
                rename_map[normalize_key(Path(old).stem)] = strip_md_suffix(new)
    return rename_map


def candidate_paths(index: VaultIndex, target: str, rename_map: dict[str, str]) -> list[tuple[Path, float, str, bool]]:
    target_norm = norm_rel(target)
    target_noext = strip_md_suffix(target_norm)
    candidates: list[tuple[Path, float, str, bool]] = []
    for key in (target_norm, target_noext, Path(target_norm).stem):
        mapped = rename_map.get(normalize_key(key))
        if mapped:
            path = VAULT / mapped
            if path.exists():
                candidates.append((path, 1.0, "git_rename", True))
    exact_stem = normalize_key(Path(target_noext).stem)
    if exact_stem in index.note_by_stem and len(index.note_by_stem[exact_stem]) == 1:
        candidates.append((index.note_by_stem[exact_stem][0], 1.0, "unique_stem", True))
    if exact_stem in index.note_by_alias and len(index.note_by_alias[exact_stem]) == 1:
        candidates.append((index.note_by_alias[exact_stem][0], 1.0, "unique_alias", True))
    scored: list[tuple[float, Path]] = []
    normalized_target = normalize_title(Path(target_noext).stem)
    if normalized_target:
        for meta in index.notes:
            options = [meta.stem, meta.title, *meta.aliases]
            score = max((SequenceMatcher(None, normalized_target, normalize_title(item)).ratio() for item in options if item), default=0.0)
            if score >= 0.72:
                scored.append((score, meta.path))
    for score, path in sorted(scored, key=lambda item: item[0], reverse=True)[:5]:
        candidates.append((path, round(score, 3), "fuzzy_title", False))
    deduped: list[tuple[Path, float, str, bool]] = []
    seen: set[str] = set()
    for path, confidence, reason, safe in sorted(candidates, key=lambda item: (item[3], item[1]), reverse=True):
        key = rel_path(path)
        if key in seen:
            continue
        seen.add(key)
        deduped.append((path, confidence, reason, safe))
    return deduped


def format_link_target(path: Path, config: dict[str, Any]) -> str:
    rel = rel_path(path)
    if path.suffix.lower() == ".md":
        rel = strip_md_suffix(rel)
    if config.get("write_wikilink_targets_as_vault_paths", True):
        return rel
    return Path(rel).stem


def scan(config: dict[str, Any]) -> ScanResult:
    index = VaultIndex(config)
    issues: list[Issue] = []
    counts: dict[str, int] = {
        "files_seen": len(index.files),
        "notes_seen": len(index.notes),
        "wikilinks_seen": 0,
        "wikilinks_ok": 0,
        "markdown_links_seen": 0,
    }
    check_wikilinks(index, issues, counts)
    check_markdown_links(index, issues, counts)
    check_frontmatter_paths(index, issues)
    check_metadata_json(config, issues)
    check_cross_platform(index, issues)
    suggestions = build_suggestions(index, issues)
    counts["issues"] = len(issues)
    counts["blocking_issues"] = len([issue for issue in issues if is_blocking(issue, config)])
    counts["safe_suggestions"] = len([suggestion for suggestion in suggestions if suggestion.safe])
    return ScanResult(issues=issues, suggestions=suggestions, counts=counts)


def is_blocking(issue: Issue, config: dict[str, Any]) -> bool:
    return issue.type in set(config.get("strict_block_issue_types", [])) and issue.severity == "error"


def issues_by_type(issues: list[Issue]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for issue in issues:
        counts[issue.type] = counts.get(issue.type, 0) + 1
    return dict(sorted(counts.items()))


def print_check(result: ScanResult, config: dict[str, Any], json_mode: bool = False) -> None:
    if json_mode:
        print(
            json.dumps(
                {
                    "summary": result.counts,
                    "issue_counts": issues_by_type(result.issues),
                    "issues": [asdict(issue) for issue in result.issues],
                    "suggestions": [asdict(suggestion) for suggestion in result.suggestions],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return
    print("Vault Integrity Check")
    print(json.dumps(result.counts, ensure_ascii=False, indent=2))
    print("Issue counts:")
    print(json.dumps(issues_by_type(result.issues), ensure_ascii=False, indent=2))
    blocking = [issue for issue in result.issues if is_blocking(issue, config)]
    sample = blocking[:20] if blocking else result.issues[:20]
    if sample:
        print("Sample issues:")
        for issue in sample:
            location = f"{issue.file}:{issue.line}" if issue.line else issue.file
            target = f" -> {issue.target}" if issue.target else ""
            print(f"- [{issue.type}] {location}{target} :: {issue.message}")
    if result.counts.get("safe_suggestions"):
        print(f"Safe suggestions available: {result.counts['safe_suggestions']}")


def print_suggestions(result: ScanResult, json_mode: bool = False) -> None:
    if json_mode:
        print(json.dumps([asdict(suggestion) for suggestion in result.suggestions], ensure_ascii=False, indent=2))
        return
    if not result.suggestions:
        print("No suggestions.")
        return
    for suggestion in result.suggestions:
        flag = "safe" if suggestion.safe else "review"
        line = f":{suggestion.line}" if suggestion.line else ""
        print(
            f"[{flag}] {suggestion.file}{line}: "
            f"{suggestion.old_target} -> {suggestion.new_target} "
            f"({suggestion.confidence:.2f}, {suggestion.reason})"
        )


def apply_safe_fixes(config: dict[str, Any]) -> dict[str, Any]:
    result = scan(config)
    safe = [suggestion for suggestion in result.suggestions if suggestion.safe]
    link_safe = [suggestion for suggestion in safe if suggestion.issue_type in {"missing_wikilink", "missing_embed"}]
    metadata_safe = dedupe_metadata_suggestions([suggestion for suggestion in safe if suggestion.issue_type == "stale_metadata_path"])
    replacements_by_file: dict[str, dict[str, str]] = {}
    for suggestion in link_safe:
        replacements_by_file.setdefault(suggestion.file, {})[suggestion.old_target] = suggestion.new_target
    changed_files: list[str] = []
    for rel, replacements in replacements_by_file.items():
        path = VAULT / rel
        original = path.read_text(encoding="utf-8")

        def repl(match: re.Match[str]) -> str:
            prefix = match.group(1)
            raw = match.group(2)
            target, heading, display = split_wikilink(raw)
            if target not in replacements:
                return match.group(0)
            return f"{prefix}[[{replacements[target]}{heading}{display}]]"

        updated = WIKI_RE.sub(repl, original)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed_files.append(rel)
    for suggestion in metadata_safe:
        changed_files.extend(update_metadata_paths(suggestion.old_target, suggestion.new_target, config))
    return {
        "safe_suggestions": len(link_safe) + len(metadata_safe),
        "applied_link_suggestions": len(link_safe),
        "applied_metadata_suggestions": len(metadata_safe),
        "review_only_safe_suggestions": len(safe) - len(link_safe) - len(metadata_safe),
        "changed_files": changed_files,
        "remaining_blocking_issues": scan(config).counts["blocking_issues"],
    }


def dedupe_metadata_suggestions(suggestions: list[Suggestion]) -> list[Suggestion]:
    deduped: list[Suggestion] = []
    seen: set[tuple[str, str, str]] = set()
    for suggestion in suggestions:
        key = (suggestion.file, norm_rel(suggestion.old_target), norm_rel(suggestion.new_target))
        if key in seen:
            continue
        seen.add(key)
        deduped.append(suggestion)
    return deduped


def inbound_references(target: str, config: dict[str, Any]) -> list[dict[str, Any]]:
    index = VaultIndex(config)
    target_path = (VAULT / norm_rel(target)).resolve()
    if not inside_vault(target_path):
        raise SystemExit("target must stay inside the vault")
    target_rel = rel_path(target_path)
    refs: list[dict[str, Any]] = []
    for meta in index.notes:
        if meta.path.resolve() == target_path:
            continue
        text = meta.path.read_text(encoding="utf-8", errors="ignore")
        stripped = strip_fenced_code(text)
        for match in WIKI_RE.finditer(stripped):
            raw = match.group(2)
            link_target, _heading, _display = split_wikilink(raw)
            status, matches = index.resolve_wikilink(link_target, meta.path, bool(match.group(1)))
            if status == "ok" and matches and rel_path(matches[0]) == target_rel:
                refs.append(
                    {
                        "file": meta.rel,
                        "line": line_number(stripped, match.start()),
                        "target": link_target,
                        "raw": raw,
                    }
                )
    return refs


def update_links_for_move(old_rel: str, new_rel: str, config: dict[str, Any]) -> list[str]:
    before = VaultIndex(config)
    old_path = VAULT / old_rel
    old_aliases = {normalize_key(strip_md_suffix(old_rel)), normalize_key(Path(old_rel).stem)}
    if old_path.exists() and old_path.suffix.lower() == ".md":
        meta = parse_note_meta(old_path)
        old_aliases.update(normalize_key(item) for item in [meta.title, *meta.aliases] if item)
    new_target = strip_md_suffix(norm_rel(new_rel))
    changed: list[str] = []
    for meta in before.notes:
        if norm_rel(meta.rel) == norm_rel(old_rel):
            continue
        text = meta.path.read_text(encoding="utf-8", errors="ignore")

        def repl(match: re.Match[str]) -> str:
            prefix = match.group(1)
            raw = match.group(2)
            target, heading, display = split_wikilink(raw)
            status, paths = before.resolve_wikilink(target, meta.path, bool(prefix))
            target_is_old = status == "ok" and paths and norm_rel(rel_path(paths[0])) == norm_rel(old_rel)
            if not target_is_old and normalize_key(target) not in old_aliases:
                return match.group(0)
            return f"{prefix}[[{new_target}{heading}{display}]]"

        updated = WIKI_RE.sub(repl, text)
        if updated != text:
            meta.path.write_text(updated, encoding="utf-8")
            changed.append(meta.rel)
    changed.extend(update_metadata_paths(old_rel, new_rel, config))
    return sorted(set(changed))


def update_metadata_paths(old_rel: str, new_rel: str, config: dict[str, Any]) -> list[str]:
    changed: list[str] = []
    old_forms = {norm_rel(old_rel), norm_rel(old_rel).replace("/", "\\")}
    new_form = norm_rel(new_rel)
    for raw_path in config.get("metadata_json_files", []):
        path = VAULT / raw_path
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        data = json.loads(text)
        updated = replace_json_paths(data, old_forms, new_form)
        if updated:
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            changed.append(norm_rel(raw_path))
    return changed


def replace_json_paths(data: Any, old_forms: set[str], new_form: str) -> bool:
    changed = False
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, str) and norm_rel(value) in {norm_rel(item) for item in old_forms}:
                data[key] = new_form
                changed = True
            elif isinstance(value, (dict, list)):
                changed = replace_json_paths(value, old_forms, new_form) or changed
    elif isinstance(data, list):
        for value in data:
            if isinstance(value, (dict, list)):
                changed = replace_json_paths(value, old_forms, new_form) or changed
    return changed


def move_path(source: str, destination: str, config: dict[str, Any], force: bool = False, dry_run: bool = False) -> dict[str, Any]:
    src = (VAULT / norm_rel(source)).resolve()
    dst = (VAULT / norm_rel(destination)).resolve()
    if not inside_vault(src) or not inside_vault(dst):
        raise SystemExit("source and destination must stay inside the vault")
    if not src.exists():
        raise SystemExit(f"source does not exist: {source}")
    if dst.exists() and not force:
        raise SystemExit(f"destination already exists: {destination}")
    old_rel = rel_path(src)
    new_rel = dst.relative_to(VAULT).as_posix()
    changed = update_links_for_move(old_rel, new_rel, config) if not dry_run else []
    if not dry_run:
        dst.parent.mkdir(parents=True, exist_ok=True)
        os.replace(src, dst)
    return {"moved": {"from": old_rel, "to": new_rel}, "updated_files": changed, "dry_run": dry_run}


def command_check(args: argparse.Namespace) -> int:
    config = load_config()
    result = scan(config)
    print_check(result, config, json_mode=args.json)
    if args.strict and any(is_blocking(issue, config) for issue in result.issues):
        return 1
    return 0


def command_suggest(args: argparse.Namespace) -> int:
    config = load_config()
    result = scan(config)
    print_suggestions(result, json_mode=args.json)
    return 0


def command_fix(args: argparse.Namespace) -> int:
    config = load_config()
    if not args.safe:
        raise SystemExit("Only --safe fixes are supported in v1.")
    report = apply_safe_fixes(config)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


def command_move(args: argparse.Namespace) -> int:
    config = load_config()
    report = move_path(args.source, args.destination, config, force=args.force, dry_run=args.dry_run)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


def command_delete_check(args: argparse.Namespace) -> int:
    config = load_config()
    refs = inbound_references(args.target, config)
    report = {
        "target": norm_rel(args.target),
        "inbound_references": refs,
        "would_break": len(refs),
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if args.strict and refs else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Check and repair Obsidian vault references.")
    sub = parser.add_subparsers(dest="command", required=True)

    check = sub.add_parser("check", help="scan vault references and metadata")
    check.add_argument("--json", action="store_true", help="print machine-readable report")
    check.add_argument("--strict", action="store_true", help="exit non-zero when blocking issues exist")
    check.add_argument("--staged", action="store_true", help="accepted for Git hooks; v1 still scans configured roots")
    check.set_defaults(func=command_check)

    suggest = sub.add_parser("suggest", help="show candidate repairs without writing files")
    suggest.add_argument("--json", action="store_true", help="print machine-readable suggestions")
    suggest.set_defaults(func=command_suggest)

    fix = sub.add_parser("fix", help="apply repairs")
    fix.add_argument("--safe", action="store_true", help="apply only high-confidence deterministic repairs")
    fix.set_defaults(func=command_fix)

    move = sub.add_parser("move", help="move a vault file and update inbound references")
    move.add_argument("source")
    move.add_argument("destination")
    move.add_argument("--force", action="store_true", help="replace destination if it exists")
    move.add_argument("--dry-run", action="store_true", help="validate arguments without moving")
    move.set_defaults(func=command_move)

    delete_check = sub.add_parser("delete-check", help="show inbound wikilinks that would break if a file is deleted")
    delete_check.add_argument("target")
    delete_check.add_argument("--strict", action="store_true", help="exit non-zero when inbound references exist")
    delete_check.set_defaults(func=command_delete_check)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
