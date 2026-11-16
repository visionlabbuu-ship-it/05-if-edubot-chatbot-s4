"""Extract text from full MG400 corpus and write cleaned Markdown + chunk JSONL."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

# Allow running as script: python scripts/preprocess.py
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bs4 import BeautifulSoup
from pypdf import PdfReader
from tqdm import tqdm

from config import settings

TEXT_SUFFIXES = {
    ".md",
    ".py",
    ".txt",
    ".lua",
    ".cs",
    ".cpp",
    ".h",
    ".hpp",
    ".c",
    ".srv",
    ".msg",
    ".json",
    ".html",
    ".htm",
    ".pdf",
}


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = re.sub(r"[\s_-]+", "-", text)
    return text[:100] or "doc"


def file_sha1(path: Path) -> str:
    h = hashlib.sha1()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def clean_text(text: str) -> str:
    text = text.replace("\x00", " ")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def should_skip_path(path_str: str) -> bool:
    p = path_str.replace("\\", "/")
    for part in settings.SKIP_PATH_PARTS:
        if part.replace("\\", "/") in p:
            return True
    return False


def resolve_source_path(rel: str) -> Path | None:
    """Resolve corpus-relative path or curated:filename."""
    if rel.startswith("curated:"):
        name = rel.split(":", 1)[1]
        path = settings.CURATED_DIR / name
        return path if path.exists() else None
    path = settings.CORPUS_RAW / rel
    return path if path.exists() else None


def extract_pdf(path: Path) -> list[dict]:
    try:
        reader = PdfReader(str(path))
    except Exception as exc:  # noqa: BLE001
        print(f"[WARN] PDF open failed: {path.name}: {exc}")
        return []
    pages = []
    for i, page in enumerate(reader.pages, start=1):
        try:
            raw = page.extract_text() or ""
        except Exception as exc:  # noqa: BLE001
            raw = f"[PDF extract error on page {i}: {exc}]"
        text = clean_text(raw)
        if text:
            pages.append({"page": i, "text": text})
    return pages


def extract_text_file(path: Path) -> str:
    for enc in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
        try:
            return clean_text(path.read_text(encoding=enc))
        except UnicodeDecodeError:
            continue
    return clean_text(path.read_bytes().decode("utf-8", errors="replace"))


def scrub_html_noise(text: str) -> str:
    """Drop nav/footer/marketing lines common on Dobot web pages."""
    patterns = [re.compile(p, re.I) for p in settings.HTML_NOISE_LINE_PATTERNS]
    # Multi-line noise blocks
    block_noise = re.compile(
        r"(?is)(Products\s+Industries\s+Applications.*?)(?=Q:|Which |What |Does |How |The MG400|Port |\Z)",
    )
    text = block_noise.sub("\n", text)
    text = re.sub(
        r"(?is)Did it solve your problem\?.*?support@dobot-robots\.com",
        "",
        text,
    )
    text = re.sub(
        r"(?is)Subscribe to the latest updates.*?Contact Us",
        "",
        text,
    )
    text = re.sub(
        r"(?is)Products\s+CRA Series.*?Research Lab",
        "",
        text,
    )
    kept: list[str] = []
    for line in text.splitlines():
        s = line.strip()
        if not s:
            kept.append("")
            continue
        if any(p.match(s) for p in patterns):
            continue
        # Drop pure product-menu one-liners
        if s in {
            "CRA Series",
            "Nova Series",
            "CRS Series",
            "Magician E6",
            "MG400",
            "M1 Pro",
            "X-Trainer",
            "Automotive",
            "Consumer Electronics",
            "Education",
            "Food & Beverage",
            "Healthcare",
            "Metal Processing",
            "Semiconductor",
            "Research Lab",
            "Welding",
            "Palletizing",
            "Loading and Unloading",
            "Assembly",
            "Bin Picking",
            "Gluing",
        }:
            continue
        kept.append(s)
    return clean_text("\n".join(kept))


def extract_html(path: Path, *, scrub: bool = True) -> str:
    html = path.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(html, "lxml")
    for tag in soup(["script", "style", "noscript", "svg", "nav", "footer", "header"]):
        tag.decompose()
    # Prefer FAQ/question regions when present
    main = (
        soup.find("main")
        or soup.find("article")
        or soup.find(class_=re.compile(r"(faq|content|main|article)", re.I))
        or soup.body
        or soup
    )
    text = main.get_text("\n", strip=True)
    text = clean_text(text)
    if scrub:
        text = scrub_html_noise(text)
    return text


def is_excluded_tight(meta: dict) -> bool:
    """Return True if source should be dropped in tight mode."""
    path = str(meta.get("path") or "").replace("\\", "/")
    doc_type = str(meta.get("doc_type") or "")

    # Always keep curated cards and training lua demos
    if doc_type in {"cheat_sheet", "demo_script"}:
        return False
    if path.startswith("curated:"):
        return False

    for sub in settings.TIGHT_EXCLUDE_PATH_SUBSTRINGS:
        if sub.replace("\\", "/") in path:
            return True
    if doc_type in settings.TIGHT_DOC_TYPES_DROP:
        return True

    # Drop multi-SDK trees (C++/C#/ROS) — Python only in tight
    if any(
        x in path
        for x in (
            "tcp-ip-4axis-cpp_repo",
            "tcp-ip-4axis-csharp_repo",
            "mg400-ros_repo",
            "05_case_application_pages",
        )
    ):
        return True

    # Drop duplicate training chapter PDFs (Ch1,3-6); Ch2 PDF kept as palletizing fallback
    # Lua scripts are allowed above via demo_script
    if "training-system-user-guide_2023-02-06_en_extracted" in path and path.endswith(".pdf"):
        if "/Chapter2/" in path or "\\Chapter2\\" in path:
            return False
        if any(f"/Chapter{n}/" in path for n in (1, 3, 4, 5, 6)):
            return True

    for sub in settings.TIGHT_DROP_PATH_SUBSTRINGS:
        sub_n = sub.replace("\\", "/")
        if sub_n in path and doc_type != "demo_script":
            # path-based drops already handled for multi-SDK; skip chapter strings here if lua
            if "training-system-user-guide" in sub_n:
                continue
            return True
    return False


def collect_tight_extra_sources(seen_paths: set[str]) -> list[dict]:
    """Chapter2 palletizing PDF + training Lua (high-signal, small)."""
    sources: list[dict] = []
    base = (
        settings.CORPUS_RAW
        / "03_demo_training"
        / "official_mg400_demo_training-system-user-guide_2023-02-06_en_extracted"
    )
    if not base.exists():
        return sources

    # Palletizing chapter replaces corrupt top-level palletizing PDF
    ch2 = list(base.glob("Chapter2/*.pdf"))
    for path in ch2:
        rel = str(path.relative_to(settings.CORPUS_RAW)).replace("\\", "/")
        if rel in seen_paths:
            continue
        sources.append(
            {
                "path": rel,
                "doc_title": f"Training System: {path.stem}",
                "doc_type": "demo_guide",
                "doc_version": "2023-02-06",
                "publish_date": "2023-02-06",
                "language": "en",
                "robot_model": "mg400",
                "axis_family": "4-axis",
                "applicability": "direct_mg400",
                "priority": "high",
                "safety_level": "caution",
                "source_type": "official_demo",
            }
        )
        seen_paths.add(rel)

    # Lua demos only (skip project JSON)
    for path in sorted(base.rglob("*.lua")):
        rel = str(path.relative_to(settings.CORPUS_RAW)).replace("\\", "/")
        if rel in seen_paths or should_skip_path(rel):
            continue
        # skip pure coordinate dumps if named point.json.lua and huge noise
        parent = path.parent.name
        sources.append(
            {
                "path": rel,
                "doc_title": f"Training Lua: {parent}/{path.name}",
                "doc_type": "demo_script",
                "doc_version": "2023-02-06",
                "publish_date": "2023-02-06",
                "language": "en",
                "robot_model": "mg400",
                "axis_family": "4-axis",
                "applicability": "direct_mg400",
                "priority": "medium",
                "safety_level": "caution",
                "source_type": "official_demo",
                "code_related": True,
            }
        )
        seen_paths.add(rel)
    return sources


def extract_alarm_json(path: Path) -> str:
    """Flatten alarm JSON into readable one-entry-per-block text."""
    data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    lines: list[str] = [f"# Alarm catalog: {path.name}", ""]
    if isinstance(data, list):
        for item in data:
            if not isinstance(item, dict):
                lines.append(str(item))
                continue
            eid = item.get("id") or item.get("error_id") or item.get("code") or "?"
            en = item.get("en") or item.get("description") or item.get("desc") or ""
            zh = item.get("zh_CN") or item.get("zh") or ""
            level = item.get("level") or item.get("type") or ""
            solution = item.get("solution") or item.get("en_solution") or ""
            lines.append(f"## Alarm/Error ID: {eid}")
            if level:
                lines.append(f"Level: {level}")
            if en:
                lines.append(f"Description (EN): {en}")
            if zh:
                lines.append(f"Description (ZH): {zh}")
            if solution:
                lines.append(f"Solution: {solution}")
            extra = {
                k: v
                for k, v in item.items()
                if k
                not in {
                    "id",
                    "error_id",
                    "code",
                    "en",
                    "description",
                    "desc",
                    "zh_CN",
                    "zh",
                    "level",
                    "type",
                    "solution",
                    "en_solution",
                }
                and v not in (None, "", [], {})
            }
            if extra:
                lines.append(f"Extra: {json.dumps(extra, ensure_ascii=False)[:500]}")
            lines.append("")
    elif isinstance(data, dict):
        for key, value in data.items():
            lines.append(f"## {key}")
            lines.append(json.dumps(value, ensure_ascii=False, indent=2)[:2000])
            lines.append("")
    else:
        lines.append(str(data))
    return clean_text("\n".join(lines))


def chunk_text(
    text: str,
    *,
    chunk_size: int,
    overlap: int,
    prefer_code: bool = False,
) -> list[str]:
    text = clean_text(text)
    if not text:
        return []

    if prefer_code:
        parts = re.split(r"\n(?=(?:def |class |## |# |\*\*|public |private |namespace ))", text)
        units: list[str] = []
        buf = ""
        for part in parts:
            part = part.strip()
            if not part:
                continue
            if len(buf) + len(part) + 1 <= chunk_size:
                buf = f"{buf}\n\n{part}".strip()
            else:
                if buf:
                    units.append(buf)
                if len(part) <= chunk_size:
                    buf = part
                else:
                    units.extend(_window(part, chunk_size, overlap))
                    buf = ""
        if buf:
            units.append(buf)
        return [u for u in units if u.strip()]

    return _window(text, chunk_size, overlap)


def _window(text: str, chunk_size: int, overlap: int) -> list[str]:
    if len(text) <= chunk_size:
        return [text]
    chunks: list[str] = []
    start = 0
    n = len(text)
    while start < n:
        end = min(start + chunk_size, n)
        if end < n:
            window = text[start:end]
            break_at = max(window.rfind("\n\n"), window.rfind("\n"), window.rfind(". "))
            if break_at > chunk_size * 0.4:
                end = start + break_at + 1
        piece = text[start:end].strip()
        if piece:
            chunks.append(piece)
        if end >= n:
            break
        start = max(0, end - overlap)
    return chunks


def write_markdown(out_path: Path, meta: dict, body: str) -> None:
    header = [
        "---",
        f"doc_title: {meta.get('doc_title', '')}",
        f"doc_type: {meta.get('doc_type', '')}",
        f"robot_model: {meta.get('robot_model', 'mg400')}",
        f"axis_family: {meta.get('axis_family', '4-axis')}",
        f"applicability: {meta.get('applicability', '')}",
        f"priority: {meta.get('priority', '')}",
        f"safety_level: {meta.get('safety_level', 'normal')}",
        f"source_type: {meta.get('source_type', '')}",
        f"doc_version: {meta.get('doc_version', '')}",
        f"language: {meta.get('language', '')}",
        f"source_path: {meta.get('source_path', '')}",
        "---",
        "",
        f"# {meta.get('doc_title', out_path.stem)}",
        "",
        body,
        "",
    ]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(header), encoding="utf-8")


def process_source(meta: dict) -> list[dict]:
    rel = meta["path"]
    src = resolve_source_path(rel)
    if src is None:
        print(f"[WARN] missing: {rel}")
        return []

    if should_skip_path(str(src)):
        print(f"[SKIP] {rel}")
        return []

    sha = file_sha1(src)
    source_path = rel if rel.startswith("curated:") else str(rel).replace("\\", "/")
    base_meta = {
        **{k: v for k, v in meta.items() if k != "path"},
        "path": rel,
        "source_path": source_path,
        "source_sha1": sha,
        "code_related": bool(meta.get("code_related", False)),
    }
    # Unique slug: title + short path hash (avoids duplicate Chroma IDs across similar filenames)
    path_tag = hashlib.sha1(source_path.encode("utf-8")).hexdigest()[:10]
    out_slug = f"{slugify(meta.get('doc_title') or src.stem)}-{path_tag}"

    md_path = settings.PROCESSED_DIR / "markdown" / f"{out_slug}.md"
    chunks: list[dict] = []
    prefer_code = base_meta["doc_type"] in {
        "sdk_code",
        "api_reference",
        "error_code",
        "ros_api",
        "demo_script",
        "cheat_sheet",
    }

    suffix = src.suffix.lower()
    if suffix == ".pdf":
        pages = extract_pdf(src)
        if not pages:
            print(f"[WARN] no extractable text: {rel}")
            # still record empty body for transparency
            write_markdown(md_path, base_meta, "_[No extractable text layer in this PDF]_")
            return []
        body_parts = []
        for page in pages:
            body_parts.append(f"## Page {page['page']}\n\n{page['text']}")
            page_chunks = chunk_text(
                page["text"],
                chunk_size=settings.CHUNK_SIZE,
                overlap=settings.CHUNK_OVERLAP,
                prefer_code=prefer_code,
            )
            for idx, ch in enumerate(page_chunks):
                chunks.append(
                    {
                        "id": f"{out_slug}-p{page['page']}-c{idx}",
                        "text": ch,
                        "page": page["page"],
                        "section": f"page_{page['page']}",
                        **base_meta,
                    }
                )
        write_markdown(md_path, base_meta, "\n\n".join(body_parts))
    elif suffix == ".json":
        # Only treat known alarm catalogs as structured alarms; other JSON as text
        name_l = src.name.lower()
        if "alarm" in name_l:
            body = extract_alarm_json(src)
            write_markdown(md_path, base_meta, body)
            for idx, block in enumerate(re.split(r"\n(?=## )", body)):
                block = block.strip()
                if not block:
                    continue
                pieces = chunk_text(
                    block,
                    chunk_size=settings.CHUNK_SIZE,
                    overlap=settings.CHUNK_OVERLAP,
                    prefer_code=True,
                )
                for j, ch in enumerate(pieces):
                    chunks.append(
                        {
                            "id": f"{out_slug}-a{idx}-c{j}",
                            "text": ch,
                            "page": None,
                            "section": f"alarm_block_{idx}",
                            **base_meta,
                        }
                    )
        else:
            body = extract_text_file(src)
            write_markdown(md_path, base_meta, body)
            pieces = chunk_text(
                body,
                chunk_size=settings.CHUNK_SIZE,
                overlap=settings.CHUNK_OVERLAP,
            )
            for idx, ch in enumerate(pieces):
                chunks.append(
                    {
                        "id": f"{out_slug}-c{idx}",
                        "text": ch,
                        "page": None,
                        "section": "json",
                        **base_meta,
                    }
                )
    elif suffix in TEXT_SUFFIXES - {".pdf", ".json", ".html", ".htm"}:
        body = extract_text_file(src)
        if not body:
            print(f"[WARN] empty text: {rel}")
            return []
        fence = suffix[1:] if suffix != ".md" else ""
        md_body = f"```{fence}\n{body}\n```" if fence and suffix != ".md" else body
        write_markdown(md_path, base_meta, md_body)
        pieces = chunk_text(
            body,
            chunk_size=settings.CHUNK_SIZE,
            overlap=settings.CHUNK_OVERLAP,
            prefer_code=prefer_code or suffix in {".py", ".lua", ".cs", ".cpp", ".h", ".srv", ".msg"},
        )
        for idx, ch in enumerate(pieces):
            chunks.append(
                {
                    "id": f"{out_slug}-c{idx}",
                    "text": ch,
                    "page": None,
                    "section": "body",
                    **base_meta,
                }
            )
    elif suffix in {".html", ".htm"}:
        # FAQ: aggressive scrub; other HTML: still scrub nav/footer
        body = extract_html(src, scrub=True)
        if not body or len(body) < 40:
            print(f"[WARN] empty/short html after scrub: {rel}")
            return []
        write_markdown(md_path, base_meta, body)
        # FAQ answers are short — prefer fewer, denser chunks
        csize = min(settings.CHUNK_SIZE, 700) if base_meta.get("doc_type") == "faq" else settings.CHUNK_SIZE
        pieces = chunk_text(
            body,
            chunk_size=csize,
            overlap=min(settings.CHUNK_OVERLAP, 80),
        )
        for idx, ch in enumerate(pieces):
            chunks.append(
                {
                    "id": f"{out_slug}-c{idx}",
                    "text": ch,
                    "page": None,
                    "section": base_meta.get("doc_type") or "html",
                    **base_meta,
                }
            )
    else:
        print(f"[WARN] unsupported type: {src}")
        return []

    return chunks


def expand_brace_glob(pattern: str) -> list[str]:
    """Expand a single {a,b} brace group in a glob pattern."""
    m = re.search(r"\{([^}]+)\}", pattern)
    if not m:
        return [pattern]
    options = m.group(1).split(",")
    return [pattern[: m.start()] + opt.strip() + pattern[m.end() :] for opt in options]


def collect_glob_sources(seen_paths: set[str]) -> list[dict]:
    sources: list[dict] = []
    for spec in settings.GLOB_SOURCES:
        patterns = expand_brace_glob(spec["glob"])
        for pattern in patterns:
            for path in sorted(settings.CORPUS_RAW.glob(pattern)):
                if not path.is_file():
                    continue
                rel = str(path.relative_to(settings.CORPUS_RAW)).replace("\\", "/")
                if rel in seen_paths or should_skip_path(rel):
                    continue
                if path.suffix.lower() not in TEXT_SUFFIXES:
                    continue
                title = f"{spec.get('doc_type', 'doc')}: {path.stem}"
                if "CppDemo" in rel:
                    title = f"C++ SDK: {path.name}"
                elif "com.dobot.api" in rel:
                    title = f"C# SDK: {path.name}"
                elif rel.endswith(".srv"):
                    title = f"ROS service: {path.stem}"
                elif rel.endswith(".msg"):
                    title = f"ROS message: {path.stem}"
                elif rel.endswith(".lua"):
                    parent = path.parent.name
                    title = f"Training Lua: {parent}/{path.name}"
                elif "training-system" in rel and path.suffix.lower() == ".pdf":
                    title = f"Training System: {path.stem}"

                meta = {
                    "path": rel,
                    "doc_title": title,
                    "doc_type": spec.get("doc_type", "document"),
                    "doc_version": spec.get("doc_version", "unknown"),
                    "publish_date": spec.get("publish_date", "unknown"),
                    "language": spec.get("language", "en"),
                    "robot_model": spec.get("robot_model", "mg400"),
                    "axis_family": spec.get("axis_family", "4-axis"),
                    "applicability": spec.get("applicability", "direct_mg400"),
                    "priority": spec.get("priority", "medium"),
                    "safety_level": spec.get("safety_level", "normal"),
                    "source_type": spec.get("source_type", "official"),
                    "code_related": bool(spec.get("code_related", False)),
                }
                sources.append(meta)
                seen_paths.add(rel)
    return sources


def collect_faq_sources(seen_paths: set[str]) -> list[dict]:
    faq_dir = settings.CORPUS_RAW / "04_faq_pages"
    if not faq_dir.exists():
        return []
    sources = []
    for path in sorted(faq_dir.glob("*.html")):
        rel = str(path.relative_to(settings.CORPUS_RAW)).replace("\\", "/")
        if rel in seen_paths:
            continue
        title = path.stem.replace("official_mg400_faq_", "").replace("_current_en", "")
        title = title.replace("-", " ").replace("_", " ").title()
        sources.append(
            {
                "path": rel,
                "doc_title": f"MG400 FAQ: {title}",
                **settings.FAQ_META,
            }
        )
        seen_paths.add(rel)
    return sources


def collect_case_sources(seen_paths: set[str]) -> list[dict]:
    case_dir = settings.CORPUS_RAW / "05_case_application_pages"
    if not case_dir.exists():
        return []
    sources = []
    for path in sorted(case_dir.glob("*.html")):
        rel = str(path.relative_to(settings.CORPUS_RAW)).replace("\\", "/")
        if rel in seen_paths:
            continue
        title = path.stem.replace("official_", "").replace("_current_en", "")
        title = title.replace("-", " ").replace("_", " ").title()
        sources.append(
            {
                "path": rel,
                "doc_title": f"Case/Web: {title}",
                **settings.CASE_META,
            }
        )
        seen_paths.add(rel)
    return sources


def collect_all_sources(
    *,
    mode: str = "tight",
    with_faq: bool = True,
    with_cases: bool = False,
    with_globs: bool = False,
    with_curated: bool = True,
    with_alarms: bool = False,
) -> list[dict]:
    """
    mode:
      - tight (default): high-signal only, scrubbed FAQ, demos, no cases/alarms/multi-SDK
      - full: previous broad corpus
      - core-only: CORE + curated + FAQ (no demos/globs)
    """
    sources: list[dict] = []
    seen: set[str] = set()

    for meta in settings.CORE_SOURCES:
        p = meta["path"]
        if p not in seen:
            sources.append(dict(meta))
            seen.add(p)

    if with_curated:
        for meta in settings.CURATED_SOURCES:
            p = meta["path"]
            if p not in seen:
                sources.append(dict(meta))
                seen.add(p)

    if with_faq:
        sources.extend(collect_faq_sources(seen))

    if mode == "core-only":
        # strip demos from core list? Keep CORE as-is including demos in CORE_SOURCES
        pass
    elif mode == "full":
        if with_cases:
            sources.extend(collect_case_sources(seen))
        if with_globs:
            sources.extend(collect_glob_sources(seen))
    else:
        # tight: add only chapter2 palletizing + lua; no cases; no multi-SDK globs
        sources.extend(collect_tight_extra_sources(seen))

    # Apply filters
    filtered: list[dict] = []
    for meta in sources:
        path = str(meta.get("path") or "").replace("\\", "/")
        doc_type = str(meta.get("doc_type") or "")

        # Broken / empty PDFs always skip
        if "parameter-document_2022-07-28" in path:
            continue
        if "official_mg400_demo_palletizing-guide_2023-06-16_en.pdf" in path:
            continue

        if doc_type == "error_code" and not with_alarms:
            continue

        if mode == "tight":
            # Allow alarms only when explicitly requested
            if is_excluded_tight(meta):
                if doc_type == "error_code" and with_alarms:
                    pass
                else:
                    continue

        filtered.append(meta)

    return filtered


def main() -> int:
    parser = argparse.ArgumentParser(description="Preprocess Dobot MG400 corpus (tight by default)")
    parser.add_argument(
        "--tight",
        action="store_true",
        help="High-signal corpus only (default if no mode flag)",
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Full corpus: cases, C++/C#/ROS, training chapters (noiser)",
    )
    parser.add_argument(
        "--core-only",
        action="store_true",
        help="CORE_SOURCES + curated + FAQ only",
    )
    parser.add_argument("--with-faq", action="store_true", default=True, help="Include FAQ HTML")
    parser.add_argument("--no-faq", action="store_true", help="Skip FAQ")
    parser.add_argument("--with-alarms", action="store_true", help="Include alarm JSON catalogs")
    parser.add_argument("--with-cases", action="store_true", help="Include case HTML (full mode)")
    parser.add_argument("--no-cases", action="store_true", help="Skip case HTML")
    parser.add_argument("--no-globs", action="store_true", help="Skip glob expansions")
    parser.add_argument("--no-curated", action="store_true", help="Skip curated markdown")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of sources (debug)")
    parser.add_argument("--dry-run", action="store_true", help="List sources only")
    args = parser.parse_args()

    if args.full:
        mode = "full"
    elif args.core_only:
        mode = "core-only"
    else:
        mode = "tight"  # default — denser, less noise

    settings.PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    (settings.PROCESSED_DIR / "markdown").mkdir(parents=True, exist_ok=True)

    with_cases = False
    with_globs = False
    if mode == "full":
        with_cases = args.with_cases or not args.no_cases
        with_globs = not args.no_globs

    sources = collect_all_sources(
        mode=mode,
        with_faq=args.with_faq and not args.no_faq,
        with_cases=with_cases,
        with_globs=with_globs,
        with_curated=not args.no_curated,
        with_alarms=args.with_alarms,
    )
    if args.limit:
        sources = sources[: args.limit]

    print(f"Mode: {mode}")
    print(f"Sources to process: {len(sources)}")
    if args.dry_run:
        for s in sources:
            print(f"  [{s.get('doc_type')}] {s.get('doc_title')} <- {s.get('path')}")
        return 0

    all_chunks: list[dict] = []
    manifest: list[dict] = []

    for meta in tqdm(sources, desc="preprocess"):
        chunks = process_source(meta)
        all_chunks.extend(chunks)
        manifest.append(
            {
                "path": meta.get("path"),
                "doc_title": meta.get("doc_title"),
                "doc_type": meta.get("doc_type"),
                "chunk_count": len(chunks),
                "ok": len(chunks) > 0,
            }
        )

    with settings.CHUNKS_PATH.open("w", encoding="utf-8") as f:
        for ch in all_chunks:
            # drop non-serializable if any
            row = {k: v for k, v in ch.items()}
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    with settings.MANIFEST_PATH.open("w", encoding="utf-8") as f:
        for row in manifest:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    ok = sum(1 for m in manifest if m["ok"])
    empty = [m for m in manifest if not m["ok"]]
    by_type: dict[str, int] = {}
    for ch in all_chunks:
        t = ch.get("doc_type") or "?"
        by_type[t] = by_type.get(t, 0) + 1

    print(f"Done. mode={mode} sources_ok={ok}/{len(manifest)} chunks={len(all_chunks)}")
    print(f"Chunks by type: {by_type}")
    print(f"Chunks: {settings.CHUNKS_PATH}")
    print(f"Markdown: {settings.PROCESSED_DIR / 'markdown'}")
    # Write mode stamp for docs/eval
    stamp = {
        "mode": mode,
        "sources_ok": ok,
        "sources_total": len(manifest),
        "chunks": len(all_chunks),
        "by_type": by_type,
    }
    stamp_path = settings.PROCESSED_DIR / "ingest_mode.json"
    stamp_path.write_text(json.dumps(stamp, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Mode stamp: {stamp_path}")
    if empty:
        print(f"Empty/failed sources ({len(empty)}):")
        for m in empty[:20]:
            print(f"  - {m['doc_title']}: {m['path']}")
        if len(empty) > 20:
            print(f"  ... and {len(empty) - 20} more")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
