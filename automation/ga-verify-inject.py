#!/usr/bin/env python3
"""
Inject Google Search Console verification meta + GA4 (gtag.js) into <head>
of every HTML page in the compliancebridge static site.

Idempotent: skips any page that already contains the verification token or
the GA4 measurement ID. Inserts immediately after the <link rel="icon"> line,
which is present and unique in all pages.
"""
import glob
import pathlib
import sys

VERIFY_TOKEN = "AwyNl3szglpaRHlRhlD8FIMH3oq2ucT3vRkXUNCNsYA"
GA4_ID = "G-0CG0Y9FTW3"

ANCHOR = '<link rel="icon"'

SNIPPET = f"""    <!-- Google Search Console verification -->
    <meta name="google-site-verification" content="{VERIFY_TOKEN}" />
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());

      gtag('config', '{GA4_ID}');
    </script>
"""


def main() -> int:
    root = pathlib.Path(__file__).resolve().parent.parent
    pages = sorted(glob.glob(str(root / "*.html"))) + sorted(
        glob.glob(str(root / "insights" / "*.html"))
    )

    changed, skipped, failed = [], [], []

    for path in pages:
        p = pathlib.Path(path)
        rel = p.relative_to(root)
        src = p.read_text(encoding="utf-8")

        if VERIFY_TOKEN in src or GA4_ID in src:
            skipped.append(str(rel))
            continue

        head_end = src.find("</head>")
        if head_end == -1:
            failed.append(f"{rel}: no </head>")
            continue

        head = src[:head_end]
        idx = head.find(ANCHOR)
        if idx == -1:
            failed.append(f"{rel}: anchor {ANCHOR!r} not found in head")
            continue

        # Insert just after the full icon line (up to and including newline).
        line_end = head.find("\n", idx)
        if line_end == -1:
            failed.append(f"{rel}: unterminated anchor line")
            continue

        cut = line_end + 1
        out = src[:cut] + SNIPPET + src[cut:]
        p.write_text(out, encoding="utf-8")
        changed.append(str(rel))

    print(f"injected: {len(changed)}")
    print(f"skipped:  {len(skipped)}")
    for f in failed:
        print(f"FAILED:   {f}", file=sys.stderr)

    if failed:
        return 1

    print("\n--- updated files ---")
    for f in changed:
        print(f"  {f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
