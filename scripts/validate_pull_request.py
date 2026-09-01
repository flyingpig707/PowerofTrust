#!/usr/bin/env python3
"""Validate the changed-file boundary for contributor or maintainer editorial PRs."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def changed_files(base_ref: str) -> list[str]:
    completed = subprocess.run(
        ["git", "diff", "--name-only", f"{base_ref}...HEAD"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    return [line for line in completed.stdout.splitlines() if line]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-ref", required=True)
    parser.add_argument("--mode", choices=("contributor", "editorial"), default="contributor")
    parser.add_argument("--pr-author", help="Authenticated GitHub login for contributor-boundary checks")
    args = parser.parse_args()
    changed = changed_files(args.base_ref)
    if not changed:
        print("FAIL: no changed files found")
        return 1

    errors: list[str] = []
    if args.mode == "contributor":
        forbidden = [path for path in changed if not path.startswith("contributions/")]
        if forbidden:
            errors.append("contributor PRs may change only contributions/<github-login>/<proposal-slug>/")
            errors.extend(f"  forbidden: {path}" for path in forbidden)
        if any(path.startswith("book/") for path in changed):
            errors.append("canonical book files require a separate maintainer-controlled editorial PR")
        if args.pr_author:
            for path in changed:
                parts = Path(path).parts
                if len(parts) < 4 or parts[0] != "contributions":
                    continue
                if parts[1].lower() != args.pr_author.lower():
                    errors.append(
                        f"contributor path owner {parts[1]!r} must match authenticated PR author {args.pr_author!r}"
                    )
    else:
        allowed_prefixes = ("book/", "media/")
        allowed_files = {"CONTRIBUTORS.md", "CHANGELOG.md"}
        forbidden = [path for path in changed if not path.startswith(allowed_prefixes) and path not in allowed_files]
        if forbidden:
            errors.append("editorial PRs may change only book/, media/, CONTRIBUTORS.md, and CHANGELOG.md")
            errors.extend(f"  forbidden: {path}" for path in forbidden)
        if any(path.startswith("book/") for path in changed) and "CONTRIBUTORS.md" not in changed:
            errors.append("an editorial PR changing book/ must also update CONTRIBUTORS.md")

    if errors:
        print("FAIL")
        print("\n".join(errors))
        return 1
    print(f"PASS: {args.mode} change boundary ({len(changed)} files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
