#!/usr/bin/env python
"""Optimize image attachments for Obsidian notes.

Requires Pillow. The script writes optimized copies and never deletes source
files. Use it to create compact WebP attachments before embedding them in notes.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from PIL import Image, ImageOps
except Exception as exc:  # pragma: no cover - import guard for CLI use
    print(
        "Pillow is required. Install it with: python -m pip install pillow",
        file=sys.stderr,
    )
    print(f"Import error: {exc}", file=sys.stderr)
    sys.exit(2)


SUPPORTED_EXTENSIONS = {
    ".bmp",
    ".jpeg",
    ".jpg",
    ".png",
    ".tif",
    ".tiff",
    ".webp",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Optimize local images for Obsidian attachment folders."
    )
    parser.add_argument("inputs", nargs="+", help="Image files or directories.")
    parser.add_argument(
        "--output-dir",
        help="Destination directory. Defaults to each input file's directory.",
    )
    parser.add_argument(
        "--format",
        choices=["webp", "jpeg", "png"],
        default="webp",
        help="Output format. Default: webp.",
    )
    parser.add_argument(
        "--quality",
        type=int,
        default=82,
        help="Lossy quality for WebP/JPEG, 1-100. Default: 82.",
    )
    parser.add_argument(
        "--max-edge",
        type=int,
        default=1800,
        help="Resize so the longest edge is at most this many pixels. Use 0 to disable. Default: 1800.",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Recurse into input directories.",
    )
    parser.add_argument(
        "--name-prefix",
        help="Rename outputs as <prefix>-01.<ext>, <prefix>-02.<ext>, ...",
    )
    parser.add_argument(
        "--start-index",
        type=int,
        default=1,
        help="Starting index when --name-prefix is used. Default: 1.",
    )
    parser.add_argument(
        "--digits",
        type=int,
        default=2,
        help="Index digits when --name-prefix is used. Default: 2.",
    )
    parser.add_argument(
        "--min-savings-ratio",
        type=float,
        default=0.05,
        help="Skip output if it is not at least this fraction smaller than the source. Default: 0.05.",
    )
    parser.add_argument(
        "--always-write",
        action="store_true",
        help="Keep the optimized output even when it is larger than the source.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing output files.",
    )
    parser.add_argument(
        "--manifest",
        help="Optional path to write the JSON manifest.",
    )
    return parser.parse_args()


def collect_inputs(inputs: list[str], recursive: bool) -> list[Path]:
    files: list[Path] = []
    for raw in inputs:
        path = Path(raw)
        if path.is_dir():
            pattern = "**/*" if recursive else "*"
            for child in path.glob(pattern):
                if child.is_file() and child.suffix.lower() in SUPPORTED_EXTENSIONS:
                    files.append(child)
        elif path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
            files.append(path)
    return sorted(dict.fromkeys(p.resolve() for p in files))


def has_transparency(image: Image.Image) -> bool:
    if image.mode in {"RGBA", "LA"}:
        return True
    if image.mode == "P" and "transparency" in image.info:
        return True
    return False


def normalize_image(image: Image.Image, output_format: str) -> Image.Image:
    image = ImageOps.exif_transpose(image)
    if output_format == "jpeg":
        if image.mode in {"RGBA", "LA", "P"} and has_transparency(image):
            background = Image.new("RGB", image.size, (255, 255, 255))
            background.paste(image.convert("RGBA"), mask=image.convert("RGBA").split()[-1])
            return background
        return image.convert("RGB")
    if output_format == "webp":
        return image.convert("RGBA" if has_transparency(image) else "RGB")
    if output_format == "png":
        return image.convert("RGBA" if has_transparency(image) else "RGB")
    return image


def resize_if_needed(image: Image.Image, max_edge: int) -> Image.Image:
    if max_edge <= 0:
        return image
    width, height = image.size
    longest = max(width, height)
    if longest <= max_edge:
        return image
    scale = max_edge / longest
    size = (max(1, round(width * scale)), max(1, round(height * scale)))
    return image.resize(size, Image.Resampling.LANCZOS)


def target_path(
    source: Path,
    output_dir: Path | None,
    output_format: str,
    index: int,
    args: argparse.Namespace,
) -> Path:
    suffix = ".jpg" if output_format == "jpeg" else f".{output_format}"
    directory = output_dir if output_dir else source.parent
    if args.name_prefix:
        stem = f"{args.name_prefix}-{index:0{args.digits}d}"
    else:
        stem = source.stem
        if source.suffix.lower() == suffix and directory.resolve() == source.parent.resolve():
            stem = f"{stem}-optimized"
    return directory / f"{stem}{suffix}"


def save_image(image: Image.Image, destination: Path, output_format: str, quality: int) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if output_format == "webp":
        image.save(destination, "WEBP", quality=quality, method=6)
    elif output_format == "jpeg":
        image.save(destination, "JPEG", quality=quality, optimize=True, progressive=True)
    elif output_format == "png":
        image.save(destination, "PNG", optimize=True)
    else:
        raise ValueError(f"Unsupported output format: {output_format}")


def optimize_one(
    source: Path,
    destination: Path,
    args: argparse.Namespace,
) -> dict[str, object]:
    if destination.exists() and not args.overwrite:
        return {
            "source": str(source),
            "output": str(destination),
            "status": "skipped",
            "reason": "output_exists",
        }

    source_bytes = source.stat().st_size
    with Image.open(source) as opened:
        original_width, original_height = opened.size
        image = normalize_image(opened, args.format)
        image = resize_if_needed(image, args.max_edge)
        width, height = image.size
        save_image(image, destination, args.format, args.quality)

    output_bytes = destination.stat().st_size
    savings_ratio = 1 - (output_bytes / source_bytes) if source_bytes else 0

    if not args.always_write and savings_ratio < args.min_savings_ratio:
        destination.unlink(missing_ok=True)
        return {
            "source": str(source),
            "output": str(destination),
            "status": "skipped",
            "reason": "insufficient_savings",
            "source_bytes": source_bytes,
            "output_bytes": output_bytes,
            "savings_ratio": round(savings_ratio, 4),
            "original_width": original_width,
            "original_height": original_height,
            "width": width,
            "height": height,
        }

    return {
        "source": str(source),
        "output": str(destination),
        "status": "created",
        "source_bytes": source_bytes,
        "output_bytes": output_bytes,
        "savings_ratio": round(savings_ratio, 4),
        "original_width": original_width,
        "original_height": original_height,
        "width": width,
        "height": height,
    }


def main() -> int:
    args = parse_args()
    output_dir = Path(args.output_dir).resolve() if args.output_dir else None
    sources = collect_inputs(args.inputs, args.recursive)

    manifest: dict[str, object] = {
        "created": [],
        "skipped": [],
        "errors": [],
    }

    if not sources:
        manifest["errors"].append({"reason": "no_supported_images"})

    for offset, source in enumerate(sources):
        destination = target_path(
            source,
            output_dir,
            args.format,
            args.start_index + offset,
            args,
        )
        try:
            result = optimize_one(source, destination, args)
            if result["status"] == "created":
                manifest["created"].append(result)
            else:
                manifest["skipped"].append(result)
        except Exception as exc:
            manifest["errors"].append(
                {"source": str(source), "reason": type(exc).__name__, "detail": str(exc)}
            )

    manifest["ok"] = not manifest["errors"]
    text = json.dumps(manifest, ensure_ascii=False, indent=2)
    if args.manifest:
        Path(args.manifest).write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if manifest["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
