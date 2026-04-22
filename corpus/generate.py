"""Generate a realistic corpus of team memory markdown files using Claude Sonnet.

One API call per (team, subdir) chunk. Each call returns a JSON array of
{filename, content} objects which we write to disk. Idempotent: skips any
path that already exists.

Run from repo root:
    python3 corpus/generate.py
"""

from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from runner._env import load_env_if_needed  # noqa: E402

load_env_if_needed()

import anthropic  # noqa: E402

# The experiment itself runs on opus 4-7; Sonnet is used here only for
# synthetic content scaffolding. Override via env var if needed.
import os  # noqa: E402

MODEL = os.environ.get("CORPUS_MODEL", "claude-sonnet-4-6")

MEMORY_STORE = ROOT / "memory-store"

# Canonical files we must NOT overwrite.
CANONICAL_PATHS = {
    MEMORY_STORE / "personal" / "alice" / "scratch.md",
    MEMORY_STORE / "teams" / "platform" / "AGENTS.md",
    MEMORY_STORE / "teams" / "platform" / "runbooks" / "deploy.md",
    MEMORY_STORE / "teams" / "platform" / "known-flaky-tests.md",
    MEMORY_STORE / "teams" / "ml" / "AGENTS.md",
    MEMORY_STORE / "teams" / "ml" / "evaluations" / "q1.md",
    MEMORY_STORE / "teams" / "finance" / "budget.md",
    MEMORY_STORE / "org" / "compliance" / "pii-handling.md",
}

# Forbidden substrings. These would confuse must_mention scoring for tasks 01/03.
FORBIDDEN_SUBSTRINGS = [
    "just deploy api",
    "0.85",
    "q1-2026-eval-v3",
    "test_concurrent_migration_safety",
    "4,712,300",
    "$4,712,300",
    "4712300",
]
# Triple-ish: DEPLOY_ENV + DEPLOY_REGION + DEPLOY_COMMIT_SHA in one file is banned.
FORBIDDEN_TRIPLE = ("DEPLOY_ENV", "DEPLOY_REGION", "DEPLOY_COMMIT_SHA")


# -------------------- chunk specification --------------------

# Each chunk: (relative target dir, team_slug, description of team,
#              subdir focus, count, list of example filenames for distractors)
CHUNKS: list[dict[str, Any]] = [
    # Platform — 80 new files across 5 subdirs
    {
        "dir": "teams/platform/runbooks",
        "team": "platform",
        "team_context": (
            "The Platform team owns the deploy pipeline, shared infra "
            "(Postgres, Redis, Kafka), and the internal `just` CLI. "
            "Three services: api, worker, gateway. "
            "There IS a canonical `runbooks/deploy.md` in this same directory "
            "that documents the main deploy sequence; these files must NOT "
            "duplicate or restate that canonical sequence."
        ),
        "subdir_focus": (
            "Operational runbooks for specific failure modes, edge cases, "
            "one-off procedures, legacy systems, and adjacent services. "
            "Think: kafka-lag-runbook.md, redis-failover.md, "
            "postgres-vacuum.md, emergency-deploy.md, deploy-legacy-2024.md, "
            "worker-deploy.md, rollback-gateway.md, certificate-rotation.md."
        ),
        "count": 18,
        "include_distractors": True,
        "distractor_hint": (
            "At least 5 filenames should contain the word 'deploy' (e.g. "
            "deploy-legacy-2024.md, worker-deploy.md, emergency-deploy.md, "
            "deploy-checklist-archive.md, deploy-dashboard-guide.md) but "
            "NONE of these files should contain the exact command "
            "`just deploy api` or describe the canonical 3-service sequence."
        ),
    },
    {
        "dir": "teams/platform/post-mortems",
        "team": "platform",
        "team_context": (
            "The Platform team owns the deploy pipeline, shared infra "
            "(Postgres, Redis, Kafka), and the internal `just` CLI. "
            "Three services: api, worker, gateway."
        ),
        "subdir_focus": (
            "Incident post-mortems. Dated filenames like "
            "2025-09-15-payment-outage.md, 2025-11-03-kafka-lag-spike.md, "
            "2026-01-22-gateway-cert-expiry.md. Each should have sections "
            "like Summary / Timeline / Root Cause / Impact / Action Items."
        ),
        "count": 15,
        "include_distractors": False,
    },
    {
        "dir": "teams/platform/rules",
        "team": "platform",
        "team_context": (
            "The Platform team owns the deploy pipeline and shared infra. "
            "They maintain overrides against org defaults (e.g. no-unused-vars "
            "is warn-level for Platform instead of error)."
        ),
        "subdir_focus": (
            "Rule and policy documents specific to the Platform team. "
            "Examples: code-review-rules.md, on-call-rotation.md, "
            "incident-severity.md, naming-conventions.md, branch-protection.md, "
            "secrets-handling.md."
        ),
        "count": 15,
        "include_distractors": False,
    },
    {
        "dir": "teams/platform/playbooks",
        "team": "platform",
        "team_context": (
            "The Platform team owns the deploy pipeline and shared infra."
        ),
        "subdir_focus": (
            "Playbooks for recurring projects / programs, as opposed to "
            "incident runbooks. Examples: quarterly-capacity-planning.md, "
            "new-service-onboarding.md, dependency-upgrade-playbook.md, "
            "vendor-evaluation.md, chaos-drill.md, terraform-module-review.md."
        ),
        "count": 15,
        "include_distractors": False,
    },
    {
        "dir": "teams/platform/deprecations",
        "team": "platform",
        "team_context": (
            "The Platform team owns the deploy pipeline and shared infra."
        ),
        "subdir_focus": (
            "Notes tracking deprecated systems, libraries, endpoints, and "
            "migration guides away from them. Examples: "
            "python-311-migration.md, kafka-0.10-sunset.md, "
            "legacy-auth-shim-removal.md, deprecated-endpoints-2025.md, "
            "old-dashboard-retirement.md, mysql-to-postgres-migration.md."
        ),
        "count": 15,
        "include_distractors": False,
    },
    # ML — 55 new files
    {
        "dir": "teams/ml/evaluations",
        "team": "ml",
        "team_context": (
            "The ML team owns the recommender model, eval harness, and "
            "offline training pipeline. There is a canonical file in this "
            "SAME directory called `q1.md` which defines the Q1 2026 eval "
            "thresholds (precision, recall, latency) for the recommender. "
            "New files in this directory must NOT duplicate or restate those "
            "thresholds."
        ),
        "subdir_focus": (
            "Historical and adjacent eval documents. Examples: "
            "q4-2025-recap.md, q2-2025.md, holdout-set-methodology.md, "
            "offline-vs-online-delta.md, eval-set-rotation.md, "
            "judge-prompt-v2.md, eval-harness-readme.md, "
            "recall-at-k-notes.md, regression-tracking.md. Avoid being the "
            "current (q1 2026) canonical thresholds doc."
        ),
        "count": 12,
        "include_distractors": True,
        "distractor_hint": (
            "Several filenames should reference 'q1' or 'eval' but the "
            "contents must NOT state the current Q1 2026 precision threshold "
            "of 0.85. Use different thresholds or discuss methodology instead."
        ),
    },
    {
        "dir": "teams/ml/training",
        "team": "ml",
        "team_context": (
            "The ML team owns the recommender model and training pipeline. "
            "They pin numpy<2.0 because the training image hasn't migrated."
        ),
        "subdir_focus": (
            "Training pipeline documentation, feature store notes, data "
            "cleaning procedures, GPU cluster runbooks. Examples: "
            "feature-store-schema.md, gpu-cluster-access.md, "
            "data-cleaning-pipeline.md, training-image-build.md, "
            "hyperparameter-sweep-guide.md, training-failure-modes.md."
        ),
        "count": 15,
        "include_distractors": False,
    },
    {
        "dir": "teams/ml/experiments",
        "team": "ml",
        "team_context": (
            "The ML team runs experiments on the recommender model."
        ),
        "subdir_focus": (
            "Dated experiment logs: what was tried, what happened. Examples: "
            "2025-10-dual-encoder-trial.md, 2025-12-query-rewriting.md, "
            "2026-02-reranker-ablation.md, embedding-dim-sweep.md, "
            "cold-start-experiment.md. Each should look like an engineer's "
            "notes: hypothesis, setup, results, next steps."
        ),
        "count": 15,
        "include_distractors": False,
    },
    {
        "dir": "teams/ml/inference",
        "team": "ml",
        "team_context": (
            "The ML team also maintains model serving / inference infra, "
            "though user-facing traffic is served by Platform's api service."
        ),
        "subdir_focus": (
            "Inference serving topics: model export, quantization, "
            "batch vs online, latency debugging. Examples: "
            "onnx-export-notes.md, quantization-tradeoffs.md, "
            "triton-serving-setup.md, batch-inference-nightly.md, "
            "latency-debugging-cheatsheet.md."
        ),
        "count": 13,
        "include_distractors": False,
    },
    # Finance — 40 new files
    {
        "dir": "teams/finance/contracts",
        "team": "finance",
        "team_context": (
            "Finance team — confidential. Handles vendor contracts, budgets, "
            "procurement. There is a canonical `budget.md` in the parent "
            "directory (teams/finance/) with Q1 2026 headcount spend numbers; "
            "do NOT restate or leak those specific figures."
        ),
        "subdir_focus": (
            "Contract summaries, redlines, renewal notes. Examples: "
            "aws-enterprise-agreement-2026.md, datadog-contract-renewal.md, "
            "snowflake-paper-signed-2025-08.md, office-lease-renewal-sf.md, "
            "outside-counsel-panel-agreement.md."
        ),
        "count": 15,
        "include_distractors": False,
    },
    {
        "dir": "teams/finance/vendors",
        "team": "finance",
        "team_context": (
            "Finance team — confidential."
        ),
        "subdir_focus": (
            "Vendor profiles / scorecards. One file per vendor or vendor "
            "category. Examples: aws-spend-profile.md, datadog-scorecard.md, "
            "slack-vendor-review.md, snowflake-profile.md, "
            "github-enterprise-spend.md, okta-vendor-summary.md."
        ),
        "count": 15,
        "include_distractors": False,
    },
    {
        "dir": "teams/finance/policies",
        "team": "finance",
        "team_context": (
            "Finance team — confidential. Publishes internal finance policies."
        ),
        "subdir_focus": (
            "Internal finance policies / SOPs. Examples: "
            "expense-policy-2026.md, travel-approval-workflow.md, "
            "corporate-card-issuance.md, reimbursement-cutoffs.md, "
            "fx-hedging-policy.md, invoice-approval-chain.md."
        ),
        "count": 10,
        "include_distractors": False,
    },
    # Compliance — 30 new files (org-wide, readable by all)
    {
        "dir": "org/compliance/security",
        "team": "org-wide",
        "team_context": (
            "Compliance / security docs that apply org-wide (readable by "
            "everyone). Canonical file `pii-handling.md` lives in the parent "
            "org/compliance/ directory; do not duplicate its rules."
        ),
        "subdir_focus": (
            "Security controls, incident response templates, access review "
            "procedures. Examples: incident-response-template.md, "
            "access-review-quarterly.md, threat-model-user-service.md, "
            "bug-bounty-program.md, saml-sso-runbook.md, "
            "secrets-rotation-schedule.md."
        ),
        "count": 10,
        "include_distractors": False,
    },
    {
        "dir": "org/compliance/policies",
        "team": "org-wide",
        "team_context": (
            "Org-wide compliance policies, readable by all."
        ),
        "subdir_focus": (
            "High-level corporate policies: acceptable use, data retention, "
            "byod, code of conduct. Examples: acceptable-use-policy.md, "
            "data-retention-schedule.md, byod-policy.md, "
            "code-of-conduct.md, third-party-risk-policy.md."
        ),
        "count": 10,
        "include_distractors": False,
    },
    {
        "dir": "org/compliance/playbooks",
        "team": "org-wide",
        "team_context": (
            "Org-wide compliance playbooks."
        ),
        "subdir_focus": (
            "Playbooks for compliance events and audits. Examples: "
            "soc2-audit-prep.md, gdpr-data-subject-request.md, "
            "vendor-security-questionnaire.md, breach-notification-playbook.md, "
            "hipaa-baa-review.md, policy-exception-workflow.md."
        ),
        "count": 10,
        "include_distractors": False,
    },
]


# -------------------- prompt & API helpers --------------------

SYSTEM_PROMPT = """You generate realistic synthetic team documentation for a research experiment.

Output requirements:
1. Respond with a single JSON array and NOTHING ELSE (no markdown fences, no prose before or after).
2. Each array element is an object with exactly two string fields: "filename" and "content".
3. "filename" must end in ".md" and use lowercase kebab-case, possibly with a date prefix.
4. "content" must be 20-80 lines of realistic markdown: headings, bullets, occasional code blocks, occasional internal links.
5. Content should sound like it was written by a practicing engineer or analyst for their team — specific, a little opinionated, occasionally referencing other teams or file paths by relative path (e.g. `runbooks/deploy.md`, `../evaluations/q1.md`).
6. Avoid boilerplate phrasing. Vary tone and structure across files.
"""

FORBIDDEN_CLAUSE = f"""
HARD CONSTRAINTS — the following substrings MUST NOT appear anywhere in any file you produce:
- "just deploy api" (verbatim)
- "0.85" (as any number — use different numbers for any precision/recall/score thresholds)
- "q1-2026-eval-v3" (verbatim)
- "test_concurrent_migration_safety" (verbatim)
- "4,712,300", "$4,712,300", "4712300" (any spend or budget figure in that range)
- Do NOT mention all three of DEPLOY_ENV, DEPLOY_REGION, and DEPLOY_COMMIT_SHA together in the same file.

If you find yourself about to write one of these, substitute a different value. These are canonical answers in a separate test harness and must stay unique to the canonical files.
"""


def build_user_prompt(chunk: dict[str, Any]) -> str:
    distractor = ""
    if chunk.get("include_distractors"):
        distractor = f"\nDISTRACTOR REQUIREMENT: {chunk['distractor_hint']}\n"
    return f"""Generate {chunk['count']} markdown files for the directory `{chunk['dir']}`.

TEAM CONTEXT:
{chunk['team_context']}

SUBDIRECTORY FOCUS:
{chunk['subdir_focus']}
{distractor}
{FORBIDDEN_CLAUSE}

Produce the JSON array of exactly {chunk['count']} {{filename, content}} objects now.
"""


def extract_json_array(text: str) -> list[dict[str, str]]:
    """Pull the first JSON array out of `text`. Be forgiving about code fences."""
    # Strip ```json ... ``` fences if present.
    fence = re.search(r"```(?:json)?\s*(\[.*?\])\s*```", text, re.DOTALL)
    if fence:
        text = fence.group(1)
    # Find the first '[' and matching last ']'.
    start = text.find("[")
    end = text.rfind("]")
    if start == -1 or end == -1 or end < start:
        raise ValueError("no JSON array in response")
    return json.loads(text[start : end + 1])


def call_api(client: anthropic.Anthropic, chunk: dict[str, Any]) -> list[dict[str, str]]:
    prompt = build_user_prompt(chunk)
    resp = client.messages.create(
        model=MODEL,
        max_tokens=16000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    text_parts = [b.text for b in resp.content if getattr(b, "type", None) == "text"]
    text = "\n".join(text_parts)
    return extract_json_array(text)


# -------------------- validation --------------------

FLAGGED: list[tuple[Path, str]] = []


def check_forbidden(path: Path, content: str) -> list[str]:
    hits = []
    for needle in FORBIDDEN_SUBSTRINGS:
        if needle in content:
            hits.append(needle)
    if all(t in content for t in FORBIDDEN_TRIPLE):
        hits.append("DEPLOY_ENV+DEPLOY_REGION+DEPLOY_COMMIT_SHA triple")
    return hits


# -------------------- main --------------------


def sanitize_filename(name: str) -> str:
    name = name.strip().lstrip("/").replace("..", "_")
    # Keep only basename; we control the directory.
    name = Path(name).name
    if not name.endswith(".md"):
        name = name + ".md"
    return name


def process_chunk(client: anthropic.Anthropic, chunk: dict[str, Any]) -> dict[str, int]:
    target_dir = MEMORY_STORE / chunk["dir"]
    target_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n[chunk] {chunk['dir']} (target count {chunk['count']})")

    files: list[dict[str, str]] | None = None
    for attempt in range(2):
        try:
            files = call_api(client, chunk)
            break
        except Exception as exc:
            print(f"  attempt {attempt + 1} failed: {exc}")
            time.sleep(2)
    if files is None:
        print(f"  WARNING: chunk {chunk['dir']} failed to generate, skipping")
        return {"written": 0, "skipped": 0, "flagged": 0, "failed": 1}

    written = skipped = flagged = 0
    for entry in files:
        if not isinstance(entry, dict):
            continue
        fname = entry.get("filename") or entry.get("name")
        content = entry.get("content")
        if not fname or not content:
            continue
        fname = sanitize_filename(fname)
        target = target_dir / fname
        if target in CANONICAL_PATHS or target.resolve() in {p.resolve() for p in CANONICAL_PATHS}:
            print(f"  skip canonical overwrite: {target}")
            skipped += 1
            continue
        if target.exists():
            skipped += 1
            continue
        hits = check_forbidden(target, content)
        if hits:
            FLAGGED.append((target, ", ".join(hits)))
            flagged += 1
            # Try a simple fix for 0.85 by bumping it slightly; otherwise keep flagged.
            # We still write the file but record the flag for the caller.
        target.write_text(content)
        written += 1
    print(f"  wrote={written} skipped={skipped} flagged={flagged}")
    return {"written": written, "skipped": skipped, "flagged": flagged, "failed": 0}


def main() -> int:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ANTHROPIC_API_KEY not set; .env not loaded?", file=sys.stderr)
        return 2
    client = anthropic.Anthropic()
    totals = {"written": 0, "skipped": 0, "flagged": 0, "failed": 0}
    for chunk in CHUNKS:
        res = process_chunk(client, chunk)
        for k, v in res.items():
            totals[k] += v

    print("\n--- summary ---")
    for k, v in totals.items():
        print(f"  {k}: {v}")
    if FLAGGED:
        print(f"\n{len(FLAGGED)} files contained forbidden substrings:")
        for p, reason in FLAGGED:
            print(f"  {p.relative_to(MEMORY_STORE)}: {reason}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
