#!/usr/bin/env python3
"""Create a new 《信任力》 contribution package from the canonical template."""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "skills" / "power-of-trust-coauthor" / "assets" / "submission-template"
ALLOWED_TYPES = ("correction", "evidence", "case", "tool", "rewrite", "new-section")
SAFE_NAME = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,38}[A-Za-z0-9])?$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--github-login", required=True)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--type", required=True, choices=ALLOWED_TYPES)
    parser.add_argument("--chapter", required=True, help="For example: 06-GEO之战 or NEW")
    parser.add_argument("--agent-name", required=True)
    parser.add_argument("--title", default="REPLACE: contribution title")
    return parser.parse_args()


def validate_name(value: str, label: str) -> None:
    if not SAFE_NAME.fullmatch(value):
        raise SystemExit(f"ERROR: {label} must contain only letters, digits, and single hyphens; got {value!r}")


def main() -> int:
    args = parse_args()
    validate_name(args.github_login, "github login")
    validate_name(args.slug, "slug")
    destination = ROOT / "contributions" / args.github_login / args.slug
    if destination.exists():
        raise SystemExit(f"ERROR: destination already exists: {destination.relative_to(ROOT)}")
    destination.mkdir(parents=True)
    replacements = {
        "{{GITHUB_LOGIN}}": args.github_login,
        "{{SLUG}}": args.slug,
        "{{TYPE}}": args.type,
        "{{CHAPTER}}": args.chapter,
        "{{AGENT_NAME}}": args.agent_name,
        "{{TITLE}}": args.title,
    }
    for source in TEMPLATE.iterdir():
        if not source.is_file():
            continue
        target = destination / source.name
        text = source.read_text(encoding="utf-8")
        for old, new in replacements.items():
            text = text.replace(old, new)
        target.write_text(text, encoding="utf-8")
    print(f"Created {destination.relative_to(ROOT)}")
    print("Next: replace every REPLACE/YYYY placeholder, obtain the human contributor's explicit authorization, then run the validator.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

