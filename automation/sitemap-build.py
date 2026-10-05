#!/usr/bin/env python3
"""
Rebuild sitemap.xml for the compliancebridge static site.

- Existing 28 commercial/service URLs keep their existing priority + changefreq,
  but get a refreshed <lastmod>.
- Article URLs under /insights/ are appended, ordered by datePublished
  (newest first), with lastmod set to dateModified.

Only articles that carry real body content are eligible. Run with --all to
include placeholder/stub articles too (not recommended: submitting thin
template pages to the index hurts crawl budget and quality signals).
"""
import argparse
import datetime
import glob
import os
import pathlib
import re
import sys
import xml.etree.ElementTree as ET

SITE = "https://compliancebridgeadvisory.com"
TODAY = datetime.date.today().isoformat()

# Minimum word count in <body> for an article to count as real content.
MIN_WORDS = 800


def strip_tags(html: str) -> str:
    body = re.search(r"<body.*?>(.*)</body>", html, re.S)
    chunk = body.group(1) if body else html
    chunk = re.sub(r"<(script|style|nav|footer|header)[^>]*>.*?</\1>", " ", chunk, flags=re.S)
    return re.sub(r"<[^>]+>", " ", chunk)


def word_count(html: str) -> int:
    return len([w for w in strip_tags(html).split() if w.strip()])


def extract_date(html: str, key: str):
    m = re.search(rf'"{key}"\s*:\s*"(\d{{4}}-\d{{2}}-\d{{2}})"', html)
    if m:
        return m.group(1)
    m = re.search(rf'<meta property="article:{key.lower().replace("published", "published")}', html)
    return None


def extract_date_meta(html: str, prop: str):
    m = re.search(rf'<meta property="article:{prop}" content="(\d{{4}}-\d{{2}}-\d{{2}})"', html)
    return m.group(1) if m else None


def read_existing(path: pathlib.Path):
    """Return [(loc, lastmod, changefreq, priority)] preserving file order."""
    if not path.exists():
        return []
    root = ET.parse(path).getroot()
    ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    out = []
    for url in root.findall(f"{ns}url"):
        loc = url.findtext(f"{ns}loc") or ""
        loc = loc.replace(SITE, "").lstrip("/") or ""
        out.append(
            (
                loc,
                url.findtext(f"{ns}lastmod"),
                url.findtext(f"{ns}changefreq") or "monthly",
                url.findtext(f"{ns}priority") or "0.5",
            )
        )
    return out


def collect_articles(root: pathlib.Path, include_stubs: bool):
    articles = []
    for path in sorted(glob.glob(str(root / "insights" / "*.html"))):
        html = pathlib.Path(path).read_text(encoding="utf-8")
        name = os.path.basename(path)
        words = word_count(html)

        pub = extract_date_meta(html, "published_time") or extract_date(html, "datePublished")
        mod = extract_date_meta(html, "modified_time") or extract_date(html, "dateModified")
        mod = mod or pub or TODAY

        if words < MIN_WORDS and not include_stubs:
            articles.append((name, words, "SKIPPED (stub)", pub, mod))
            continue
        articles.append((name, words, "added", pub, mod))
    return articles


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true", help="include stub/placeholder articles")
    ap.add_argument("--dry-run", action="store_true", help="print report, write nothing")
    args = ap.parse_args()

    root = pathlib.Path(__file__).resolve().parent.parent
    sitemap = root / "sitemap.xml"

    existing = read_existing(sitemap)
    existing_locs = {loc for loc, *_ in existing}
    articles = collect_articles(root, args.all)

    included, skipped = [], []
    for name, words, status, pub, mod in articles:
        (included if status == "added" else skipped).append((name, words, status, pub, mod))

    included.sort(key=lambda a: (a[3] or "0000-00-00"), reverse=True)

    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']

    for loc, _old, changefreq, priority in existing:
        url = f"{SITE}/{loc}" if loc else f"{SITE}/"
        lines += [
            "  <url>",
            f"    <loc>{url}</loc>",
            f"    <lastmod>{TODAY}</lastmod>",
            f"    <changefreq>{changefreq}</changefreq>",
            f"    <priority>{priority}</priority>",
            "  </url>",
        ]

    for name, _words, _status, pub, mod in included:
        lines += [
            "  <url>",
            f"    <loc>{SITE}/insights/{name}</loc>",
            f"    <lastmod>{mod}</lastmod>",
            "    <changefreq>monthly</changefreq>",
            "    <priority>0.7</priority>",
            "  </url>",
        ]

    lines.append("</urlset>")
    out = "\n".join(lines) + "\n"

    print(f"service/core URLs kept : {len(existing)}")
    print(f"article URLs added     : {len(included)}")
    print(f"articles skipped (stub): {len(skipped)}")
    for name, words, _s, pub, _m in skipped:
        print(f"    - {name} ({words} words, published {pub})")
    print(f"total URLs             : {len(existing) + len(included)}")

    if args.dry_run:
        print("\n[dry-run] nothing written")
        return 0

    sitemap.write_text(out, encoding="utf-8")

    # Validate
    ET.parse(sitemap)
    print(f"\nwrote {sitemap} — XML parses clean")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
