from __future__ import annotations

import json
import re
from pathlib import Path


VAULT = Path(__file__).resolve().parents[1]
REPORT = VAULT / "90_System" / "drive_download_20260523_import_report.json"


def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---"):
        return "", text
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n?", text, re.S)
    if not match:
        return "", text
    return match.group(1), text[match.end():]


def parse_scalar(frontmatter: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\s*(.*)$", frontmatter, re.M)
    if not match:
        return ""
    value = match.group(1).strip()
    if len(value) >= 2 and value[0] == value[-1] == '"':
        value = value[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    return value


def parse_list(frontmatter: str, key: str) -> list[str]:
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
            item = re.match(r"\s*-\s*(.*)$", line)
            if item:
                value = item.group(1).strip()
                if len(value) >= 2 and value[0] == value[-1] == '"':
                    value = value[1:-1].replace('\\"', '"').replace("\\\\", "\\")
                values.append(value)
    return values


def yaml_quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def normalize_aliases(title: str, aliases: list[str]) -> list[str]:
    seen = set()
    out = []
    for value in aliases:
        value = value.strip()
        if not value or value == title or value in seen:
            continue
        seen.add(value)
        out.append(value)
    return out[:3]


def build_frontmatter(old_fm: str, item: dict[str, object]) -> str:
    title = str(item["title"])
    aliases = normalize_aliases(title, parse_list(old_fm, "aliases"))
    tags = parse_list(old_fm, "tags") or list(item.get("tags", []))
    tags = sorted(dict.fromkeys(tags + ["status/imported"]))
    source_file = parse_scalar(old_fm, "source_file")
    imported = parse_scalar(old_fm, "imported")
    target_folder = parse_scalar(old_fm, "target_folder")
    original_format = parse_scalar(old_fm, "original_format") or "docx"
    safety = "true" if item.get("sensitive_stub") else "false"

    lines = [
        "---",
        f"title: {yaml_quote(title)}",
        "aliases:",
    ]
    if aliases:
        lines.extend(f"  - {yaml_quote(alias)}" for alias in aliases)
    else:
        lines.append("  - none")
    lines.append("tags:")
    lines.extend(f"  - {tag}" for tag in tags)
    if source_file:
        lines.append(f"source_file: {yaml_quote(source_file)}")
    if imported:
        lines.append(f"imported: {imported}")
    lines.append(f"original_format: {original_format}")
    if target_folder:
        lines.append(f"target_folder: {yaml_quote(target_folder)}")
    lines.append("status: imported")
    lines.append(f"safety_review_required: {safety}")
    lines.append("---")
    return "\n".join(lines)


def strip_import_header(body: str, title: str) -> str:
    body = body.replace("\r\n", "\n")
    body = re.sub(rf"^\s*#\s+{re.escape(title)}\s*\n+", "", body)
    previous_reformat = re.search(r"(?:^|\n)## 正文\s*\n", body)
    if previous_reformat:
        body = body[previous_reformat.end():]
    body = re.sub(
        r"^> \[!info\] Import Note\n(?:>.*\n)+\n*",
        "",
        body,
        flags=re.M,
    )
    body = re.sub(
        r"^> \[!warning\] Embedded Media\n(?:>.*\n)+\n*",
        "",
        body,
        flags=re.M,
    )
    return body.strip()


def heading_level(line: str) -> int | None:
    text = line.strip()
    if not text:
        return None
    existing = re.match(r"^(#{2,6})\s+(.+)$", text)
    if existing:
        title = existing.group(2).strip()
        if re.match(r"^\d+(?:\.\d+){2,}", title):
            return 4
        if re.match(r"^\d+\.\d+", title):
            return 3
        return 2
    if re.match(r"^第[一二三四五六七八九十百]+[章节篇部]\s*", text):
        return 2
    if re.match(r"^[一二三四五六七八九十]+、", text):
        return 2
    if re.match(r"^\d+(?:\.\d+){2,}\s+", text):
        return 4
    if re.match(r"^\d+\.\d+\s+", text):
        return 3
    if re.match(r"^\d+[.．、]\s*", text):
        return 2
    return None


def clean_heading_text(line: str) -> str:
    text = re.sub(r"^#{1,6}\s+", "", line.strip())
    return text.strip()


def normalize_body(body: str) -> tuple[str, list[str]]:
    lines = body.splitlines()
    out: list[str] = []
    headings: list[str] = []
    in_table = False
    for raw in lines:
        line = raw.rstrip()
        if not line.strip():
            if out and out[-1] != "":
                out.append("")
            in_table = False
            continue
        if line.lstrip().startswith("|"):
            out.append(line)
            in_table = True
            continue
        level = None if in_table else heading_level(line)
        if level:
            heading = clean_heading_text(line)
            out.extend(["", f"{'#' * level} {heading}", ""])
            headings.append(heading)
            in_table = False
            continue
        line = re.sub(r"^([A-Za-z\u4e00-\u9fff][^:：]{1,18})[:：]\s+", r"**\1:** ", line)
        out.append(line)
        in_table = False
    text = "\n".join(out)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text, headings


def anchor_for(heading: str) -> str:
    return heading.replace("[", "").replace("]", "").strip()


def related_links(title: str, tags: list[str]) -> list[str]:
    probe = f"{title} {' '.join(tags)}".lower()
    links: list[str] = []
    if "midjourney" in probe:
        links += ["[[midjourney-prompt-guide]]", "[[midjourney-prompt-best-practices]]", "[[midjourney-parameters-guide]]"]
    if any(k in probe for k in ["视频", "video", "seedance", "可灵"]):
        links += ["[[ai_video_prompt_engineering]]", "[[Flux2 Kelin]]"]
    if any(k in probe for k in ["zimage", "z-image"]):
        links += ["[[z-image_prompt_knowledge]]"]
    if any(k in probe for k in ["photoshop", "photography", "cinematic", "摄影"]):
        links += ["[[Photoshop Cinematic Look Principles]]", "[[Photoshop Cinematic and CG Look Guide]]", "[[LoL 原画风格摄影转译与高级人像构图]]"]
    if "prompt" in probe or "提示词" in probe:
        links += ["[[提示词]]"]
    seen = set()
    return [link for link in links if not (link in seen or seen.add(link))]


def build_overview(item: dict[str, object], tags: list[str], headings: list[str]) -> str:
    title = str(item["title"])
    folder = str(Path(str(item["target"])).parent).replace("\\", "/")
    links = related_links(title, tags)
    lines = [
        f"# {title}",
        "",
        "> [!info] Import Summary",
        f"> - **来源:** Google Drive DOCX 批量导入",
        f"> - **分类:** `{folder}`",
        f"> - **状态:** 已转换为 Obsidian Markdown，建议后续人工精读压缩为永久笔记",
    ]
    if item.get("closest_existing") and float(item.get("closest_existing_similarity", 0)) >= 0.62:
        lines.append(f"> - **近似现有笔记:** [[{Path(str(item['closest_existing'])).stem}]]")
    if item.get("stats", {}).get("media"):
        lines += [
            "",
            "> [!warning] Embedded Media",
            f"> 原文档包含 {item['stats']['media']} 个嵌入媒体对象；当前笔记只保留文本结构，未抽取图片附件。",
        ]
    if headings:
        lines += ["", "## 导览", ""]
        for heading in headings[:12]:
            lines.append(f"- [[#{anchor_for(heading)}|{heading}]]")
    if links:
        lines += ["", "## 相关笔记", ""]
        lines.extend(f"- {link}" for link in links)
    lines += ["", "## 正文", ""]
    return "\n".join(lines)


def build_sensitive_note(old_fm: str, item: dict[str, object]) -> str:
    frontmatter = build_frontmatter(old_fm, item)
    title = str(item["title"])
    return f"""{frontmatter}

# {title}

> [!warning] Safety Review Required
> 这篇文档涉及平台审核规避或绕过主题。保留为来源索引和人工审查入口，不展开正文，也不整理为可操作步骤。

## 来源

- 原始格式：DOCX
- 导入状态：仅元数据占位
- 建议处理：如需保留，改写为平台安全规范、风险识别或合规边界笔记。
"""


def reformat_note(item: dict[str, object]) -> None:
    path = VAULT / str(item["target"])
    text = path.read_text(encoding="utf-8")
    old_fm, body = split_frontmatter(text)
    if item.get("sensitive_stub"):
        path.write_text(build_sensitive_note(old_fm, item), encoding="utf-8")
        return
    tags = parse_list(old_fm, "tags") or list(item.get("tags", []))
    title = str(item["title"])
    body = strip_import_header(body, title)
    normalized_body, headings = normalize_body(body)
    frontmatter = build_frontmatter(old_fm, item)
    overview = build_overview(item, tags, headings)
    path.write_text(f"{frontmatter}\n\n{overview}\n{normalized_body}\n", encoding="utf-8")


def main() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    reformatted = 0
    missing = []
    for item in report.get("imported", []):
        path = VAULT / str(item["target"])
        if not path.exists():
            missing.append(str(item["target"]))
            continue
        reformat_note(item)
        reformatted += 1
    summary = {"reformatted": reformatted, "missing": missing}
    (VAULT / "90_System" / "reformat_imported_markdown_report.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
