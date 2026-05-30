from __future__ import annotations

import argparse
import hashlib
import json
import re
import unicodedata
import zipfile
from datetime import date
from pathlib import Path
from xml.etree import ElementTree as ET


VAULT = Path(__file__).resolve().parents[1]
DOWNLOAD = Path(r"C:\Users\80998\Desktop\drive-download-20260523T041143Z-3-001")
REPORT = VAULT / "90_System" / "drive_download_20260523_import_report.json"
TODAY = date.today().isoformat()

DOCX_NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
}

STOPWORDS = {
    "the", "and", "for", "with", "that", "this", "from", "into", "using", "use",
    "are", "was", "were", "will", "can", "you", "your", "have", "has", "not",
    "\u4e00\u4e2a", "\u4e00\u79cd", "\u4ee5\u53ca", "\u8fdb\u884c", "\u901a\u8fc7",
    "\u53ef\u4ee5", "\u9700\u8981", "\u8fd9\u4e2a", "\u8fd9\u4e9b", "\u5bf9\u4e8e",
    "\u5982\u679c", "\u56e0\u4e3a", "\u6240\u4ee5", "\u5c31\u662f", "\u4e0d\u662f",
    "\u6ca1\u6709", "\u4f7f\u7528", "\u751f\u6210", "\u63d0\u793a\u8bcd",
}


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).lower()
    text = re.sub(r"\s+", "", text)
    text = re.sub(r"[^\w\u4e00-\u9fff]+", "", text)
    return text


def slugify(name: str) -> str:
    stem = Path(name).stem
    stem = unicodedata.normalize("NFKC", stem)
    stem = re.sub(r"\(\d+\)$", "", stem).strip()
    stem = stem.replace("\uff1a", " ")
    stem = re.sub(r'[\\/:*?"<>|]', " ", stem)
    stem = re.sub(r"\s+", " ", stem).strip()
    return stem.rstrip(" .") or "Untitled"


def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def tokenize(text: str) -> set[str]:
    normalized = unicodedata.normalize("NFKC", text).lower()
    tokens = set(re.findall(r"[a-z0-9][a-z0-9_-]{2,}", normalized))
    for segment in re.findall(r"[\u4e00-\u9fff]{2,}", normalized):
        if len(segment) <= 12:
            tokens.add(segment)
        for size in (2, 3):
            for index in range(0, len(segment) - size + 1):
                tokens.add(segment[index:index + size])
    return {token for token in tokens if token not in STOPWORDS}


def digest_text(text: str) -> str:
    return hashlib.sha256(normalize_text(text).encode("utf-8")).hexdigest()


def jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def docx_paragraph_text(paragraph: ET.Element) -> str:
    parts: list[str] = []
    for node in paragraph.iter():
        tag = node.tag.rsplit("}", 1)[-1]
        if tag == "t" and node.text:
            parts.append(node.text)
        elif tag == "tab":
            parts.append("\t")
        elif tag == "br":
            parts.append("\n")
    return "".join(parts).strip()


def extract_docx(path: Path) -> tuple[str, dict[str, int]]:
    with zipfile.ZipFile(path) as zf:
        root = ET.fromstring(zf.read("word/document.xml"))
        lines: list[str] = []
        paragraphs = 0
        tables = 0
        for child in root.findall(".//w:body/*", DOCX_NS):
            tag = child.tag.rsplit("}", 1)[-1]
            if tag == "p":
                text = docx_paragraph_text(child)
                if text:
                    lines.append(text)
                    paragraphs += 1
            elif tag == "tbl":
                tables += 1
                rows: list[str] = []
                for tr in child.findall(".//w:tr", DOCX_NS):
                    cells = []
                    for tc in tr.findall("./w:tc", DOCX_NS):
                        cell_texts = [docx_paragraph_text(p) for p in tc.findall(".//w:p", DOCX_NS)]
                        cell_text = " ".join(t for t in cell_texts if t)
                        cells.append(cell_text.replace("|", "\\|"))
                    if any(cells):
                        rows.append("| " + " | ".join(cells) + " |")
                if rows:
                    if len(rows) > 1:
                        column_count = rows[0].count("|") - 1
                        sep = "| " + " | ".join(["---"] * column_count) + " |"
                        lines.extend([rows[0], sep, *rows[1:]])
                    else:
                        lines.extend(rows)
                    lines.append("")
        media_count = len([name for name in zf.namelist() if name.startswith("word/media/")])
        stats = {"paragraphs": paragraphs, "tables": tables, "media": media_count}
        return "\n\n".join(lines).strip(), stats


def load_existing_notes() -> list[dict[str, object]]:
    notes: list[dict[str, object]] = []
    for path in VAULT.rglob("*.md"):
        if ".git" in path.parts or ".obsidian" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        notes.append(
            {
                "path": path,
                "name": path.stem,
                "slug": normalize_text(path.stem),
                "digest": digest_text(text),
                "tokens": tokenize(text),
                "chars": len(text),
            }
        )
    return notes


def has_any(probe: str, needles: list[str]) -> bool:
    return any(needle in probe for needle in needles)


def classify(title: str, text: str, filename: str) -> tuple[Path, list[str], str, bool]:
    probe = f"{title}\n{filename}\n{text[:3000]}".lower()
    title_probe = f"{title}\n{filename}".lower()
    tags = ["imported/drive-download", "source/docx"]
    reason = "\u6309\u5185\u5bb9\u4e3b\u9898\u5f52\u5165\u53ef\u590d\u7528\u77e5\u8bc6\u7b14\u8bb0\u3002"
    target = VAULT / "02_Knowledge" / "AIGC"
    sensitive = False

    if (
        has_any(title_probe, [
            "\u5ba1\u6838\u89c4\u907f", "\u89c4\u907f\u5ba1\u6838", "\u7ed5\u8fc7\u5ba1\u6838",
            "bypass", "moderation_bypass", "jailbreak", "\u8d8a\u72f1",
        ])
        or ("\u5ba1\u6838" in probe and has_any(probe, ["\u7ed5\u8fc7", "\u8d8a\u72f1", "\u89c4\u907f"]))
        or ("moderation" in probe and "bypass" in probe)
    ):
        target = VAULT / "03_Resources" / "References"
        tags += ["source-material", "safety-review"]
        reason = (
            "\u6d89\u53ca\u5e73\u53f0\u5ba1\u6838\u6216\u89c4\u907f\u4e3b\u9898\uff0c"
            "\u4ec5\u8bb0\u5f55\u5143\u6570\u636e\u5e76\u7559\u4f5c\u5f85\u5ba1\u6e90\u6750\u6599\uff0c"
            "\u4e0d\u8f6c\u6362\u4e3a\u53ef\u64cd\u4f5c\u77e5\u8bc6\u7b14\u8bb0\u3002"
        )
        sensitive = True
    elif has_any(title_probe, ["\u51cf\u80a5", "\u996e\u98df", "\u5065\u8eab", "weight loss"]) or (
        "\u51cf\u80a5" in probe and has_any(probe, ["\u996e\u98df", "\u70ed\u91cf", "\u8bad\u7ec3", "hiit"])
    ):
        target = VAULT / "00_Inbox"
        tags += ["health", "fitness"]
        reason = "\u4e2a\u4eba\u8ba1\u5212\u7c7b\u5185\u5bb9\u9700\u8981\u540e\u7eed\u786e\u8ba4\uff0c\u4e0d\u76f4\u63a5\u6c89\u6dc0\u4e3a\u957f\u671f\u77e5\u8bc6\u3002"
    elif has_any(probe, ["zimage", "z-image", "architecture", "policy"]):
        target = VAULT / "02_Knowledge" / "AIGC"
        tags += ["aigc", "model-notes"]
        reason = "AIGC \u6a21\u578b\u548c\u751f\u6210\u7b56\u7565\u7c7b\u5185\u5bb9\u3002"
    elif has_any(probe, [
        "midjourney", "nano banana", "prompt", "\u63d0\u793a\u8bcd", "video", "seedance",
        "\u53ef\u7075", "\u89c6\u9891", "sora", "gemini",
    ]):
        target = VAULT / "02_Knowledge" / "AIGC"
        if has_any(probe, ["video", "seedance", "\u53ef\u7075", "\u89c6\u9891", "sora"]):
            tags += ["aigc", "video-generation"]
            reason = "AI \u89c6\u9891\u751f\u6210\u5de5\u4f5c\u6d41\u548c\u63d0\u793a\u8bcd\u89c4\u8303\u3002"
        else:
            tags += ["aigc", "prompt-engineering"]
            reason = "AIGC \u63d0\u793a\u8bcd\u5de5\u7a0b\u7c7b\u77e5\u8bc6\u3002"
    elif has_any(probe, [
        "photoshop", "\u6444\u5f71", "cinematic", "cg\u611f", "\u4eba\u50cf",
        "visual storytelling", "atmospheric perspective",
    ]):
        target = VAULT / "02_Knowledge" / "Photography"
        tags += ["photography", "visual-design"]
        reason = "\u6444\u5f71\u3001\u5f71\u50cf\u540e\u671f\u4e0e\u89c6\u89c9\u53d9\u4e8b\u65b9\u6cd5\uff0c\u5f52\u5165 Photography\u3002"
    elif has_any(probe, [
        "\u4f2f\u91cc\u66fc", "\u4eba\u4f53", "\u6f2b\u753b\u8eab\u6750", "\u89d2\u8272\u539f\u753b",
        "\u89d2\u8272\u8bbe\u8ba1", "\u7d20\u4f53", "\u900f\u89c6\u7ed3\u6784", "lol",
        "\u82f1\u96c4\u8054\u76df", "\u539f\u753b", "composition", "planar",
    ]):
        target = VAULT / "02_Knowledge" / "Photography"
        tags += ["visual-design", "character-art"]
        reason = "\u89d2\u8272\u539f\u753b\u3001\u6784\u56fe\u4e0e\u4eba\u4f53\u7ed3\u6784\u65b9\u6cd5\uff0c\u5f52\u5165 Photography \u4e0b\u7684\u89c6\u89c9\u8bbe\u8ba1\u77e5\u8bc6\u3002"
    return target, sorted(set(tags)), reason, sensitive


def first_headings(text: str, limit: int = 8) -> list[str]:
    headings = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or len(stripped) > 80:
            continue
        if re.match(r"^#{1,6}\s+", stripped):
            headings.append(stripped.lstrip("# ").strip())
        elif re.match(r"^([\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341]+[\u3001.\uff0e]|[\u7b2c][\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341]+[\u7ae0\u8282]|[0-9]+[.\uff0e\u3001])", stripped):
            headings.append(stripped)
        elif stripped.endswith(("\uff1a", ":")) and len(stripped) <= 40:
            headings.append(stripped.rstrip("\uff1a:"))
        if len(headings) >= limit:
            break
    return headings


def body_to_markdown(text: str) -> str:
    lines = []
    previous_blank = True
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            if not previous_blank:
                lines.append("")
                previous_blank = True
            continue
        if re.match(r"^([\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341]+[\u3001.\uff0e]|\u7b2c[\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341]+[\u7ae0\u8282]|[0-9]+[.\uff0e\u3001])", line) and len(line) <= 90:
            lines.append(f"## {line}")
        else:
            lines.append(line)
        previous_blank = False
    return "\n".join(lines).strip()


def build_note(title: str, source: Path, target_folder: Path, tags: list[str], text: str, stats: dict[str, int], reason: str) -> str:
    headings = first_headings(text)
    tag_yaml = "\n".join(f"  - {tag}" for tag in tags)
    heading_yaml = "\n".join(f"  - {yaml_quote(h)}" for h in headings) if headings else "  - none"
    frontmatter = f"""---
title: {yaml_quote(title)}
aliases:
  - {yaml_quote(source.stem)}
tags:
{tag_yaml}
source_file: {yaml_quote(str(source))}
imported: {TODAY}
original_format: docx
target_folder: {yaml_quote(str(target_folder.relative_to(VAULT)).replace(chr(92), "/"))}
word_paragraphs: {stats["paragraphs"]}
word_tables: {stats["tables"]}
embedded_media_count: {stats["media"]}
detected_headings:
{heading_yaml}
---
"""
    note_header = f"""
# {title}

> [!info] Import Note
> \u4ece Google Drive \u4e0b\u8f7d\u76ee\u5f55\u4e2d\u7684 DOCX \u6279\u91cf\u8f6c\u6362\u3002\u5206\u7c7b\u4f9d\u636e\uff1a{reason}
"""
    if stats["media"]:
        note_header += f"""
> [!warning] Embedded Media
> \u539f DOCX \u5305\u542b {stats["media"]} \u4e2a\u5d4c\u5165\u5a92\u4f53\u5bf9\u8c61\u3002\u672c\u6b21\u5bfc\u5165\u4ee5\u6587\u672c\u77e5\u8bc6\u5316\u4e3a\u4e3b\uff0c\u672a\u81ea\u52a8\u62bd\u53d6\u56fe\u7247\u9644\u4ef6\u3002
"""
    return f"{frontmatter}{note_header}\n{body_to_markdown(text)}\n"


def build_sensitive_stub(title: str, source: Path, target_folder: Path, tags: list[str], stats: dict[str, int], reason: str) -> str:
    tag_yaml = "\n".join(f"  - {tag}" for tag in tags)
    frontmatter = f"""---
title: {yaml_quote(title)}
aliases:
  - {yaml_quote(source.stem)}
tags:
{tag_yaml}
source_file: {yaml_quote(str(source))}
imported: {TODAY}
original_format: docx
target_folder: {yaml_quote(str(target_folder.relative_to(VAULT)).replace(chr(92), "/"))}
word_paragraphs: {stats["paragraphs"]}
word_tables: {stats["tables"]}
embedded_media_count: {stats["media"]}
safety_review_required: true
---
"""
    return f"""{frontmatter}
# {title}

> [!warning] Safety Review Required
> {reason}

\u539f\u59cb DOCX \u4fdd\u7559\u5728\u4e0b\u8f7d\u76ee\u5f55\uff0c\u672a\u5c06\u6b63\u6587\u8f6c\u6362\u8fdb vault\u3002
"""


def unique_path(folder: Path, title: str) -> Path:
    folder.mkdir(parents=True, exist_ok=True)
    base = slugify(title)
    path = folder / f"{base}.md"
    if not path.exists():
        return path
    index = 2
    while True:
        candidate = folder / f"{base} {index}.md"
        if not candidate.exists():
            return candidate
        index += 1


def duplicate_match(path: Path, title: str, digest: str, tokens: set[str], existing: list[dict[str, object]], seen_docx_digests: dict[str, Path]) -> tuple[str, str, float, str]:
    if digest in seen_docx_digests:
        return "duplicate within download folder", str(seen_docx_digests[digest]), 1.0, str(seen_docx_digests[digest])

    exact = next((n for n in existing if n["digest"] == digest), None)
    if exact:
        rel = str(Path(exact["path"]).relative_to(VAULT))
        return "exact content duplicate in vault", rel, 1.0, rel

    title_slug = normalize_text(title)
    title_match = next((n for n in existing if n["slug"] == title_slug), None)
    if title_match:
        sim = jaccard(tokens, title_match["tokens"])
        rel = str(Path(title_match["path"]).relative_to(VAULT))
        return f"same title already in vault; token similarity {sim:.2f}", rel, sim, rel

    scored = [(jaccard(tokens, n["tokens"]), n) for n in existing if n["tokens"]]
    scored.sort(key=lambda x: x[0], reverse=True)
    if not scored:
        return "", "", 0.0, ""
    closest_similarity, closest_note = scored[0]
    closest_path = str(Path(closest_note["path"]).relative_to(VAULT))
    if closest_similarity >= 0.62:
        return f"high content similarity {closest_similarity:.2f}", closest_path, closest_similarity, closest_path
    return "", "", closest_similarity, closest_path


def analyze_or_import(write: bool) -> dict[str, object]:
    existing = load_existing_notes()
    imported = []
    skipped = []
    analyzed = []
    seen_docx_digests: dict[str, Path] = {}

    for path in sorted(DOWNLOAD.iterdir(), key=lambda p: p.name.lower()):
        if path.is_dir():
            continue
        suffix = path.suffix.lower()
        if suffix != ".docx":
            skipped.append({"source": str(path), "reason": f"unsupported format: {suffix}"})
            continue

        title = slugify(path.name)
        text, stats = extract_docx(path)
        if not text:
            skipped.append({"source": str(path), "reason": "empty extracted text"})
            continue

        digest = digest_text(text)
        tokens = tokenize(text)
        duplicate_reason, duplicate_of, closest_similarity, closest_path = duplicate_match(
            path, title, digest, tokens, existing, seen_docx_digests
        )

        if duplicate_reason:
            skipped.append(
                {
                    "source": str(path),
                    "title": title,
                    "reason": duplicate_reason,
                    "duplicate_of": duplicate_of,
                    "closest_existing_similarity": round(closest_similarity, 3),
                    "closest_existing": closest_path,
                    "stats": stats,
                }
            )
            seen_docx_digests.setdefault(digest, path)
            continue

        target, tags, reason, sensitive = classify(title, text, path.name)
        target_path = unique_path(target, title)
        record = {
            "source": str(path),
            "title": title,
            "target": str(target_path.relative_to(VAULT)),
            "tags": tags,
            "reason": reason,
            "sensitive_stub": sensitive,
            "closest_existing_similarity": round(closest_similarity, 3),
            "closest_existing": closest_path,
            "chars": len(text),
            "tokens": len(tokens),
            "stats": stats,
            "headings": first_headings(text),
        }
        analyzed.append(record)
        seen_docx_digests[digest] = path
        if write:
            if sensitive:
                target_path.write_text(build_sensitive_stub(title, path, target, tags, stats, reason), encoding="utf-8")
            else:
                target_path.write_text(build_note(title, path, target, tags, text, stats, reason), encoding="utf-8")
            imported.append(record)

    result = {
        "download_dir": str(DOWNLOAD),
        "vault": str(VAULT),
        "write": write,
        "analyzed_count": len(analyzed),
        "imported_count": len(imported),
        "skipped_count": len(skipped),
        "analyzed": analyzed,
        "imported": imported,
        "skipped": skipped,
    }
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write converted markdown notes")
    args = parser.parse_args()
    result = analyze_or_import(args.write)
    print(json.dumps(
        {
            "write": result["write"],
            "analyzed_count": result["analyzed_count"],
            "imported_count": result["imported_count"],
            "skipped_count": result["skipped_count"],
            "report": str(REPORT),
        },
        ensure_ascii=False,
        indent=2,
    ))


if __name__ == "__main__":
    main()
