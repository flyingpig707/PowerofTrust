# Submission contract

Read this before generating, validating, or reviewing a package.

## Directory contract

Each contributor owns one new directory per proposal:

```text
contributions/<github-login>/<proposal-slug>/
├── contribution.md
├── metadata.json
├── sources.md
└── self_check.json
```

`<github-login>` and `<proposal-slug>` use letters, digits, and hyphens only. A Pull Request from a contributor may add one or more directories under their own login, but must not change `book/` or project governance files.

## Required content

`metadata.json` is the machine-readable record. It must include:

- format version, proposal title, contribution type, affected chapter, and status;
- human GitHub login and Agent name;
- short summary and change rationale;
- at least one claim classified as `fact`, `inference`, or `author-view`;
- source records for factual claims, or an explicit explanation when no external source is relevant;
- originality and project-use authorization accepted by the human contributor;
- an acknowledgement that submission does not guarantee adoption.

`contribution.md` is the editorial proposal. It explains the problem, current passage or insertion point, proposed material, evidence and reasoning, framework fit, reader value, limitations, and requested editorial decision.

`sources.md` gives human-readable source notes and links. It must not reproduce large copyrighted passages.

`self_check.json` records local validation and human confirmations. Before validation, the human must set `privacy_and_secrets_checked`, `copyright_checked`, and `human_authorization_confirmed` to `true`. The validator updates only deterministic results; it never declares truth or editorial acceptance.

## Pull Request contract

The contributor PR is an intake proposal. Its allowed changes are confined to `contributions/<same-login>/...`. Maintainers may request fixes in that PR. If an idea is selected, a maintainer opens a separate editorial PR that changes `book/`, updates `CONTRIBUTORS.md`, and links back to the original proposal.

Automated checks verify structure and obvious policy violations only. Human review decides evidence quality, originality, coherence, usefulness, safety, and publication suitability.
