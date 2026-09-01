---
name: power-of-trust-coauthor
description: Participate in the collaborative writing of the Chinese book 《信任力》 by preparing a reviewable contribution package, checking evidence and rights, validating it locally, and opening a scoped GitHub Pull Request. Use for corrections, evidence, cases, tools, rewrites, or new-section proposals; do not edit the canonical book directly.
---

# 《信任力》共同写作

Help a human contributor turn one useful idea into a traceable proposal for the book. A passing package enters the public proposal library; only the authors or maintainers decide whether to adapt it into `book/` through a separate editorial Pull Request.

## Start safely

1. Read `README.md`, `CONTRIBUTING.md`, `CONTRIBUTOR-TERMS.md`, `GOVERNANCE.md`, and the relevant file under `book/`.
2. Inspect open Issues and Pull Requests when GitHub access is available. Avoid duplicating an existing proposal.
3. Preserve current work before forking or changing branches. Never overwrite uncommitted user files.
4. Ask the human contributor for their GitHub login, contribution type, affected chapter, and concrete idea if any is missing.
5. Do not submit secrets, personal data, private correspondence, unlicensed excerpts, fabricated evidence, or confidential company information.

## Choose one contribution type

Use exactly one of these values:

- `correction`: typo, broken link, formatting, or unambiguous factual correction;
- `evidence`: a source that supports, limits, updates, or challenges an existing claim;
- `case`: a verifiable practice case with scope and limitations;
- `tool`: an improvement to a checklist, worksheet, measurement method, or exercise;
- `rewrite`: a clearer alternative to an existing passage;
- `new-section`: a proposal for a new subsection or chapter.

Read [references/editorial-framework.md](references/editorial-framework.md) before developing the idea. Read [references/submission-contract.md](references/submission-contract.md) before generating files or preparing a Pull Request.

## Create the proposal package

Fork `flyingpig707/PowerofTrust`, create a branch, and work only under:

```text
contributions/<github-login>/<proposal-slug>/
```

From the repository root, run:

```bash
python3 scripts/scaffold_contribution.py \
  --github-login <github-login> \
  --slug <proposal-slug> \
  --type <contribution-type> \
  --chapter <chapter-id> \
  --agent-name "<agent name>"
```

Replace every placeholder in the generated package. Keep the proposed wording in `contribution.md`; do not directly modify `book/`, `media/`, repository governance, workflows, or other contributors' packages.

## Evidence and writing rules

- Mark material claims as `fact`, `inference`, or `author-view` in `metadata.json` and explain the classification in the proposal.
- Give facts a source URL, publisher, title, publication or retrieval date, relevance, and limitations. Prefer current primary sources.
- A source supports only what it actually establishes. Do not turn correlation, marketing claims, model behavior observations, or a single case into a universal conclusion.
- For rewrites, quote only the minimum locator text needed to identify the passage; put the full proposed replacement in your own words.
- Explain how the proposal relates to the book's chain: expression, transmission, fact, experience, commitment; and to the matching trust layer: data, source, logic, experience, fulfillment.
- State uncertainty, counterexamples, and conditions where the proposal should not be used.

## Rights and human authorization

Before marking a package ready, show the human contributor `CONTRIBUTOR-TERMS.md`. They must deliberately set both authorization fields in `metadata.json` to `true` and provide their GitHub login. An Agent must not accept the terms for a person, invent a signature, or assume authorization from silence.

They must also review the finished files and deliberately set `privacy_and_secrets_checked`, `copyright_checked`, and `human_authorization_confirmed` in `self_check.json` to `true`. These are human judgments; the validator will not set them.

The repository has no book-wide open-source license. Contribution permission allows the project to review, edit, merge, display, and publish the submitted material; it does not guarantee acceptance or relicense the whole book.

## Validate and prepare the Pull Request

Run:

```bash
python3 scripts/validate_contributions.py \
  contributions/<github-login>/<proposal-slug> \
  --write-self-check
python3 scripts/validate_pull_request.py \
  --base-ref origin/main \
  --pr-author <github-login>
```

Repair all errors. Warnings require human judgment but do not automatically reject a package.

Open a Pull Request that changes only the new proposal directory. Use `.github/pull_request_template.md`, disclose the human contributor and Agent, link related Issues, and paste the validator results. Do not claim that a passing validator means the content is true, endorsed, accepted, or part of the canonical book.

If `gh` is available and the human has authorized publication, it may be used to fork, push, and open the Pull Request. Otherwise, leave a clean branch and provide the exact GitHub steps for the human. Stop before any external submission or message if authorization is absent.

## What happens next

Maintainers review originality, evidence quality, framework fit, readability, risk, and publication rights. Accepted ideas are incorporated through a separate maintainer-controlled editorial Pull Request. Preserve contributor and Agent credit in `CONTRIBUTORS.md`; distinguish `proposed`, `under-review`, `selected`, and `incorporated` states.
