#!/usr/bin/env python3
"""Deterministically validate one or more 《信任力》 contribution packages."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = ("contribution.md", "metadata.json", "sources.md", "self_check.json")
ALLOWED_TYPES = {"correction", "evidence", "case", "tool", "rewrite", "new-section"}
ALLOWED_CLASSIFICATIONS = {"fact", "inference", "author-view"}
SAFE_NAME = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,62}[A-Za-z0-9])?$")
PLACEHOLDER = re.compile(r"REPLACE|YYYY-MM-DD|\{\{[^}]+\}\}")
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"(?i)(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{12,}"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
)
REQUIRED_HEADINGS = (
    "## 1. 要解决的问题",
    "## 2. 影响位置",
    "## 3. 建议内容",
    "## 4. 证据与推理",
    "## 5. 与全书框架的关系",
    "## 6. 给读者带来的价值",
    "## 7. 边界、反例与风险",
    "## 8. 请求编辑判断",
)


class Result:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def is_web_url(value: object) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def is_iso_date(value: object) -> bool:
    if not isinstance(value, str):
        return False
    try:
        date.fromisoformat(value)
        return True
    except ValueError:
        return False


def non_placeholder(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip()) and not PLACEHOLDER.search(value)


def package_parts(path: Path, result: Result) -> tuple[str, str] | None:
    try:
        relative = path.resolve().relative_to((ROOT / "contributions").resolve())
    except ValueError:
        result.error(f"package must be inside contributions/: {path}")
        return None
    if len(relative.parts) != 2:
        result.error("package path must be contributions/<github-login>/<proposal-slug>/")
        return None
    login, slug = relative.parts
    if not SAFE_NAME.fullmatch(login) or not SAFE_NAME.fullmatch(slug):
        result.error("github login and proposal slug may contain only letters, digits, and hyphens")
    return login, slug


def load_json(path: Path, result: Result) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        result.error(f"cannot parse {path.name}: {exc}")
        return {}
    if not isinstance(value, dict):
        result.error(f"{path.name} must contain a JSON object")
        return {}
    return value


def scan_text(path: Path, text: str, result: Result) -> None:
    if PLACEHOLDER.search(text):
        result.error(f"{path.name} still contains template placeholders")
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            result.error(f"{path.name} appears to contain a secret or private key")


def validate_package(path: Path, write_self_check: bool = False) -> Result:
    result = Result()
    parts = package_parts(path, result)
    for name in REQUIRED_FILES:
        if not (path / name).is_file():
            result.error(f"missing required file: {name}")
    if result.errors:
        return result

    texts = {name: (path / name).read_text(encoding="utf-8") for name in REQUIRED_FILES}
    for name, text in texts.items():
        scan_text(path / name, text, result)

    contribution = texts["contribution.md"]
    for heading in REQUIRED_HEADINGS:
        if heading not in contribution:
            result.error(f"contribution.md is missing heading: {heading}")
    if len(contribution.strip()) < 800:
        result.warn("contribution.md is very short; confirm the proposal is editorially reviewable")

    metadata = load_json(path / "metadata.json", result)
    self_check = load_json(path / "self_check.json", result)
    if parts:
        login, slug = parts
        if metadata.get("slug") != slug:
            result.error("metadata slug must match the package directory")
        human = metadata.get("human_contributor")
        if not isinstance(human, dict):
            result.error("human_contributor must be an object")
            human = {}
        if human.get("github_login") != login:
            result.error("human_contributor.github_login must match the contributor directory")
        if human.get("accepted_originality_statement") is not True:
            result.error("the human contributor must explicitly accept the originality statement")
        if human.get("accepted_project_use_authorization") is not True:
            result.error("the human contributor must explicitly accept project-use authorization")

    for key in ("format_version", "title", "affected_chapter", "summary", "change_rationale"):
        if not non_placeholder(metadata.get(key)):
            result.error(f"metadata field {key!r} is missing or contains a placeholder")
    if metadata.get("contribution_type") not in ALLOWED_TYPES:
        result.error(f"contribution_type must be one of: {', '.join(sorted(ALLOWED_TYPES))}")
    if metadata.get("status") != "proposed":
        result.error("new contribution status must be proposed")
    if metadata.get("submission_does_not_guarantee_adoption") is not True:
        result.error("submission_does_not_guarantee_adoption must be true")
    agent = metadata.get("agent")
    if not isinstance(agent, dict) or not non_placeholder(agent.get("name")):
        result.error("agent.name is required")

    sources = metadata.get("sources")
    if not isinstance(sources, list):
        result.error("sources must be a list")
        sources = []
    source_ids: set[str] = set()
    for index, source in enumerate(sources):
        if not isinstance(source, dict):
            result.error(f"sources[{index}] must be an object")
            continue
        source_id = source.get("id")
        if not non_placeholder(source_id):
            result.error(f"sources[{index}].id is required")
        elif source_id in source_ids:
            result.error(f"duplicate source id: {source_id}")
        else:
            source_ids.add(source_id)
        for key in ("publisher", "title", "supports", "limitations"):
            if not non_placeholder(source.get(key)):
                result.error(f"sources[{index}].{key} is missing or contains a placeholder")
        if not is_web_url(source.get("url")):
            result.error(f"sources[{index}].url must be an http(s) URL")
        if not is_iso_date(source.get("published_or_retrieved")):
            result.error(f"sources[{index}].published_or_retrieved must be YYYY-MM-DD")

    claims = metadata.get("claims")
    if not isinstance(claims, list) or not claims:
        result.error("claims must contain at least one classified claim")
        claims = []
    claim_ids: set[str] = set()
    for index, claim in enumerate(claims):
        if not isinstance(claim, dict):
            result.error(f"claims[{index}] must be an object")
            continue
        claim_id = claim.get("id")
        if not non_placeholder(claim_id):
            result.error(f"claims[{index}].id is required")
        elif claim_id in claim_ids:
            result.error(f"duplicate claim id: {claim_id}")
        else:
            claim_ids.add(claim_id)
        if claim.get("classification") not in ALLOWED_CLASSIFICATIONS:
            result.error(f"claims[{index}].classification must be fact, inference, or author-view")
        if not non_placeholder(claim.get("text")):
            result.error(f"claims[{index}].text is required")
        linked = claim.get("source_ids", [])
        if not isinstance(linked, list):
            result.error(f"claims[{index}].source_ids must be a list")
            linked = []
        unknown = set(linked) - source_ids
        if unknown:
            result.error(f"claims[{index}] refers to unknown source ids: {', '.join(sorted(unknown))}")
        if claim.get("classification") == "fact" and not linked:
            result.error(f"fact claim {claim_id or index} must cite at least one source")

    if "http://" not in texts["sources.md"] and "https://" not in texts["sources.md"]:
        result.warn("sources.md contains no web URL; explain why if external evidence is not relevant")

    human_checks = ("privacy_and_secrets_checked", "copyright_checked", "human_authorization_confirmed")
    for key in human_checks:
        if self_check.get(key) is not True:
            result.error(f"self_check.{key} must be explicitly confirmed by the human contributor")

    if write_self_check:
        deterministic_pass = not result.errors
        self_check.update(
            {
                "validator_version": "1.0",
                "structure_passed": deterministic_pass,
                "link_format_checked": deterministic_pass,
                "claims_classified": deterministic_pass,
                "sources_and_limits_recorded": deterministic_pass,
                "book_directory_unchanged": True,
            }
        )
        (path / "self_check.json").write_text(json.dumps(self_check, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    else:
        deterministic_checks = (
            "structure_passed",
            "link_format_checked",
            "claims_classified",
            "sources_and_limits_recorded",
            "book_directory_unchanged",
        )
        for key in deterministic_checks:
            if self_check.get(key) is not True:
                result.error(f"self_check.{key} is not true; run the validator with --write-self-check")
    return result


def find_packages(paths: list[str]) -> list[Path]:
    if paths:
        return [Path(value) if Path(value).is_absolute() else ROOT / value for value in paths]
    packages = []
    base = ROOT / "contributions"
    if base.exists():
        for login in base.iterdir():
            if login.is_dir():
                packages.extend(path for path in login.iterdir() if path.is_dir())
    return sorted(packages)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*")
    parser.add_argument("--write-self-check", action="store_true")
    args = parser.parse_args()
    packages = find_packages(args.paths)
    if not packages:
        print("No contribution packages found.")
        return 0
    failed = False
    for package in packages:
        result = validate_package(package, args.write_self_check)
        label = package.resolve().relative_to(ROOT.resolve()) if package.exists() else package
        for message in result.warnings:
            print(f"WARNING {label}: {message}")
        for message in result.errors:
            print(f"ERROR {label}: {message}")
        if result.errors:
            failed = True
            print(f"FAIL {label}")
        else:
            print(f"PASS {label}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
